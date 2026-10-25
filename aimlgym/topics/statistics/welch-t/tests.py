"""Tests for ST-18 Welch's t-statistic by Hand.

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


class TestWelch(unittest.TestCase):
    def test_symmetric_example(self):
        t, df = S.welch_t([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
        self.assertAlmostEqual(t, -2.0)
        self.assertAlmostEqual(df, 8.0)

    def test_unequal(self):
        t, df = S.welch_t([10, 12, 14], [1, 2, 3, 4, 5, 6])
        vx, vy = 4 / 3, 3.5 / 6
        self.assertAlmostEqual(t, 8.5 / math.sqrt(vx + vy), places=10)
        self.assertAlmostEqual(df, (vx + vy) ** 2 / (vx ** 2 / 2 + vy ** 2 / 5), places=10)

    def test_antisymmetric(self):
        a, b = [2.0, 3.5, 4.0, 1.0], [5.0, 6.5, 4.5]
        t1, d1 = S.welch_t(a, b)
        t2, d2 = S.welch_t(b, a)
        self.assertAlmostEqual(t1, -t2)
        self.assertAlmostEqual(d1, d2)

    def test_same_means(self):
        t, _ = S.welch_t([1, 2, 3], [0, 2, 4])
        self.assertAlmostEqual(t, 0.0)

    def test_too_small(self):
        with self.assertRaises(ValueError):
            S.welch_t([1], [2, 3])

    def test_zero_variance(self):
        with self.assertRaises(ValueError):
            S.welch_t([2, 2], [2, 2])

    def test_one_zero_variance_ok(self):
        t, df = S.welch_t([5, 5, 5], [1, 2, 3])
        self.assertAlmostEqual(t, 3 / math.sqrt(1 / 3))
        self.assertAlmostEqual(df, 2.0)


try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_scipy_welch(self):
        from scipy.stats import ttest_ind
        x = [5.1, 4.9, 6.2, 5.8, 6.0, 5.5]
        y = [4.1, 4.4, 3.9, 4.8, 5.0]
        t, df = S.welch_t(x, y)
        ref = ttest_ind(x, y, equal_var=False)
        self.assertAlmostEqual(t, float(ref.statistic), places=10)
        if hasattr(ref, "df"):
            self.assertAlmostEqual(df, float(ref.df), places=8)


if __name__ == "__main__":
    unittest.main()
