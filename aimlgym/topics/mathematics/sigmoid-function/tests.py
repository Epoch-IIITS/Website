"""Tests for MA-03 The Sigmoid Function.

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


class TestSigmoid(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(S.sigmoid(0), 0.5)
        self.assertAlmostEqual(S.sigmoid(2), 1 / (1 + math.exp(-2)))

    def test_symmetry(self):
        for x in (-5.0, -0.3, 0.7, 4.0):
            self.assertAlmostEqual(S.sigmoid(-x), 1 - S.sigmoid(x))

    def test_extremes_no_overflow(self):
        self.assertEqual(S.sigmoid(1000), 1.0)
        self.assertEqual(S.sigmoid(-1000), 0.0)
        self.assertGreater(S.sigmoid(-30), 0.0)

    def test_derivative(self):
        self.assertAlmostEqual(S.sigmoid_derivative(0), 0.25)
        h = 1e-6
        for x in (-3.0, 0.5, 2.0):
            numeric = (S.sigmoid(x + h) - S.sigmoid(x - h)) / (2 * h)
            self.assertAlmostEqual(S.sigmoid_derivative(x), numeric, places=8)

    def test_logit_inverse(self):
        self.assertAlmostEqual(S.logit(0.5), 0.0)
        for p in (0.01, 0.3, 0.9):
            self.assertAlmostEqual(S.sigmoid(S.logit(p)), p)

    def test_logit_domain(self):
        for bad in (0, 1, -0.2, 1.5):
            with self.assertRaises(ValueError):
                S.logit(bad)


try:
    import scipy.special as _special
except ImportError:
    _special = None


class TestAgainstLibrary(unittest.TestCase):
    @unittest.skipIf(_special is None, "SciPy not installed")
    def test_matches_scipy(self):
        for x in (-50.0, -1.0, 0.0, 3.5, 40.0):
            self.assertAlmostEqual(S.sigmoid(x), float(_special.expit(x)), places=12)
        for p in (0.1, 0.5, 0.75):
            self.assertAlmostEqual(S.logit(p), float(_special.logit(p)), places=12)


if __name__ == "__main__":
    unittest.main()
