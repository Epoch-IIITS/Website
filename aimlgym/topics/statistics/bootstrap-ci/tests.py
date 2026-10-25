"""Tests for ST-13 Bootstrap Confidence Interval.

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


import random
import statistics

def _ref(data, n_boot, alpha, seed):
    rng = random.Random(seed)
    n = len(data)
    b = sorted(sum(data[int(rng.random() * n)] for _ in range(n)) / n for _ in range(n_boot))
    def pct(q):
        r = q / 100 * (len(b) - 1); i = math.floor(r); f = r - i
        return b[i] + f * (b[i + 1] - b[i]) if i + 1 < len(b) else b[i]
    return pct(100 * alpha / 2), pct(100 * (1 - alpha / 2))

DATA = [2, 4, 4, 5, 7, 9]

class TestBootstrap(unittest.TestCase):
    def test_contains_mean(self):
        lo, hi = S.bootstrap_ci(DATA, seed=0)
        self.assertLess(lo, sum(DATA) / 6)
        self.assertGreater(hi, sum(DATA) / 6)

    def test_exact_recipe(self):
        got = S.bootstrap_ci(DATA, n_boot=500, alpha=0.1, seed=3)
        exp = _ref(DATA, 500, 0.1, 3)
        self.assertAlmostEqual(got[0], exp[0], places=12)
        self.assertAlmostEqual(got[1], exp[1], places=12)

    def test_constant(self):
        self.assertEqual(S.bootstrap_ci([5, 5, 5], seed=1), (5.0, 5.0))

    def test_reproducible(self):
        self.assertEqual(S.bootstrap_ci(DATA, seed=11), S.bootstrap_ci(DATA, seed=11))

    def test_wider_at_higher_confidence(self):
        lo90, hi90 = S.bootstrap_ci(DATA, alpha=0.10, seed=4)
        lo99, hi99 = S.bootstrap_ci(DATA, alpha=0.01, seed=4)
        self.assertLessEqual(lo99, lo90)
        self.assertGreaterEqual(hi99, hi90)

    def test_custom_stat(self):
        lo, hi = S.bootstrap_ci(DATA, seed=2, stat=statistics.median)
        self.assertTrue(lo <= 4.5 <= hi)

    def test_bad_args(self):
        with self.assertRaises(ValueError):
            S.bootstrap_ci([], seed=0)
        with self.assertRaises(ValueError):
            S.bootstrap_ci(DATA, alpha=1.0)


try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_close_to_scipy_bootstrap(self):
        import numpy as np
        from scipy.stats import bootstrap
        data = [2.3, 3.1, 4.8, 5.0, 5.5, 6.1, 7.4, 8.0, 9.2, 10.5, 3.3, 4.4]
        lo, hi = S.bootstrap_ci(data, n_boot=4000, seed=1)
        ref = bootstrap((np.array(data),), np.mean, n_resamples=4000, method="percentile",
                        random_state=np.random.default_rng(1)).confidence_interval
        self.assertAlmostEqual(lo, ref.low, delta=0.35)
        self.assertAlmostEqual(hi, ref.high, delta=0.35)


if __name__ == "__main__":
    unittest.main()
