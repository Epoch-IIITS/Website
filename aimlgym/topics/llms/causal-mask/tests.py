"""Tests for LM-08 Causal Masking.

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

T_, F_ = True, False

def attn(Q, K, V, mask):
    s = Q @ K.T / np.sqrt(Q.shape[1]); s = np.where(mask, s, -np.inf)
    w = np.exp(s - s.max(1, keepdims=True)); w /= w.sum(1, keepdims=True); return w @ V

class TestMasks(unittest.TestCase):
    def test_causal(self):
        np.testing.assert_array_equal(S.causal_mask(3), [[T_, F_, F_], [T_, T_, F_], [T_, T_, T_]])

    def test_padding(self):
        np.testing.assert_array_equal(S.padding_mask([2, 3], 3), [[T_, T_, F_], [T_, T_, T_]])

    def test_combined(self):
        np.testing.assert_array_equal(S.combined_mask([2], 3)[0], [[T_, F_, F_], [T_, T_, F_], [T_, T_, T_]])
        np.testing.assert_array_equal(S.combined_mask([1], 3)[0], [[T_, F_, F_], [T_, T_, F_], [T_, F_, T_]])

    def test_combined_shape(self):
        self.assertEqual(S.combined_mask([1, 2, 4], 4).shape, (3, 4, 4))

    def test_no_future_leak(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(5, 4)); M = S.causal_mask(5)
        out1 = attn(X, X, X, M)
        X2 = X.copy(); X2[4] += 10.0
        out2 = attn(X2, X2, X2, M)
        np.testing.assert_allclose(out1[:4], out2[:4])

    def test_every_row_has_key(self):
        self.assertTrue(S.combined_mask([1, 3], 3).any(axis=2).all())

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.causal_mask(0)
        with self.assertRaises(ValueError):
            S.padding_mask([4], 3)


if __name__ == "__main__":
    unittest.main()
