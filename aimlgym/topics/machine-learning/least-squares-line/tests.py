"""Tests for ML-09 Least-Squares Line.

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

class TestOLS(unittest.TestCase):
    def test_fit(self):
        m = S.SimpleLinearRegression().fit([1, 2, 3, 4], [2, 4, 5, 8])
        self.assertAlmostEqual(m.slope_, 1.9)
        self.assertAlmostEqual(m.intercept_, 0.0)

    def test_predict(self):
        m = S.SimpleLinearRegression().fit([1, 2, 3, 4], [2, 4, 5, 8])
        np.testing.assert_allclose(m.predict([5]), [9.5])

    def test_through_means(self):
        x, y = np.array([0.5, 2, 3.5, 7]), np.array([1, 0, 4, 2.5])
        m = S.SimpleLinearRegression().fit(x, y)
        self.assertAlmostEqual(m.predict([x.mean()])[0], y.mean())

    def test_matches_polyfit(self):
        rng = np.random.default_rng(1)
        x = rng.uniform(0, 10, 50); y = 3 - 0.7 * x + rng.normal(0, 0.5, 50)
        m = S.SimpleLinearRegression().fit(x, y)
        slope, inter = np.polyfit(x, y, 1)
        self.assertAlmostEqual(m.slope_, slope, places=10)
        self.assertAlmostEqual(m.intercept_, inter, places=10)

    def test_score_perfect(self):
        self.assertAlmostEqual(S.SimpleLinearRegression().fit([0, 1, 2], [1, 3, 5]).score([0, 1, 2], [1, 3, 5]), 1.0)

    def test_constant_x(self):
        with self.assertRaises(ValueError):
            S.SimpleLinearRegression().fit([2, 2, 2], [1, 2, 3])

    def test_not_fitted(self):
        with self.assertRaises(RuntimeError):
            S.SimpleLinearRegression().predict([1])


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_polyfit(self):
        import numpy as np
        x = np.array([1.0, 2.0, 3.0, 5.0, 8.0])
        y = np.array([2.2, 2.8, 4.1, 6.2, 9.9])
        m = S.SimpleLinearRegression().fit(x, y)
        slope, intercept = np.polyfit(x, y, 1)
        self.assertAlmostEqual(m.slope_, slope, places=10)
        self.assertAlmostEqual(m.intercept_, intercept, places=10)

    @unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
    def test_library_matches_sklearn(self):
        import numpy as np
        from sklearn.linear_model import LinearRegression
        x = np.array([1.0, 2.0, 3.0, 5.0, 8.0])
        y = np.array([2.2, 2.8, 4.1, 6.2, 9.9])
        sk = LinearRegression().fit(x.reshape(-1, 1), y)
        m = S.SimpleLinearRegression().fit(x, y)
        self.assertAlmostEqual(m.score(x, y), sk.score(x.reshape(-1, 1), y), places=10)


if __name__ == "__main__":
    unittest.main()
