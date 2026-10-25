"""Grade every pack through the warm-container scheduler and record time and memory.

    LEARN_EXECUTOR_IMAGE=epoch-learn-runner:latest python3 -m executor.measure [--only slug ...]

Run from the repository root on the executor host. For each pack the reference solution must
pass in Run and Submit mode and the starter must fail Submit. Results go to
executor/measurements.json (or --output); the summary is printed. Uses the real limits and pool settings.
"""

import argparse
import concurrent.futures
import json
from pathlib import Path
import platform
import statistics
import subprocess
import threading
import time

from executor import service

ROOT = Path(__file__).resolve().parents[1]


def grade(slug, mode, code):
    started = time.monotonic()
    raw = service.execute({"mode": mode, "slug": slug, "code": code})
    clean = service.sanitize_result({"mode": mode, "slug": slug}, raw)
    return clean, raw.get("stats", {}), time.monotonic() - started


def measure(slug, pack):
    row = {"slug": slug}
    try:
        solution, stats, total = grade(slug, "submit", pack["solution"])
        row.update(submitPassed=solution["status"] == "passed", seconds=stats.get("seconds"), cpuSeconds=stats.get("cpuSeconds"),
                   maxRssMb=round(stats.get("maxRssKb", 0) / 1024), endToEndSeconds=round(total, 3))
        row["runPassed"] = grade(slug, "run", pack["solution"])[0]["status"] == "passed"
        row["starterFails"] = grade(slug, "submit", pack["starter"])[0]["status"] == "failed"
    except Exception as error:
        row["error"] = type(error).__name__ + ": " + str(error)[:200]
    row["ok"] = bool(row.get("submitPassed") and row.get("runPassed") and row.get("starterFails"))
    return row


class Progress:
    """Prints one line per finished pack: position, outcome, timings, failures so far and an ETA."""

    def __init__(self, total):
        self.total, self.done, self.failed = total, 0, 0
        self.started = time.monotonic()
        self.lock = threading.Lock()

    def start(self, image, slots, pool, memory):
        print(f"Measuring {self.total} packs ({3 * self.total} jobs) with {image}: "
              f"{slots} slot(s), {pool} warm container(s), {memory} per job", flush=True)

    def finish(self, row):
        with self.lock:
            self.done += 1
            self.failed += not row["ok"]
            elapsed = time.monotonic() - self.started
            eta = elapsed / self.done * (self.total - self.done)
            if row["ok"]:
                detail = f"test {row['seconds']:.2f}s cpu {row['cpuSeconds']:.2f}s mem {row['maxRssMb']}MB end-to-end {row['endToEndSeconds']:.1f}s"
            else:
                checks = [name for name in ("submitPassed", "runPassed", "starterFails") if not row.get(name)]
                detail = row.get("error") or "failed: " + ", ".join(checks)
            print(f"[{self.done:>{len(str(self.total))}}/{self.total}] {'ok  ' if row['ok'] else 'FAIL'} {row['slug']:<34} {detail}"
                  f"  | {self.failed} failed, {elapsed / 60:.1f} min elapsed, ~{eta / 60:.1f} min left", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--output", default=str(ROOT / "executor" / "measurements.json"))
    args = parser.parse_args()
    packs = json.loads((ROOT / "lib" / "learn" / "packs.generated.json").read_text())
    slugs = [slug for slug in packs if not args.only or slug in args.only]
    with service.SCHEDULER.condition:
        service.SCHEDULER.refill()
    progress = Progress(len(slugs))
    progress.start(service.IMAGE, service.JOB_SLOTS, service.POOL_SIZE, service.JOB_MEMORY)

    def measured(slug):
        row = measure(slug, packs[slug])
        progress.finish(row)
        return row

    started = time.monotonic()
    # One client per job slot keeps every slot busy, as during a lab session.
    with concurrent.futures.ThreadPoolExecutor(max_workers=service.JOB_SLOTS) as pool:
        rows = list(pool.map(measured, slugs))
    elapsed = time.monotonic() - started
    service.SCHEDULER.close()
    ok = [row for row in rows if row["ok"]]
    timed = [row for row in rows if row.get("seconds") is not None] or [{"slug": "", "seconds": 0, "cpuSeconds": 0, "maxRssMb": 0, "endToEndSeconds": 0}]
    heaviest = sorted(timed, key=lambda row: row["seconds"], reverse=True)[:10]
    summary = {
        "date": time.strftime("%Y-%m-%d"), "host": f"{platform.system()} {platform.machine()}", "image": service.IMAGE,
        "imageId": subprocess.run(["docker", "image", "inspect", "-f", "{{.Id}}", service.IMAGE], capture_output=True, text=True).stdout.strip(),
        "packs": len(rows), "allChecksPassed": len(ok), "jobs": 3 * len(rows), "wallSeconds": round(elapsed, 1),
        "jobsPerMinute": round(3 * len(rows) / elapsed * 60, 1),
        "testSeconds": {"median": statistics.median(row["seconds"] for row in timed), "max": max(row["seconds"] for row in timed)},
        "endToEndSeconds": {"median": statistics.median(row["endToEndSeconds"] for row in timed), "max": max(row["endToEndSeconds"] for row in timed)},
        "maxRssMb": {"median": statistics.median(row["maxRssMb"] for row in timed), "max": max(row["maxRssMb"] for row in timed)},
        "heaviest": [{key: row[key] for key in ("slug", "seconds", "cpuSeconds", "maxRssMb")} for row in heaviest],
        "failures": [row for row in rows if not row["ok"]],
    }
    Path(args.output).write_text(json.dumps({"summary": summary, "packs": rows}, indent=1) + "\n")
    print(f"\nDone in {elapsed / 60:.1f} min: {len(ok)}/{len(rows)} packs passed every check. Full results: {args.output}\nSummary:", flush=True)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
