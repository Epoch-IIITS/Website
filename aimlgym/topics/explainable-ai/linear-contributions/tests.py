"""Tests for XA-01 Linear Model Contributions.

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

class TestLinearContrib(unittest.TestCase):
    def test_example(self):
        r = S.contributions(np.array([2., -1.]), 5.0, np.array([3., 4.]), np.array([1., 1.]))
        np.testing.assert_allclose(r["phi"], [4., -3.])
        self.assertEqual((r["prediction"], r["baseline_prediction"]), (7.0, 6.0))

    def test_efficiency(self):
        rng = np.random.default_rng(0)
        w, x, base = rng.normal(size=6), rng.normal(size=6), rng.normal(size=6)
        r = S.contributions(w, 0.3, x, base)
        self.assertAlmostEqual(r["phi"].sum(), r["prediction"] - r["baseline_prediction"])

    def test_at_baseline_zero(self):
        r = S.contributions(np.array([1., 2.]), 0.0, np.array([5., 5.]), np.array([5., 5.]))
        np.testing.assert_allclose(r["phi"], 0)

    def test_zero_weight_zero_contrib(self):
        r = S.contributions(np.array([0., 3.]), 0.0, np.array([100., 1.]), np.array([0., 0.]))
        self.assertEqual(r["phi"][0], 0.0)

    def test_baseline_matters(self):
        w, x = np.array([1.0]), np.array([10.0])
        a = S.contributions(w, 0, x, np.array([0.0]))["phi"][0]
        b = S.contributions(w, 0, x, np.array([9.0]))["phi"][0]
        self.assertNotEqual(a, b)

    def test_mismatch(self):
        with self.assertRaises(ValueError):
            S.contributions(np.ones(2), 0, np.ones(3), np.ones(2))


if __name__ == "__main__":
    unittest.main()
