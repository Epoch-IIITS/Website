"""Private HTTP entry point behind an HTTPS reverse proxy on the VPS."""

import heapq
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import itertools
import json
import math
import os
from pathlib import Path
import re
import selectors
import subprocess
import threading
import time
from uuid import uuid4

TESTS = json.loads((Path(__file__).parent / "tests.generated.json").read_text())
TOKEN = os.environ.get("LEARN_EXECUTOR_TOKEN", "")
IMAGE = os.environ.get("LEARN_EXECUTOR_IMAGE", "epoch-learn-runner:latest")
MAX_BODY = 20000
MAX_OUTPUT = 65536
# Sized for 2 vCPU / 4 GB; override for smaller test machines (see README.md).
JOB_SLOTS = int(os.environ.get("LEARN_EXECUTOR_SLOTS", "2"))  # jobs running at once, one per vCPU
POOL_SIZE = int(os.environ.get("LEARN_EXECUTOR_POOL", "2"))  # preloaded containers waiting for a job
JOB_MEMORY = os.environ.get("LEARN_EXECUTOR_MEMORY", "1g")  # per container, swap disabled
QUEUE_LIMIT = 30  # requests waiting for a job slot
QUEUE_WAIT = 30  # seconds a request may wait for a slot and a warm container
TIMEOUT = 30  # wall-clock seconds per job once its code is sent
START_TIMEOUT = 120  # seconds for a new container to import the libraries
PRIORITY = {"submit": 0, "run": 1}  # Submit is served before Run
# Per-client limits (client = a hash of the signed-in user id sent by Next.js): requests per minute
# by mode, and one request in flight at a time.
RATE_LIMITS = {"run": int(os.environ.get("LEARN_EXECUTOR_RUNS_PER_MINUTE", "10")),
               "submit": int(os.environ.get("LEARN_EXECUTOR_SUBMITS_PER_MINUTE", "5"))}
CLIENT_PATTERN = re.compile(r"[a-f0-9]{32,64}")


class Busy(Exception):
    pass


def sanitize_result(request, result):
    pack = TESTS[request["slug"]]
    expected = len(pack["visibleNames"]) if request["mode"] == "run" else pack["testCount"]
    if not isinstance(result, dict) or result.get("total") != expected or type(result.get("passed")) is not int or not 0 <= result["passed"] <= expected or result.get("status") != ("passed" if result["passed"] == expected else "failed"):
        raise ValueError("Invalid container result")
    clean = {"passed": result["passed"], "total": expected, "status": result["status"]}
    failed = result.get("failed")
    known = set(pack.get("testNames", []) if request["mode"] == "submit" else pack["visibleNames"])
    if request["mode"] == "submit" and isinstance(failed, list) and len(failed) == expected - result["passed"] \
            and len(set(failed)) == len(failed) and all(isinstance(name, str) and name in known for name in failed):
        clean["failed"] = failed
    if request["mode"] == "run":
        rows = result.get("tests")
        if not isinstance(rows, list) or len(rows) != expected or any(not isinstance(row, dict) or type(row.get("passed")) is not bool for row in rows) or {row["name"] for row in rows} != set(pack["visibleNames"]) or sum(row["passed"] for row in rows) != result["passed"]:
            raise ValueError("Invalid visible results")
        clean["tests"] = [{"name": row["name"], "passed": row["passed"]} for row in rows]
    return clean


def docker_command(name):
    return [
        "docker", "run", "--rm", "--pull", "never", "--name", name, "--interactive",
        "--network", "none", "--read-only", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges", "--user", "65534:65534",
        "--memory", JOB_MEMORY, "--memory-swap", JOB_MEMORY, "--cpus", "1",
        "--pids-limit", "64", "--ulimit", "nofile=64:64",
        "--ulimit", "fsize=1048576:1048576",
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=32m,mode=1777",
        IMAGE,
    ]


class Container:
    """A started runner that has imported the libraries and is waiting for one job."""

    def __init__(self):
        self.name = "epoch-learn-" + uuid4().hex
        self.process = subprocess.Popen(docker_command(self.name), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        self.output = bytearray()

    def read_until(self, done, deadline):
        """Read stdout until done(output) is true or the stream closes; False on close."""
        while not done(self.output):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Container timed out")
            for key, _ in self.selector.select(min(remaining, 0.2)):
                chunk = os.read(key.fd, 4096)
                if not chunk:
                    return False
                self.output.extend(chunk)
                if len(self.output) > MAX_OUTPUT:
                    raise ValueError("Output limit exceeded")
        return True

    def wait_ready(self):
        try:
            # Anything a library printed while importing comes before READY and is dropped.
            if not self.read_until(lambda output: b"READY\n" in output, time.monotonic() + START_TIMEOUT):
                raise RuntimeError("Container did not start")
            del self.output[:self.output.index(b"READY\n") + 6]
        except BaseException:
            self.remove()
            raise

    def alive(self):
        return self.process.poll() is None

    def execute(self, payload):
        """Send one job and return the runner's JSON result. The container exits afterwards."""
        try:
            assert self.process.stdin
            self.process.stdin.write(json.dumps(payload).encode())
            self.process.stdin.close()
            self.read_until(lambda output: False, time.monotonic() + TIMEOUT)
            if self.process.wait(timeout=1) != 0:
                raise RuntimeError("Container failed")
            return json.loads(self.output.decode())
        finally:
            self.remove()

    def remove(self):
        self.selector.close()
        if self.process.poll() is None:
            self.process.kill()
            self.process.wait(timeout=2)
            subprocess.run(["docker", "rm", "-f", self.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)


class Scheduler:
    """Admits at most JOB_SLOTS jobs, queues up to QUEUE_LIMIT more (Submit first) and keeps
    POOL_SIZE warm containers. A container starts only while fewer than JOB_SLOTS containers
    are busy (running a job or importing), so refilling never competes with running tests."""

    def __init__(self, start=Container):
        self.start = start
        self.condition = threading.Condition()
        self.queue = []
        self.order = itertools.count()
        self.admitted = 0
        self.ready = []
        self.starting = 0
        self.executing = 0
        self.waiting = 0  # admitted jobs that have no container yet
        self.takers = []  # their order of arrival
        self.failures = 0
        self.retry_at = 0.0
        self.closed = False

    def run(self, mode, payload):
        deadline = time.monotonic() + QUEUE_WAIT
        self.admit(PRIORITY[mode], deadline)
        try:
            container = self.take(deadline)
            try:
                return container.execute(payload)
            finally:
                with self.condition:
                    self.executing -= 1
                    self.refill()
        finally:
            with self.condition:
                self.admitted -= 1
                self.condition.notify_all()

    def admit(self, priority, deadline):
        with self.condition:
            if len(self.queue) >= QUEUE_LIMIT:
                raise Busy()
            ticket = (priority, next(self.order))
            heapq.heappush(self.queue, ticket)
            while self.admitted >= JOB_SLOTS or self.queue[0] != ticket:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    self.queue.remove(ticket)
                    heapq.heapify(self.queue)
                    self.condition.notify_all()
                    raise Busy()
                self.condition.wait(remaining)
            heapq.heappop(self.queue)
            self.admitted += 1
            self.condition.notify_all()

    def take(self, deadline):
        # Admitted jobs receive containers in arrival order; otherwise, when containers are
        # scarce, one job can lose every race for a new container until its deadline passes.
        with self.condition:
            ticket = object()
            self.takers.append(ticket)
            self.waiting += 1
            container = None
            try:
                while not container:
                    while self.ready and self.takers[0] is ticket and not container:
                        container = self.ready.pop(0)
                        if not container.alive():
                            container.remove()
                            container = None
                    if not container:
                        self.refill()
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            raise Busy()
                        self.condition.wait(min(remaining, 1))
            finally:
                self.takers.remove(ticket)
                self.waiting -= 1
                self.condition.notify_all()
            # Counted as executing (not waiting) before refilling, so the pool is not over-filled.
            self.executing += 1
            self.refill()
            return container

    def refill(self):
        """Start containers while warm ones are missing and a CPU is free. Caller holds the lock."""
        while (not self.closed and len(self.ready) + self.starting < POOL_SIZE + self.waiting
               and self.starting + self.executing < JOB_SLOTS and time.monotonic() >= self.retry_at):
            self.starting += 1
            threading.Thread(target=self.warm, daemon=True).start()

    def warm(self):
        container = None
        try:
            container = self.start()
            container.wait_ready()
        except Exception as error:
            print("executor container start failed:", type(error).__name__, str(error)[:200], flush=True)
            container = None
        with self.condition:
            self.starting -= 1
            if container and not self.closed:
                self.ready.append(container)
                self.failures = 0
                self.refill()  # this start freed a CPU, so another may now begin
            else:
                # Back off when Docker or the image is broken instead of retrying in a tight loop.
                self.failures += 1
                self.retry_at = time.monotonic() + min(30, 2 ** self.failures)
                threading.Timer(min(30, 2 ** self.failures), self.wake).start()
            self.condition.notify_all()
        if container and self.closed:
            container.remove()

    def wake(self):
        with self.condition:
            self.refill()
            self.condition.notify_all()

    def close(self):
        with self.condition:
            self.closed = True
            ready, self.ready = self.ready, []
        for container in ready:
            container.remove()


class RateLimited(Exception):
    def __init__(self, retry_after, reason):
        super().__init__(reason)
        self.retry_after = max(1, math.ceil(retry_after))
        self.reason = reason


class ClientLimiter:
    """Token buckets per (client, mode) plus one request in flight per client.

    Each bucket holds up to RATE_LIMITS[mode] tokens and refills that many per minute. The service is a
    single process, so these counts are exact across every Next.js instance that calls it.
    """

    def __init__(self, limits=None, clock=time.monotonic):
        self.limits = limits or RATE_LIMITS
        self.clock = clock
        self.lock = threading.Lock()
        self.buckets = {}
        self.in_flight = set()

    def acquire(self, client, mode):
        capacity = self.limits[mode]
        rate = capacity / 60.0
        now = self.clock()
        with self.lock:
            if client in self.in_flight:
                raise RateLimited(1, "A request is already running")
            tokens, last = self.buckets.get((client, mode), (float(capacity), now))
            tokens = min(capacity, tokens + (now - last) * rate)
            if tokens < 1:
                self.buckets[(client, mode)] = (tokens, now)
                raise RateLimited((1 - tokens) / rate, "Too many requests")
            self.buckets[(client, mode)] = (tokens - 1, now)
            self.in_flight.add(client)
            if len(self.buckets) > 10000:
                self.prune(now)

    def release(self, client):
        with self.lock:
            self.in_flight.discard(client)

    def prune(self, now):
        """Drop buckets that have refilled completely; they hold no information. Caller holds the lock."""
        for key, (tokens, last) in list(self.buckets.items()):
            if tokens + (now - last) * self.limits[key[1]] / 60.0 >= self.limits[key[1]]:
                del self.buckets[key]


SCHEDULER = Scheduler()
LIMITER = ClientLimiter()


def execute(request):
    """Grade one request in a fresh warm container and return the runner's full result."""
    payload = {"mode": request["mode"], "code": request["code"], "tests": TESTS[request["slug"]]["tests"]}
    return SCHEDULER.run(request["mode"], payload)


def run_container(request):
    return sanitize_result(request, execute(request))


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, body, headers=None):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/execute":
            self.respond(404, {"error": "Not found"})
            return
        auth = self.headers.get("Authorization", "")
        if not TOKEN or not hmac.compare_digest(auth, "Bearer " + TOKEN):
            self.respond(401, {"error": "Unauthorized"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > MAX_BODY:
                raise ValueError("Invalid request size")
            request = json.loads(self.rfile.read(length))
            if not isinstance(request, dict) or request.get("mode") not in {"run", "submit"} or not isinstance(request.get("slug"), str) or not re.fullmatch(r"[a-z0-9-]{1,100}", request["slug"]) or request["slug"] not in TESTS or not isinstance(request.get("code"), str) or not 0 < len(request["code"].encode()) <= 16000 or not isinstance(request.get("client"), str) or not CLIENT_PATTERN.fullmatch(request["client"]):
                raise ValueError("Invalid request")
        except (ValueError, UnicodeError, json.JSONDecodeError):
            self.respond(400, {"error": "Invalid request"})
            return
        try:
            LIMITER.acquire(request["client"], request["mode"])
        except RateLimited as limited:
            self.respond(429, {"error": limited.reason, "retryAfter": limited.retry_after}, {"Retry-After": str(limited.retry_after)})
            return
        try:
            self.respond(200, run_container(request))
        except Busy:
            self.respond(503, {"error": "Busy"})
        except Exception:
            self.respond(503, {"error": "Execution unavailable"})
        finally:
            LIMITER.release(request["client"])

    def log_message(self, format, *args):
        # Access logs must never include request bodies or credentials.
        print("executor request", self.address_string(), format % args, flush=True)


if __name__ == "__main__":
    if len(TOKEN) < 32:
        raise SystemExit("Set a random LEARN_EXECUTOR_TOKEN of at least 32 characters")
    if JOB_SLOTS < 1 or POOL_SIZE < 1 or not re.fullmatch(r"\d+[mg]", JOB_MEMORY):
        raise SystemExit("LEARN_EXECUTOR_SLOTS and LEARN_EXECUTOR_POOL must be >= 1 and LEARN_EXECUTOR_MEMORY like 768m or 1g")
    with SCHEDULER.condition:
        SCHEDULER.refill()
    ThreadingHTTPServer(("127.0.0.1", int(os.environ.get("LEARN_EXECUTOR_PORT", "8765"))), Handler).serve_forever()
