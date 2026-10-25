"""Tests for AG-07 LangGraph Basics: State, Nodes and Edges.

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


from langgraph.errors import GraphRecursionError


class TestCleanerGraph(unittest.TestCase):
    def test_worked_example(self):
        out = S.build_cleaner(3).invoke({"text": "  The Quick Brown Fox Jumps  ", "steps": []})
        self.assertEqual(out["text"], "the quick brown")
        self.assertEqual(out["steps"], ["strip", "lower", "shorten", "shorten"])

    def test_short_text_skips_loop(self):
        out = S.build_cleaner(5).invoke({"text": " Hi There ", "steps": []})
        self.assertEqual((out["text"], out["steps"]), ("hi there", ["strip", "lower"]))

    def test_reducer_keeps_existing_steps(self):
        out = S.build_cleaner(5).invoke({"text": "a", "steps": ["start"]})
        self.assertEqual(out["steps"], ["start", "strip", "lower"])

    def test_nodes(self):
        nodes = set(S.build_cleaner(2).get_graph().nodes)
        self.assertTrue({"strip", "lower", "check", "shorten"} <= nodes)

    def test_recursion_limit(self):
        app = S.build_cleaner(1)
        with self.assertRaises(GraphRecursionError):
            app.invoke({"text": " ".join(["w"] * 40), "steps": []}, {"recursion_limit": 10})

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.build_cleaner(0)


if __name__ == "__main__":
    unittest.main()
