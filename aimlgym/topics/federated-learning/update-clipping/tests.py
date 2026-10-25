"""Tests for FL-09 Clipping Client Updates.

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

class TestClip(unittest.TestCase):
    def test_clip(self):
        np.testing.assert_allclose(S.clip_update(np.array([3., 4.]), 2.5), [1.5, 2.0])

    def test_unchanged(self):
        np.testing.assert_allclose(S.clip_update(np.array([0.3, 0.4]), 2.5), [0.3, 0.4])

    def test_zero(self):
        np.testing.assert_array_equal(S.clip_update(np.zeros(3), 1.0), np.zeros(3))

    def test_norm_and_direction(self):
        d = np.random.default_rng(0).normal(size=10) * 10
        c = S.clip_update(d, 1.0)
        self.assertAlmostEqual(np.linalg.norm(c), 1.0)
        self.assertAlmostEqual(c @ d / (np.linalg.norm(c) * np.linalg.norm(d)), 1.0)

    def test_clip_all(self):
        cl, n = S.clip_all([np.array([3., 4.]), np.array([0.3, 0.4]), np.array([0., 10.])], 2.5)
        self.assertEqual(n, 2)
        self.assertTrue(all(np.linalg.norm(c) <= 2.5 + 1e-12 for c in cl))

    def test_sensitivity(self):
        rng = np.random.default_rng(1)
        ds = [rng.normal(size=4) * 5 for _ in range(5)]
        a = sum(S.clip_all(ds, 1.0)[0])
        ds2 = ds[:-1] + [rng.normal(size=4) * 100]
        b = sum(S.clip_all(ds2, 1.0)[0])
        self.assertLessEqual(np.linalg.norm(a - b), 2.0 + 1e-12)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.clip_update(np.ones(2), 0)


if __name__ == "__main__":
    unittest.main()
