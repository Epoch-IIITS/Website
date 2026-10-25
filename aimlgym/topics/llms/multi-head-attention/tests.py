"""Tests for LM-10 Multi-Head Attention.

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

def single_head(Q, K, V, causal=False):
    s = Q @ K.T / np.sqrt(Q.shape[1])
    if causal:
        s = np.where(np.tril(np.ones(s.shape, bool)), s, -np.inf)
    w = np.exp(s - s.max(1, keepdims=True)); w /= w.sum(1, keepdims=True)
    return w @ V

class TestMHA(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(0)
        self.X = rng.normal(size=(5, 8))
        self.W = [rng.normal(size=(8, 8)) / 3 for _ in range(4)]

    def test_split(self):
        X = np.arange(8.).reshape(2, 4)
        np.testing.assert_array_equal(S.split_heads(X, 2)[1], [[2., 3.], [6., 7.]])
        self.assertEqual(S.split_heads(X, 2).shape, (2, 2, 2))

    def test_roundtrip(self):
        np.testing.assert_array_equal(S.merge_heads(S.split_heads(self.X, 4)), self.X)

    def test_h1_equals_single(self):
        Wq, Wk, Wv, Wo = self.W
        exp = single_head(self.X @ Wq, self.X @ Wk, self.X @ Wv) @ Wo
        np.testing.assert_allclose(S.multi_head_attention(self.X, Wq, Wk, Wv, Wo, 1), exp)

    def test_h2_manual(self):
        Wq, Wk, Wv, Wo = self.W
        Q, K, V = self.X @ Wq, self.X @ Wk, self.X @ Wv
        heads = [single_head(Q[:, i*4:(i+1)*4], K[:, i*4:(i+1)*4], V[:, i*4:(i+1)*4]) for i in range(2)]
        np.testing.assert_allclose(S.multi_head_attention(self.X, Wq, Wk, Wv, Wo, 2), np.hstack(heads) @ Wo)

    def test_causal(self):
        Wq, Wk, Wv, Wo = self.W
        out = S.multi_head_attention(self.X, Wq, Wk, Wv, Wo, 2, causal=True)
        X2 = self.X.copy(); X2[-1] += 5
        out2 = S.multi_head_attention(X2, Wq, Wk, Wv, Wo, 2, causal=True)
        np.testing.assert_allclose(out[:-1], out2[:-1])

    def test_shape(self):
        self.assertEqual(S.multi_head_attention(self.X, *self.W, h=4).shape, (5, 8))

    def test_bad_heads(self):
        with self.assertRaises(ValueError):
            S.split_heads(self.X, 3)


if __name__ == "__main__":
    unittest.main()
