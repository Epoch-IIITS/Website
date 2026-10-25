"""Tests for NP-10 Seeded Random Generators.

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

class TestSeeded(unittest.TestCase):
    def test_shapes(self):
        x, y = S.make_regression(5, seed=0)
        self.assertEqual((x.shape, y.shape), ((5,), (5,)))

    def test_reproducible(self):
        a = S.make_regression(50, seed=7)
        b = S.make_regression(50, seed=7)
        np.testing.assert_array_equal(a[0], b[0])
        np.testing.assert_array_equal(a[1], b[1])

    def test_draw_order(self):
        x, y = S.make_regression(20, seed=3, noise=0.5)
        rng = np.random.default_rng(3)
        np.testing.assert_allclose(x, rng.uniform(0, 1, 20))
        np.testing.assert_allclose(y, 2 * x + 1 + rng.normal(0, 0.5, 20))

    def test_noise_free(self):
        x, y = S.make_regression(10, seed=1, noise=0.0)
        np.testing.assert_allclose(y, 2 * x + 1)

    def test_line_recovered(self):
        x, y = S.make_regression(5000, seed=2, noise=0.1)
        slope, intercept = np.polyfit(x, y, 1)
        self.assertAlmostEqual(slope, 2.0, delta=0.02)
        self.assertAlmostEqual(intercept, 1.0, delta=0.02)

    def test_split_disjoint_cover(self):
        tr, te = S.split_indices(10, 0.3, seed=1)
        self.assertEqual((len(tr), len(te)), (7, 3))
        self.assertEqual(sorted(np.concatenate([tr, te]).tolist()), list(range(10)))

    def test_split_reproducible_and_bad(self):
        np.testing.assert_array_equal(S.split_indices(20, 0.25, 4)[1], S.split_indices(20, 0.25, 4)[1])
        with self.assertRaises(ValueError):
            S.split_indices(10, 1.0, 0)


if __name__ == "__main__":
    unittest.main()
