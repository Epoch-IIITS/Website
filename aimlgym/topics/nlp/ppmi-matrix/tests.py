"""Tests for NL-17 PPMI Co-occurrence Matrix.

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

V = {"a": 0, "b": 1, "c": 2}

class TestPPMI(unittest.TestCase):
    def test_counts(self):
        C = S.cooccurrence([["a", "b"], ["a", "c"]], V, window=1)
        np.testing.assert_array_equal(C, [[0, 1, 1], [1, 0, 0], [1, 0, 0]])

    def test_window(self):
        C = S.cooccurrence([["a", "b", "c"]], V, window=1)
        self.assertEqual(C[0, 2], 0)
        self.assertEqual(S.cooccurrence([["a", "b", "c"]], V, window=2)[0, 2], 1)

    def test_oov_positions(self):
        C = S.cooccurrence([["a", "zzz", "c"]], V, window=1)
        self.assertEqual(C.sum(), 0)

    def test_symmetric(self):
        C = S.cooccurrence([["a", "b", "a", "c", "b"]], V, window=2)
        np.testing.assert_array_equal(C, C.T)

    def test_ppmi_value(self):
        P = S.ppmi(S.cooccurrence([["a", "b"], ["a", "c"]], V, window=1))
        self.assertAlmostEqual(P[0, 1], 1.0)
        self.assertEqual(P[1, 2], 0.0)

    def test_ppmi_nonneg_finite(self):
        rng = np.random.default_rng(0)
        C = rng.integers(0, 5, (6, 6))
        P = S.ppmi(C)
        self.assertTrue(np.isfinite(P).all() and (P >= 0).all())
        self.assertTrue((P[C == 0] == 0).all())

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.ppmi(np.zeros((2, 2)))
        with self.assertRaises(ValueError):
            S.cooccurrence([["a"]], V, window=0)


if __name__ == "__main__":
    unittest.main()
