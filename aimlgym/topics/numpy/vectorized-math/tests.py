"""Tests for NP-02 Vectorised Arithmetic and ufuncs.

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
import warnings

import numpy as np


class TestVectorized(unittest.TestCase):
    def test_dot_matches_loop(self):
        rng = random.Random(0)
        a = [rng.random() - 0.5 for _ in range(200)]
        b = [rng.random() - 0.5 for _ in range(200)]
        self.assertAlmostEqual(S.dot_vectorized(a, b), S.dot_loop(a, b), places=10)
        self.assertEqual(S.dot_vectorized([1, 2, 3], [4, 5, 6]), 32.0)
        self.assertIsInstance(S.dot_vectorized([1], [2]), float)

    def test_dot_mismatch(self):
        with self.assertRaises(ValueError):
            S.dot_vectorized([1, 2], [1, 2, 3])

    def test_fahrenheit(self):
        out = S.fahrenheit([0, 100, -40])
        self.assertIsInstance(out, np.ndarray)
        np.testing.assert_allclose(out, [32, 212, -40])

    def test_rms(self):
        self.assertAlmostEqual(S.rms([3, 4]), math.sqrt(12.5))
        self.assertAlmostEqual(S.rms(np.full(10, -2.0)), 2.0)

    def test_sigmoid_values(self):
        x = np.linspace(-6, 6, 13)
        expected = [1 / (1 + math.exp(-v)) for v in x]
        np.testing.assert_allclose(S.sigmoid(x), expected, rtol=1e-12)

    def test_sigmoid_stable(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            out = S.sigmoid([-1000.0, 0.0, 1000.0])
        np.testing.assert_allclose(out, [0.0, 0.5, 1.0])

    def test_sigmoid_shape(self):
        self.assertEqual(S.sigmoid(np.zeros((2, 3))).shape, (2, 3))


try:
    import scipy.special as _special
except ImportError:
    _special = None


class TestAgainstLibrary(unittest.TestCase):
    def test_dot_matches_np_dot(self):
        a, b = np.arange(5.0), np.linspace(-1, 1, 5)
        self.assertAlmostEqual(S.dot_vectorized(a, b), float(np.dot(a, b)), places=12)

    @unittest.skipIf(_special is None, "SciPy not installed")
    def test_sigmoid_matches_expit(self):
        x = np.linspace(-40, 40, 81)
        np.testing.assert_allclose(S.sigmoid(x), _special.expit(x), rtol=1e-12)


if __name__ == "__main__":
    unittest.main()
