"""Tests for AG-05 Goal Tests and Step Budgets.

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


INC = (lambda s: "inc", lambda s, a: (s + 1, 1.0), lambda s: s >= 3)

class TestBudget(unittest.TestCase):
    def test_success(self):
        r = S.run_with_budget(0, *INC, max_steps=5)
        self.assertEqual((r["status"], r["state"], r["actions"], r["cost"]), ("success", 3, ["inc"] * 3, 3.0))

    def test_step_limit(self):
        r = S.run_with_budget(0, *INC, max_steps=2)
        self.assertEqual((r["status"], r["state"]), ("step_limit", 2))

    def test_success_on_last_step(self):
        self.assertEqual(S.run_with_budget(0, *INC, max_steps=3)["status"], "success")

    def test_cost_exceeded(self):
        r = S.run_with_budget(0, *INC, max_steps=10, max_cost=1.5)
        self.assertEqual((r["status"], r["state"], r["cost"]), ("cost_exceeded", 2, 2.0))

    def test_already_done(self):
        r = S.run_with_budget(5, *INC, max_steps=10)
        self.assertEqual((r["status"], r["actions"], r["cost"]), ("success", [], 0.0))

    def test_zero_steps(self):
        self.assertEqual(S.run_with_budget(0, *INC, max_steps=0)["status"], "step_limit")

    def test_exact_budget_ok(self):
        self.assertEqual(S.run_with_budget(0, *INC, max_steps=10, max_cost=3.0)["status"], "success")


if __name__ == "__main__":
    unittest.main()
