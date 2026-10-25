"""Run every pack's tests with the current interpreter and record the results.

    python build/validate.py --label executor     # e.g. inside a venv matching the executor image
    python build/validate.py --label full         # e.g. with scikit-learn, SciPy and PyTorch installed

For each pack the tests run twice: against solution.py (every test must pass) and against
starter.py (at least one test must fail, so the tests are not vacuous). Results go to
build/results/<label>.json; reports.py reads every file in that folder.
"""
import argparse
import concurrent.futures
import importlib
import json
import os
import platform
import re
import subprocess
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
sys.path.insert(0, BUILD)
from path import PATH, TOPICS  # noqa: E402

PACKAGES = ["numpy", "pandas", "fastapi", "pydantic", "httpx", "starlette", "sklearn", "scipy", "torch", "cv2",
            "langchain_core", "langgraph", "gymnasium"]


def versions():
    out = {"python": platform.python_version()}
    for name in PACKAGES:
        try:
            out[name] = importlib.import_module(name).__version__
        except Exception:
            out[name] = None
    return out


def run(d, target):
    env = dict(os.environ, AIMLGYM_TARGET=target, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-m", "unittest", "tests", "-v"], cwd=d, env=env,
                       capture_output=True, text=True, timeout=180)
    out = r.stderr + r.stdout
    ran = int(m.group(1)) if (m := re.search(r"^Ran (\d+) test", out, re.M)) else 0
    skipped = int(m.group(1)) if (m := re.search(r"skipped=(\d+)", out)) else 0
    return r.returncode == 0, ran, skipped, out


def is_project(tslug, slug):
    """Project ideas are ungraded: they have no tests to run."""
    with open(os.path.join(ROOT, "topics", tslug, slug, "metadata.json"), encoding="utf-8") as fh:
        return json.load(fh).get("kind") == "project"


def check(job):
    tslug, slug = job
    d = os.path.join(ROOT, "topics", tslug, slug)
    meta = json.load(open(os.path.join(d, "metadata.json"), encoding="utf-8"))
    ok, ran, skipped, out = run(d, "solution")
    s_ok, s_ran, _, _ = run(d, "starter")
    status = "passed" if ok and ran == meta["test_count"] else "FAILED"
    return {
        "id": meta["id"], "slug": slug, "tests": ran, "expected_tests": meta["test_count"],
        "skipped": skipped, "solution_passed": ok, "starter_fails": not s_ok,
        "status": status if not s_ok else status + "; starter passes all tests",
        "log": "" if ok else out[-4000:],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--only", nargs="*", help="limit to these topic slugs")
    args = ap.parse_args()
    jobs = [(t[0], s) for t in TOPICS for s in PATH[t[0]] if (not args.only or t[0] in args.only)
            and not is_project(t[0], s)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        results = list(pool.map(check, jobs))
    bad = [r for r in results if r["status"] != "passed"]
    for r in bad:
        print(f"{r['id']:6} {r['slug']:30} {r['status']} ({r['tests']}/{r['expected_tests']})")
        if r["log"]:
            print(r["log"][-2500:])
    record = {"label": args.label, "environment": versions(), "packs": results,
              "partial": bool(args.only)}
    os.makedirs(os.path.join(BUILD, "results"), exist_ok=True)
    if not args.only:
        with open(os.path.join(BUILD, "results", f"{args.label}.json"), "w") as fh:
            json.dump(record, fh, indent=1)
    print(f"{args.label}: {len(results) - len(bad)}/{len(results)} packs passed; "
          f"{sum(r['tests'] for r in results)} tests run, {sum(r['skipped'] for r in results)} skipped")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
