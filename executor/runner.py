"""Runs inside the restricted container. The host service is the only caller.

A container is started ahead of time: it imports the libraries, prints READY and then waits
for exactly one job on stdin. It grades that job, prints one JSON line and exits.
"""

import ast
import contextlib
import importlib
import io
import json
import os
from pathlib import Path
import resource
import sys
import tempfile
import time
import unittest

READY = "READY"
CPU_BUDGET = 10  # seconds of CPU for the learner's code and tests, after the imports
# Imported before the job arrives so a submission pays only for its own tests.
PRELOAD = [
    "numpy", "pandas", "scipy", "scipy.stats", "scipy.optimize", "scipy.special",
    "sklearn", "sklearn.base", "sklearn.cluster", "sklearn.compose", "sklearn.datasets",
    "sklearn.ensemble", "sklearn.feature_extraction.text", "sklearn.impute", "sklearn.inspection",
    "sklearn.linear_model", "sklearn.metrics", "sklearn.model_selection", "sklearn.naive_bayes",
    "sklearn.neighbors", "sklearn.pipeline", "sklearn.preprocessing", "sklearn.tree",
    "cv2", "torch", "torch.nn", "torch.nn.functional", "torch.optim", "torch.utils.data",
    "fastapi", "fastapi.testclient", "httpx", "pydantic",
    "langchain_core.messages", "langchain_core.prompts", "langchain_core.tools",
    "langchain_core.output_parsers", "langchain_core.language_models.fake_chat_models",
    "langchain_core.embeddings", "langchain_core.vectorstores",
    "langgraph.graph", "langgraph.prebuilt", "langgraph.checkpoint.memory",
    "gymnasium",
]


class LimitedText(io.StringIO):
    def write(self, value):
        if self.tell() < 4000:
            super().write(value[: 4000 - self.tell()])
        return len(value)


class CountingResult(unittest.TestResult):
    """Records which tests passed (or were skipped), so tests that never ran are not counted."""

    def __init__(self):
        super().__init__()
        self.ok = set()

    def addSuccess(self, test):
        super().addSuccess(test)
        self.ok.add(test.id())

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.ok.add(test.id())


def preload():
    """Import the libraries and run one tiny operation in each, so first use is fast."""
    with open(os.devnull, "w") as quiet, contextlib.redirect_stdout(quiet), contextlib.redirect_stderr(quiet):
        for name in PRELOAD:
            try:
                importlib.import_module(name)
            except Exception:
                pass  # The validation image has every library; local test runs may not.
        with contextlib.suppress(Exception):
            import numpy, pandas
            pandas.DataFrame({"a": numpy.arange(4), "b": [0, 1, 0, 1]}).groupby("b").sum()
        with contextlib.suppress(Exception):
            import torch
            torch.set_num_threads(1)
            weight = torch.ones(3, requires_grad=True)
            (weight * 2).sum().backward()
        with contextlib.suppress(Exception):
            from sklearn.linear_model import LogisticRegression
            LogisticRegression().fit([[0.0], [1.0], [2.0], [3.0]], [0, 0, 1, 1])


def cpu_seconds():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_utime + usage.ru_stime


def main():
    preload()
    # Docker imposes memory, PID, network and wall-clock limits. These are additional
    # in-process limits; they do not replace the container boundary.
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    sys.__stdout__.write(READY + "\n")
    sys.__stdout__.flush()
    request = json.load(sys.stdin)
    # Charge only the job: the CPU already spent on imports is added to the budget.
    limit = int(cpu_seconds()) + CPU_BUDGET
    resource.setrlimit(resource.RLIMIT_CPU, (limit, limit + 1))
    started, cpu_started = time.monotonic(), cpu_seconds()
    code, tests, mode = request["code"], request["tests"], request["mode"]
    visible = [node.name for node in ast.walk(ast.parse(tests)) if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")][:3]
    all_count = len([node for node in ast.walk(ast.parse(tests)) if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")])
    total = len(visible) if mode == "run" else all_count
    output = LimitedText()
    work = Path(tempfile.mkdtemp(prefix="learn-", dir="/tmp"))
    (work / "solution.py").write_text(code)
    (work / "tests.py").write_text(tests)
    os.chdir(work)
    sys.path.insert(0, str(work))
    os.environ["AIMLGYM_TARGET"] = "solution"
    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            module = importlib.import_module("tests")
            suite = unittest.defaultTestLoader.loadTestsFromModule(module)
            cases = []

            def flatten(item):
                for child in item:
                    if isinstance(child, unittest.TestSuite):
                        flatten(child)
                    else:
                        cases.append(child)

            flatten(suite)
            if mode == "run":
                cases = [case for case in cases if case._testMethodName in visible]
            result = CountingResult()
            unittest.TestSuite(cases).run(result)
            failures = {case.id(): detail[-800:] for case, detail in result.failures + result.errors}
            # A failing setUpClass or module fixture stops its tests from running; they count as failed.
            fixture_errors = [detail[-800:] for case, detail in result.errors if not isinstance(case, unittest.TestCase)]
            passed = sum(case.id() in result.ok for case in cases)
            response = {"passed": passed, "total": len(cases), "status": "passed" if passed == len(cases) else "failed", "output": output.getvalue()[:4000],
                        # Names only (never test code), so a learner can see which checks failed.
                        "failed": [case._testMethodName for case in cases if case.id() not in result.ok]}
            if mode == "run":
                response["tests"] = [{"name": case._testMethodName, "passed": case.id() in result.ok,
                                      "message": None if case.id() in result.ok else failures.get(case.id(), fixture_errors[0] if fixture_errors else "Test did not run")}
                                     for case in cases]
    except BaseException as error:
        response = {"passed": 0, "total": total, "status": "failed", "output": (type(error).__name__ + ": " + str(error))[:4000]}
    # Measurements for capacity planning; the host service strips them from responses.
    response["stats"] = {"seconds": round(time.monotonic() - started, 3), "cpuSeconds": round(cpu_seconds() - cpu_started, 3),
                         "maxRssKb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    # Use the original stdout so the host sees exactly one JSON response after READY.
    sys.__stdout__.write(json.dumps(response, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
