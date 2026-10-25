"""Tests for XA-03 Tracing a Decision Path.

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


TREE = {"feature": 0, "threshold": 30, "left": {"feature": 1, "threshold": 5,
        "left": {"value": "approve"}, "right": {"value": "reject"}}, "right": {"value": "approve"}}
NAMES = ["income", "debt"]

class TestPath(unittest.TestCase):
    def test_reject(self):
        self.assertEqual(S.predict_with_path(TREE, [25, 8], NAMES), ("reject", ["income <= 30", "debt > 5"]))

    def test_right_branch(self):
        self.assertEqual(S.predict_with_path(TREE, [31, 100], NAMES), ("approve", ["income > 30"]))

    def test_boundary_left(self):
        self.assertEqual(S.predict_with_path(TREE, [30, 5], NAMES)[1], ["income <= 30", "debt <= 5"])

    def test_leaf_root(self):
        self.assertEqual(S.predict_with_path({"value": 1.5}, [0], ["a"]), (1.5, []))

    def test_float_threshold(self):
        t = {"feature": 0, "threshold": 2.5, "left": {"value": 0}, "right": {"value": 1}}
        self.assertEqual(S.predict_with_path(t, [3.0], ["x"]), (1, ["x > 2.5"]))

    def test_malformed(self):
        with self.assertRaises(ValueError):
            S.predict_with_path({"feature": 0, "left": {"value": 1}}, [0], ["a"])

    def test_tree_unchanged(self):
        import copy
        t = copy.deepcopy(TREE)
        S.predict_with_path(t, [25, 1], NAMES)
        self.assertEqual(t, TREE)


if __name__ == "__main__":
    unittest.main()
