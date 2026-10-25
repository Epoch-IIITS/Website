"""Tests for LM-15 Incremental Decoding with a KV Cache.

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

class TestKVCache(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(0)
        self.X = rng.normal(size=(7, 4))
        self.W = [rng.normal(size=(4, 4)) for _ in range(3)]

    def test_matches_full(self):
        cache = S.KVCache(*self.W)
        outs = np.array([cache.step(x) for x in self.X])
        np.testing.assert_allclose(outs, S.full_causal_attention(self.X, *self.W), atol=1e-12)

    def test_cache_growth(self):
        cache = S.KVCache(*self.W)
        self.assertEqual(cache.K.shape, (0, 4))
        for t, x in enumerate(self.X, 1):
            cache.step(x)
            self.assertEqual(cache.K.shape, (t, 4))
            self.assertEqual(cache.V.shape, (t, 4))

    def test_first_token_is_own_value(self):
        cache = S.KVCache(*self.W)
        np.testing.assert_allclose(cache.step(self.X[0]), self.X[0] @ self.W[2])

    def test_full_first_row(self):
        np.testing.assert_allclose(S.full_causal_attention(self.X, *self.W)[0], self.X[0] @ self.W[2])

    def test_full_causal_property(self):
        out1 = S.full_causal_attention(self.X, *self.W)
        X2 = self.X.copy(); X2[5:] = 0
        out2 = S.full_causal_attention(X2, *self.W)
        np.testing.assert_allclose(out1[:5], out2[:5])

    def test_cached_keys_are_projections(self):
        cache = S.KVCache(*self.W)
        for x in self.X[:3]:
            cache.step(x)
        np.testing.assert_allclose(cache.K, self.X[:3] @ self.W[1])


if __name__ == "__main__":
    unittest.main()
