"""Tests for DL-02 Numerically Stable Softmax.

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


import warnings
import numpy as np

class TestSoftmax(unittest.TestCase):
    def test_basic(self):
        np.testing.assert_allclose(S.softmax(np.array([1., 2., 3.])), [0.09003057, 0.24472847, 0.66524096], rtol=1e-7)

    def test_large(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            np.testing.assert_allclose(S.softmax(np.array([1000., 1001.])), [0.26894142, 0.73105858], rtol=1e-7)

    def test_shift_invariance(self):
        z = np.array([0.3, -1.2, 2.5])
        np.testing.assert_allclose(S.softmax(z), S.softmax(z + 123.0), atol=1e-12)

    def test_rows(self):
        Z = np.array([[1., 2., 3.], [0., 0., 0.]])
        P = S.softmax(Z)
        np.testing.assert_allclose(P.sum(axis=1), [1, 1])
        np.testing.assert_allclose(P[1], [1 / 3] * 3)

    def test_axis0(self):
        Z = np.array([[1., 5.], [1., 5.]])
        np.testing.assert_allclose(S.softmax(Z, axis=0), [[0.5, 0.5], [0.5, 0.5]])

    def test_log_softmax(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            np.testing.assert_allclose(S.log_softmax(np.array([0., -1e4])), [0., -1e4], atol=1e-9)

    def test_log_consistency(self):
        z = np.array([[0.2, 1.7, -0.4], [3.0, 3.0, 1.0]])
        np.testing.assert_allclose(np.exp(S.log_softmax(z)), S.softmax(z), rtol=1e-12)


try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_scipy(self):
        import numpy as np
        from scipy.special import log_softmax, softmax
        z = np.array([[1000.0, 1001.0, 999.0], [-3.0, 0.0, 2.5]])
        np.testing.assert_allclose(S.softmax(z, axis=1), softmax(z, axis=1), atol=1e-12)
        np.testing.assert_allclose(S.log_softmax(z, axis=0), log_softmax(z, axis=0), atol=1e-12)


if __name__ == "__main__":
    unittest.main()
