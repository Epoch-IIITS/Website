"""Tests for AG-20 Evaluating Agents.

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


TASKS = [
    {"id": "add", "input": "2+3", "expected": "5", "max_tool_calls": 1},
    {"id": "capital", "input": "capital of France", "expected": "Paris", "forbidden_tools": ["rm", "web"]},
    {"id": "crash", "input": "boom", "expected": "x"},
    {"id": "slow", "input": "think", "expected": "done", "max_tool_calls": 2},
]


def agent_v1(question):
    if question == "2+3":
        return {"status": "final", "answer": " 5. ", "tool_calls": 1, "tools_used": ["calculator"]}
    if question == "capital of France":
        return {"status": "final", "answer": "PARIS!", "tool_calls": 2, "tools_used": ["web", "rm", "search"]}
    if question == "boom":
        raise KeyError("missing")
    return {"status": "step_limit", "answer": None, "tool_calls": 5, "tools_used": []}


def agent_v2(question):
    if question == "2+3":
        return {"status": "final", "answer": "6", "tool_calls": 1, "tools_used": []}
    if question == "capital of France":
        return {"status": "final", "answer": "Paris", "tool_calls": 1, "tools_used": ["search"]}
    if question == "boom":
        return {"status": "final", "answer": "x", "tool_calls": 0, "tools_used": []}
    return {"status": "final", "answer": "Done", "tool_calls": 2, "tools_used": []}


class TestAgentEvaluation(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(S.normalize_answer("  The   Answer is 5.!  "), "the answer is 5")
        self.assertEqual(S.normalize_answer(None), "")
        self.assertEqual(S.normalize_answer("3.5"), "3.5")

    def test_reasons(self):
        report = S.evaluate(agent_v1, TASKS)
        reasons = {r["id"]: r["reasons"] for r in report["results"]}
        self.assertEqual(reasons["add"], [])
        self.assertEqual(reasons["capital"], ["forbidden tool: rm", "forbidden tool: web"])
        self.assertEqual(reasons["crash"], ["error: KeyError"])
        self.assertEqual(reasons["slow"], ["not final", "wrong answer", "over budget"])

    def test_summary(self):
        report = S.evaluate(agent_v1, TASKS)
        self.assertEqual([r["id"] for r in report["results"]], ["add", "capital", "crash", "slow"])
        self.assertEqual(report["pass_rate"], 0.25)
        self.assertAlmostEqual(report["mean_tool_calls"], (1 + 2 + 5) / 3)

    def test_calls_agent_once_per_task(self):
        calls = []
        def agent(q):
            calls.append(q)
            return agent_v2(q)
        S.evaluate(agent, TASKS)
        self.assertEqual(calls, [t["input"] for t in TASKS])

    def test_empty(self):
        self.assertEqual(S.evaluate(agent_v1, []), {"results": [], "pass_rate": 0.0, "mean_tool_calls": 0.0})

    def test_regressions(self):
        old, new = S.evaluate(agent_v1, TASKS), S.evaluate(agent_v2, TASKS)
        self.assertEqual(new["pass_rate"], 0.75)
        self.assertEqual(S.regressions(old, new), ["add"])
        self.assertEqual(S.regressions(new, old), ["capital", "crash", "slow"])
        self.assertEqual(S.regressions(new, {"results": []}), ["capital", "crash", "slow"])


if __name__ == "__main__":
    unittest.main()
