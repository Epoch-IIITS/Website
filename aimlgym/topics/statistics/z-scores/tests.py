"""Tests for ST-05 Standardize to z-scores.

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


class TestZ(unittest.TestCase):
    def test_example(self):
        z = S.z_scores([2, 4, 4, 4, 5, 5, 7, 9])
        exp = [-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]
        for a, b in zip(z, exp):
            self.assertAlmostEqual(a, b)

    def test_mean_zero_sd_one(self):
        z = S.z_scores([3.0, -1.0, 8.5, 0.25, 4.0])
        self.assertAlmostEqual(sum(z) / len(z), 0.0, places=12)
        self.assertAlmostEqual(math.sqrt(sum(t * t for t in z) / len(z)), 1.0, places=12)

    def test_sample_variant(self):
        z = S.z_scores([1, 2, 3], sample=True)
        self.assertAlmostEqual(z[0], -1.0)

    def test_constant(self):
        with self.assertRaises(ValueError):
            S.z_scores([5, 5, 5])

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.z_scores([])

    def test_outliers(self):
        self.assertEqual(S.outliers([10, 11, 9, 10, 50], threshold=1.5), [4])

    def test_no_outliers_default(self):
        self.assertEqual(S.outliers([1, 2, 3, 4, 5]), [])


if __name__ == "__main__":
    unittest.main()
