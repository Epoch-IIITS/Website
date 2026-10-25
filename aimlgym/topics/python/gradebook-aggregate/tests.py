"""Tests for PY-18 Gradebook Aggregation.

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


class TestGradebook(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.gradebook([("ann", 90), ("bob", 70), ("ann", 80), ("cy", 85)]),
                         [("ann", 85.0, 2), ("cy", 85.0, 1), ("bob", 70.0, 1)])

    def test_out_of_range(self):
        self.assertEqual(S.gradebook([("x", 101), ("x", 50)]), [("x", 50.0, 1)])

    def test_only_invalid(self):
        self.assertEqual(S.gradebook([("z", -5)]), [])

    def test_empty(self):
        self.assertEqual(S.gradebook([]), [])

    def test_rounding(self):
        self.assertEqual(S.gradebook([("a", 1), ("a", 2), ("a", 2)]), [("a", 1.67, 3)])

    def test_boundaries_included(self):
        self.assertEqual(S.gradebook([("a", 0), ("b", 100)]), [("b", 100.0, 1), ("a", 0.0, 1)])

    def test_tie_alphabetical(self):
        names = [r[0] for r in S.gradebook([("d", 60), ("b", 60), ("c", 60)])]
        self.assertEqual(names, ["b", "c", "d"])


if __name__ == "__main__":
    unittest.main()
