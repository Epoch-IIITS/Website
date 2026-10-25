"""Tests for AG-17 Orchestrator-Workers Pipeline by Hand.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import importlib
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = importlib.import_module(os.environ.get("AIMLGYM_TARGET", "solution"))


def planner(task, feedback):
    style = "long" if feedback == "too short" else "short"
    return [{"id": "a_research", "type": "research", "input": task, "deps": []},
            {"id": "b_write", "type": "write", "input": style, "deps": ["a_research"]}]

workers = {
    "research": lambda inp, deps: f"facts about {inp.split(' on ')[-1]}",
    "write": lambda style, deps: (deps["a_research"] if style == "short"
                                  else "Report: " + deps["a_research"] + " with details and sources"),
}

def evaluator(task, outputs):
    words = len(outputs["b_write"].split())
    return (words >= 5, "too short" if words < 5 else "")

class TestOrchestrator(unittest.TestCase):
    def test_two_rounds(self):
        r = S.orchestrate("brief on solar", planner, workers, evaluator)
        self.assertEqual((r["accepted"], r["rounds"]), (True, 2))
        self.assertTrue(r["outputs"]["b_write"].startswith("Report: facts about solar"))

    def test_log(self):
        r = S.orchestrate("brief on solar", planner, workers, evaluator)
        self.assertEqual(r["log"], [
            "round 1: plan ['a_research', 'b_write']", "round 1: a_research -> research", "round 1: b_write -> write",
            "round 1: evaluator rejected: too short",
            "round 2: plan ['a_research', 'b_write']", "round 2: a_research -> research", "round 2: b_write -> write",
            "round 2: evaluator accepted"])

    def test_round_cap(self):
        r = S.orchestrate("brief on solar", planner, workers, lambda t, o: (False, "no"), max_rounds=3)
        self.assertEqual((r["accepted"], r["rounds"]), (False, 3))

    def test_dependency_order(self):
        p = lambda t, f: [{"id": "z", "type": "w", "input": 1, "deps": ["y"]}, {"id": "y", "type": "w", "input": 2, "deps": []}]
        seen = []
        ws = {"w": lambda inp, deps: seen.append(inp) or inp}
        S.orchestrate("t", p, ws, lambda t, o: (True, ""))
        self.assertEqual(seen, [2, 1])

    def test_unknown_worker(self):
        p = lambda t, f: [{"id": "x", "type": "ghost", "input": None, "deps": []}]
        r = S.orchestrate("t", p, {}, lambda t, o: (True, ""), max_rounds=1)
        self.assertFalse(r["accepted"])
        self.assertIn("round 1: error x: unknown worker 'ghost'", r["log"])

    def test_worker_exception(self):
        p = lambda t, f: [{"id": "x", "type": "w", "input": 0, "deps": []}]
        r = S.orchestrate("t", p, {"w": lambda i, d: 1 / i}, lambda t, o: (True, ""), max_rounds=1)
        self.assertIn("round 1: error x: ZeroDivisionError: division by zero", r["log"])

    def test_cycle(self):
        p = lambda t, f: [{"id": "a", "type": "w", "input": 0, "deps": ["b"]}, {"id": "b", "type": "w", "input": 0, "deps": ["a"]}]
        with self.assertRaises(ValueError):
            S.orchestrate("t", p, {"w": lambda i, d: i}, lambda t, o: (True, ""))


if __name__ == "__main__":
    unittest.main()
