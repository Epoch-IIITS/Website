"""Tests for RL-06 Incremental Value Estimates.

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


import numpy as np

class TestIncremental(unittest.TestCase):
    def test_sample_average(self):
        v = S.ValueEstimates(2)
        self.assertEqual([v.update(0, r) for r in (2, 4, 6)], [2.0, 3.0, 4.0])
        self.assertEqual(v.n.tolist(), [3, 0])

    def test_constant_alpha(self):
        w = S.ValueEstimates(1, alpha=0.5)
        self.assertEqual([w.update(0, r) for r in (2, 4, 6)], [1.0, 2.5, 4.25])

    def test_equals_mean(self):
        rng = np.random.default_rng(0)
        rs = rng.normal(size=500)
        v = S.ValueEstimates(1)
        for r in rs:
            v.update(0, r)
        self.assertAlmostEqual(v.q[0], rs.mean(), places=10)

    def test_tracks_change(self):
        a, b = S.ValueEstimates(1), S.ValueEstimates(1, alpha=0.1)
        for r in [0.0] * 500 + [10.0] * 100:
            a.update(0, r); b.update(0, r)
        self.assertGreater(b.q[0], 9.0)
        self.assertLess(a.q[0], 2.0)

    def test_independent_arms(self):
        v = S.ValueEstimates(3)
        v.update(2, 5.0)
        self.assertEqual(v.q.tolist(), [0.0, 0.0, 5.0])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.ValueEstimates(2).update(2, 1.0)
        with self.assertRaises(ValueError):
            S.ValueEstimates(2, alpha=0.0)


if __name__ == "__main__":
    unittest.main()
