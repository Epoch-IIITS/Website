"""Tests for LM-03 Logits, Temperature and Softmax.

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

Z = np.array([2., 1., 0.])

class TestTemp(unittest.TestCase):
    def test_t1(self):
        np.testing.assert_allclose(S.softmax_t(Z), np.exp(Z) / np.exp(Z).sum())

    def test_t_half(self):
        np.testing.assert_allclose(S.softmax_t(Z, 0.5), np.exp(2 * Z) / np.exp(2 * Z).sum())

    def test_low_t_greedy(self):
        p = S.softmax_t(Z, 0.01)
        self.assertAlmostEqual(p[0], 1.0, places=9)

    def test_high_t_uniform(self):
        np.testing.assert_allclose(S.softmax_t(Z, 1e6), [1 / 3] * 3, atol=1e-6)

    def test_rank_preserved(self):
        for T in (0.2, 1.0, 5.0):
            self.assertEqual(list(np.argsort(S.softmax_t(Z, T))), [2, 1, 0])

    def test_entropy(self):
        self.assertAlmostEqual(S.entropy(np.array([0.5, 0.5])), np.log(2))
        self.assertEqual(S.entropy(np.array([1.0, 0.0])), 0.0)

    def test_entropy_increases_with_t(self):
        hs = [S.entropy(S.softmax_t(Z, T)) for T in (0.3, 1.0, 3.0)]
        self.assertTrue(hs[0] < hs[1] < hs[2])

    def test_bad_t(self):
        with self.assertRaises(ValueError):
            S.softmax_t(Z, 0)


if __name__ == "__main__":
    unittest.main()
