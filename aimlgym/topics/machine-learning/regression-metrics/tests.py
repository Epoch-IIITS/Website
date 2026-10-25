"""Tests for ML-03 Regression Metrics.

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

class TestRegMetrics(unittest.TestCase):
    def test_example(self):
        r = S.regression_report([3, 5, 7], [2, 5, 9])
        self.assertAlmostEqual(r["mse"], 5 / 3)
        self.assertAlmostEqual(r["rmse"], np.sqrt(5 / 3))
        self.assertAlmostEqual(r["mae"], 1.0)
        self.assertAlmostEqual(r["r2"], 0.375)

    def test_perfect(self):
        r = S.regression_report([1, 2, 3], [1, 2, 3])
        self.assertEqual((r["mse"], r["r2"]), (0.0, 1.0))

    def test_mean_baseline_zero_r2(self):
        self.assertAlmostEqual(S.regression_report([1, 2, 3], [2, 2, 2])["r2"], 0.0)

    def test_negative_r2(self):
        self.assertLess(S.regression_report([1, 2, 3], [3, 2, 1])["r2"], 0)

    def test_constant_target(self):
        with self.assertRaises(ValueError):
            S.regression_report([4, 4], [4, 5])

    def test_mismatch(self):
        with self.assertRaises(ValueError):
            S.regression_report([1, 2], [1])

    def test_types(self):
        self.assertTrue(all(isinstance(v, float) for v in S.regression_report([1, 2], [1, 3]).values()))


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_metrics(self):
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        yt, yp = [3.0, -0.5, 2.0, 7.0, 4.2], [2.5, 0.0, 2.0, 8.0, 3.9]
        r = S.regression_report(yt, yp)
        self.assertAlmostEqual(r["mse"], mean_squared_error(yt, yp))
        self.assertAlmostEqual(r["mae"], mean_absolute_error(yt, yp))
        self.assertAlmostEqual(r["r2"], r2_score(yt, yp))


if __name__ == "__main__":
    unittest.main()
