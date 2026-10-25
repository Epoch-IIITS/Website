"""Tests for MA-02 Exponentials and Logarithms.

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


class TestExpLog(unittest.TestCase):
    def test_log_base(self):
        self.assertAlmostEqual(S.log_base(8, 2), 3.0)
        self.assertAlmostEqual(S.log_base(1000, 10), 3.0)
        self.assertAlmostEqual(S.log_base(1, 7), 0.0)

    def test_doubling_time(self):
        self.assertAlmostEqual(S.doubling_time(1.0), 1.0)
        self.assertAlmostEqual(S.doubling_time(0.07), 10.244768351058712, places=9)

    def test_log_likelihood_small(self):
        self.assertAlmostEqual(S.log_likelihood([0.5, 0.25]), math.log(0.125))
        self.assertEqual(S.log_likelihood([]), 0.0)

    def test_log_likelihood_no_underflow(self):
        probs = [1e-5] * 1000
        self.assertEqual(math.prod(probs), 0.0)
        self.assertAlmostEqual(S.log_likelihood(probs), 1000 * math.log(1e-5), places=6)

    def test_log_likelihood_validates(self):
        for bad in ([0.5, 0.0], [1.5], [-0.1]):
            with self.assertRaises(ValueError):
                S.log_likelihood(bad)

    def test_logsumexp_small(self):
        v = [0.1, -2.0, 1.5]
        self.assertAlmostEqual(S.logsumexp(v), math.log(sum(math.exp(x) for x in v)))

    def test_logsumexp_large_and_negative(self):
        self.assertAlmostEqual(S.logsumexp([1000, 1000]), 1000 + math.log(2))
        self.assertAlmostEqual(S.logsumexp([-1000, -1000]), -1000 + math.log(2))
        with self.assertRaises(ValueError):
            S.logsumexp([])


try:
    import scipy.special as _special
except ImportError:
    _special = None


class TestAgainstLibrary(unittest.TestCase):
    def test_log_base_matches_math(self):
        for x, b in [(8, 2), (81, 3), (0.5, 10)]:
            self.assertAlmostEqual(S.log_base(x, b), math.log(x, b), places=12)

    def test_doubling_uses_same_value_as_log1p(self):
        self.assertAlmostEqual(S.doubling_time(1e-6), math.log(2) / math.log1p(1e-6), delta=1e-3)

    @unittest.skipIf(_special is None, "SciPy not installed")
    def test_logsumexp_matches_scipy(self):
        v = [3.0, -1.0, 700.0, 699.5]
        self.assertAlmostEqual(S.logsumexp(v), float(_special.logsumexp(v)), places=9)


if __name__ == "__main__":
    unittest.main()
