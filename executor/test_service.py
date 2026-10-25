import io
import json
from pathlib import Path
import threading
import time
import unittest
from unittest.mock import patch

from executor import service


class ServiceTests(unittest.TestCase):
    def test_submit_never_returns_test_source_or_user_output(self):
        request = {"mode": "submit", "slug": "factorial-validated"}
        count = service.TESTS[request["slug"]]["testCount"]
        result = service.sanitize_result(request, {"passed": count, "total": count, "status": "passed", "output": "private test source", "tests": [{"name": "hidden"}]})
        self.assertEqual(result, {"passed": count, "total": count, "status": "passed"})

    def test_submit_returns_failed_test_names_only(self):
        request = {"mode": "submit", "slug": "variables"}
        count = service.TESTS["variables"]["testCount"]
        result = service.sanitize_result(request, {"passed": count - 1, "total": count, "status": "failed", "failed": ["test_output"], "output": "secret"})
        self.assertEqual(result, {"passed": count - 1, "total": count, "status": "failed", "failed": ["test_output"]})

    def test_unknown_or_inconsistent_failed_names_are_dropped(self):
        request = {"mode": "submit", "slug": "variables"}
        count = service.TESTS["variables"]["testCount"]
        for failed in (["test_made_up"], ["test_output", "test_name"], "test_output", ["test_output", "test_output"]):
            result = service.sanitize_result(request, {"passed": count - 1, "total": count, "status": "failed", "failed": failed})
            self.assertNotIn("failed", result)

    def test_run_returns_only_visible_names_and_pass_flags(self):
        request = {"mode": "run", "slug": "factorial-validated"}
        names = service.TESTS[request["slug"]]["visibleNames"]
        rows = [{"name": name, "passed": True, "message": "private source"} for name in names]
        result = service.sanitize_result(request, {"passed": 3, "total": 3, "status": "passed", "tests": rows, "output": "private source"})
        self.assertEqual(result["tests"], [{"name": name, "passed": True} for name in names])
        self.assertNotIn("output", result)

    def test_wrong_test_count_cannot_be_recorded(self):
        with self.assertRaises(ValueError):
            service.sanitize_result({"mode": "submit", "slug": "factorial-validated"}, {"passed": 3, "total": 3, "status": "passed"})

    def test_authentication_runs_before_container(self):
        handler = object.__new__(service.Handler)
        handler.path = "/execute"
        handler.headers = {"Authorization": "Bearer wrong", "Content-Length": "1"}
        handler.rfile = io.BytesIO(b"x")
        handler.wfile = io.BytesIO()
        handler.send_response = lambda status: setattr(handler, "status", status)
        handler.send_header = lambda *args: None
        handler.end_headers = lambda: None
        with patch.object(service, "TOKEN", "a" * 64), patch.object(service, "run_container") as run:
            handler.do_POST()
        self.assertEqual(handler.status, 401)
        self.assertEqual(json.loads(handler.wfile.getvalue()), {"error": "Unauthorized"})
        run.assert_not_called()


    def test_busy_queue_returns_503_without_running(self):
        handler = object.__new__(service.Handler)
        body = json.dumps({"mode": "run", "slug": "factorial-validated", "code": "x = 1", "client": "a" * 64}).encode()
        handler.path = "/execute"
        handler.headers = {"Authorization": "Bearer " + "a" * 64, "Content-Length": str(len(body))}
        handler.rfile = io.BytesIO(body)
        handler.wfile = io.BytesIO()
        handler.send_response = lambda status: setattr(handler, "status", status)
        handler.send_header = lambda *args: None
        handler.end_headers = lambda: None
        with patch.object(service, "TOKEN", "a" * 64), patch.object(service, "run_container", side_effect=service.Busy):
            handler.do_POST()
        self.assertEqual((handler.status, json.loads(handler.wfile.getvalue())), (503, {"error": "Busy"}))

    def test_executor_requirements_match_validation_environment(self):
        root = Path(__file__).resolve().parents[1]
        pins = lambda path: [line for line in path.read_text().splitlines() if line and not line.startswith("#")]
        self.assertEqual(pins(root / "executor" / "requirements.txt"), pins(root / "aimlgym" / "build" / "requirements-executor.txt"))


    def test_runner_counts_tests_blocked_by_fixture_as_failed(self):
        import subprocess, sys
        tests = (
            "import unittest\n"
            "class T(unittest.TestCase):\n"
            "    @classmethod\n"
            "    def setUpClass(cls):\n"
            "        raise ValueError('boom')\n"
            + "".join(f"    def test_{i}(self):\n        pass\n" for i in range(6))
        )
        out = subprocess.run([sys.executable, "-B", str(Path(__file__).parent / "runner.py")],
                             input=json.dumps({"mode": "run", "code": "x = 1", "tests": tests}),
                             capture_output=True, text=True, timeout=120).stdout.strip().splitlines()
        result = json.loads(out[-1])
        self.assertEqual((result["passed"], result["total"], result["status"]), (0, 3, "failed"))
        self.assertTrue(all(not row["passed"] and "boom" in row["message"] for row in result["tests"]))


    def post(self, body):
        handler = object.__new__(service.Handler)
        data = json.dumps(body).encode()
        handler.path = "/execute"
        handler.headers = {"Authorization": "Bearer " + "a" * 64, "Content-Length": str(len(data))}
        handler.rfile = io.BytesIO(data)
        handler.wfile = io.BytesIO()
        handler.sent = {}
        handler.send_response = lambda status: setattr(handler, "status", status)
        handler.send_header = lambda name, value: handler.sent.__setitem__(name, value)
        handler.end_headers = lambda: None
        handler.do_POST()
        return handler.status, json.loads(handler.wfile.getvalue()), handler.sent

    def test_client_key_required(self):
        with patch.object(service, "TOKEN", "a" * 64), patch.object(service, "run_container") as run:
            status, body, _ = self.post({"mode": "run", "slug": "factorial-validated", "code": "x = 1"})
        self.assertEqual((status, body), (400, {"error": "Invalid request"}))
        run.assert_not_called()

    def test_rate_limited_requests_get_429(self):
        limiter = service.ClientLimiter({"run": 2, "submit": 1})
        request = {"mode": "run", "slug": "factorial-validated", "code": "x = 1", "client": "b" * 64}
        with patch.object(service, "TOKEN", "a" * 64), patch.object(service, "LIMITER", limiter), \
                patch.object(service, "run_container", return_value={"passed": 3, "total": 3, "status": "passed"}) as run:
            codes = [self.post(request)[0] for _ in range(3)]
            status, body, headers = self.post(request)
        self.assertEqual(codes, [200, 200, 429])
        self.assertEqual((status, body["error"]), (429, "Too many requests"))
        self.assertGreaterEqual(int(headers["Retry-After"]), 1)
        self.assertEqual(run.call_count, 2)


class ClientLimiterTests(unittest.TestCase):
    def setUp(self):
        self.now = [0.0]
        self.limiter = service.ClientLimiter({"run": 3, "submit": 1}, clock=lambda: self.now[0])

    def use(self, client, mode):
        self.limiter.acquire(client, mode)
        self.limiter.release(client)

    def test_bucket_and_refill(self):
        for _ in range(3):
            self.use("c1", "run")
        with self.assertRaises(service.RateLimited) as caught:
            self.use("c1", "run")
        self.assertEqual(caught.exception.retry_after, 20)
        self.now[0] = 20.0
        self.use("c1", "run")

    def test_modes_and_clients_are_separate(self):
        self.use("c1", "submit")
        with self.assertRaises(service.RateLimited):
            self.use("c1", "submit")
        self.use("c1", "run")
        self.use("c2", "submit")

    def test_one_request_in_flight(self):
        self.limiter.acquire("c1", "run")
        with self.assertRaises(service.RateLimited) as caught:
            self.limiter.acquire("c1", "submit")
        self.assertEqual(caught.exception.reason, "A request is already running")
        self.limiter.release("c1")
        self.limiter.acquire("c1", "submit")

    def test_prune_keeps_only_partial_buckets(self):
        self.use("c1", "run")
        self.now[0] = 1000.0
        self.use("c2", "run")
        with self.limiter.lock:
            self.limiter.prune(self.now[0])
        self.assertEqual(list(self.limiter.buckets), [("c2", "run")])


class FakeContainer:
    """Stands in for a warm Docker container; a job blocks until its gate opens."""

    def __init__(self, log, gates):
        self.log, self.gates, self.used = log, gates, False
        log.append("start")

    def wait_ready(self):
        pass

    def alive(self):
        return not self.used

    def execute(self, payload):
        assert not self.used, "a container must run only one job"
        self.used = True
        self.log.append(payload["name"])
        self.gates.setdefault(payload["name"], threading.Event()).wait(5)
        return {"name": payload["name"]}

    def remove(self):
        pass


class SchedulerTests(unittest.TestCase):
    def setUp(self):
        self.log, self.gates = [], {}
        self.scheduler = service.Scheduler(start=lambda: FakeContainer(self.log, self.gates))

    def tearDown(self):
        for gate in self.gates.values():
            gate.set()
        self.scheduler.close()

    def wait_for(self, condition):
        deadline = time.monotonic() + 3
        while not condition():
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.01)

    def submit(self, mode, name, results):
        self.gates.setdefault(name, threading.Event())
        thread = threading.Thread(target=lambda: results.append(self._run(mode, name)))
        thread.start()
        return thread

    def _run(self, mode, name):
        try:
            return self.scheduler.run(mode, {"name": name})["name"]
        except service.Busy:
            return "busy:" + name

    def test_pool_preloads_two_containers_and_uses_each_once(self):
        with self.scheduler.condition:
            self.scheduler.refill()
        self.wait_for(lambda: len(self.scheduler.ready) == service.POOL_SIZE)
        self.assertEqual(self.log.count("start"), 2)
        results = []
        self.gates["one"] = threading.Event()
        self.gates["one"].set()
        self.submit("submit", "one", results).join(3)
        self.assertEqual(results, ["one"])
        # The used container is gone and a replacement keeps the pool full.
        self.wait_for(lambda: len(self.scheduler.ready) == service.POOL_SIZE)
        self.assertEqual(self.log.count("start"), 3)

    def test_two_jobs_run_at_once_and_refill_waits_for_a_free_slot(self):
        results = []
        threads = [self.submit("run", name, results) for name in ("a", "b")]
        self.wait_for(lambda: self.scheduler.executing == 2)
        starts = self.log.count("start")
        time.sleep(0.1)
        self.assertEqual(self.log.count("start"), starts, "no container starts while both slots run jobs")
        self.gates["a"].set()
        # A finished job frees a slot, so the pool is (or stays) full; never more than
        # POOL_SIZE waiting containers plus one per running job exist.
        self.wait_for(lambda: len(self.scheduler.ready) == service.POOL_SIZE)
        self.assertLessEqual(self.log.count("start"), service.POOL_SIZE + service.JOB_SLOTS)
        self.gates["b"].set()
        for thread in threads:
            thread.join(3)
        self.assertEqual(sorted(results), ["a", "b"])

    def test_submit_is_served_before_run_and_full_queue_is_busy(self):
        results = []
        busy = [self.submit("run", name, results) for name in ("x", "y")]
        self.wait_for(lambda: self.scheduler.executing == 2)
        with patch.object(service, "QUEUE_LIMIT", 2):
            waiting = [self.submit("run", "run-1", results)]
            self.wait_for(lambda: len(self.scheduler.queue) == 1)
            waiting.append(self.submit("submit", "submit-1", results))
            self.wait_for(lambda: len(self.scheduler.queue) == 2)
            self.submit("run", "overflow", results).join(3)
        self.assertEqual(results, ["busy:overflow"])
        # Free one slot: the later Submit takes it ahead of the earlier Run.
        self.gates["x"].set()
        self.wait_for(lambda: "submit-1" in self.log)
        self.assertNotIn("run-1", self.log)
        for name in ("y", "run-1", "submit-1"):
            self.gates[name].set()
        for thread in busy + waiting:
            thread.join(3)
        jobs = [entry for entry in self.log if entry in ("run-1", "submit-1")]
        self.assertEqual(jobs, ["submit-1", "run-1"])

    def test_request_that_waits_too_long_is_busy(self):
        results = []
        threads = [self.submit("run", name, results) for name in ("p", "q")]
        self.wait_for(lambda: self.scheduler.executing == 2)
        with patch.object(service, "QUEUE_WAIT", 0.2):
            self.submit("submit", "late", results).join(3)
        self.assertEqual(results, ["busy:late"])
        self.assertEqual(self.scheduler.queue, [])
        for name in ("p", "q"):
            self.gates[name].set()
        for thread in threads:
            thread.join(3)


if __name__ == "__main__":
    unittest.main()
