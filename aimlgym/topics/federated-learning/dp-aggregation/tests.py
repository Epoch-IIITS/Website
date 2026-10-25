"""Tests for FL-13 Differentially Private Aggregation.

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

class TestDP(unittest.TestCase):
    def test_no_noise(self):
        noisy, clean, s = S.dp_mean([np.array([3., 4.]), np.array([0.3, 0.4])], 1.0, 0.0, np.random.default_rng(0))
        np.testing.assert_allclose(clean, [0.45, 0.6])
        np.testing.assert_allclose(noisy, clean)
        self.assertEqual(s, 0.0)

    def test_sigma(self):
        _, _, s = S.dp_mean([np.ones(3)] * 4, 2.0, 1.5, np.random.default_rng(0))
        self.assertAlmostEqual(s, 1.5 * 2.0 / 4)

    def test_noise_recipe(self):
        ds = [np.array([1., 0.]), np.array([0., 1.])]
        noisy, clean, s = S.dp_mean(ds, 5.0, 1.0, np.random.default_rng(3))
        np.testing.assert_allclose(noisy, clean + np.random.default_rng(3).normal(0, s, size=2))

    def test_noise_statistics(self):
        rng = np.random.default_rng(1)
        ds = [np.zeros(20000)] * 10
        noisy, _, s = S.dp_mean(ds, 1.0, 2.0, rng)
        self.assertAlmostEqual(noisy.std(), s, delta=0.01 * s * 5)
        self.assertAlmostEqual(noisy.mean(), 0.0, delta=0.01)

    def test_sensitivity_bound(self):
        rng = np.random.default_rng(2)
        ds = [rng.normal(size=5) * 3 for _ in range(6)]
        _, a, _ = S.dp_mean(ds, 1.0, 0.0, rng)
        _, b, _ = S.dp_mean(ds[:-1] + [rng.normal(size=5) * 50], 1.0, 0.0, rng)
        self.assertLessEqual(np.linalg.norm(a - b), 2 * 1.0 / 6 + 1e-12)

    def test_more_noise_more_error(self):
        ds = [np.array([0.5, 0.5])] * 5
        errs = []
        for z in (0.1, 1.0, 10.0):
            e = [np.linalg.norm(S.dp_mean(ds, 1.0, z, np.random.default_rng(r))[0] - 0.5) for r in range(200)]
            errs.append(np.mean(e))
        self.assertTrue(errs[0] < errs[1] < errs[2])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.dp_mean([], 1.0, 1.0, np.random.default_rng(0))


if __name__ == "__main__":
    unittest.main()
