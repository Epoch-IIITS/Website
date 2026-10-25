"""Tests for AG-13 Dependency-Ordered Plans.

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


DEPS = {"data": set(), "outline": set(), "charts": {"data"}, "report": {"data", "charts", "outline"}}

class TestDAG(unittest.TestCase):
    def test_order(self):
        self.assertEqual(S.topo_order(DEPS), ["data", "charts", "outline", "report"])

    def test_stages(self):
        self.assertEqual(S.stages(DEPS), [["data", "outline"], ["charts"], ["report"]])

    def test_respects_deps(self):
        deps = {"a": {"c"}, "b": {"a"}, "c": set(), "d": {"b", "c"}, "e": set()}
        order = S.topo_order(deps)
        pos = {t: i for i, t in enumerate(order)}
        self.assertTrue(all(pos[d] < pos[t] for t in deps for d in deps[t]))

    def test_cycle(self):
        with self.assertRaises(ValueError):
            S.topo_order({"a": {"b"}, "b": {"a"}})
        with self.assertRaises(ValueError):
            S.stages({"a": {"a"}})

    def test_unknown_dep(self):
        with self.assertRaises(ValueError):
            S.topo_order({"a": {"zzz"}})

    def test_independent(self):
        self.assertEqual(S.stages({"z": set(), "y": set()}), [["y", "z"]])

    def test_empty(self):
        self.assertEqual((S.topo_order({}), S.stages({})), ([], []))


if __name__ == "__main__":
    unittest.main()
