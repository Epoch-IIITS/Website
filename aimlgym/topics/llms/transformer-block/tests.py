"""Tests for LM-12 A Pre-Norm Transformer Block by Hand.

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


def make_params(d=8, dff=16, seed=0, scale=0.3):
    rng = np.random.default_rng(seed)
    n = lambda *s: rng.normal(0, scale, s)
    return {"ln1_g": 1 + n(d), "ln1_b": n(d), "Wq": n(d, d), "Wk": n(d, d), "Wv": n(d, d), "Wo": n(d, d),
            "ln2_g": 1 + n(d), "ln2_b": n(d), "W1": n(d, dff), "b1": n(dff), "W2": n(dff, d), "b2": n(d)}


class TestTransformerBlock(unittest.TestCase):
    def test_layer_norm_stats(self):
        x = np.random.default_rng(1).normal(3, 5, (4, 6))
        y = S.layer_norm(x, np.ones(6), np.zeros(6))
        np.testing.assert_allclose(y.mean(axis=-1), 0, atol=1e-12)
        np.testing.assert_allclose(y.var(axis=-1), 1, atol=1e-4)

    def test_layer_norm_affine(self):
        x = np.array([[1.0, 2.0, 3.0]])
        y = S.layer_norm(x, np.array([2.0, 2.0, 2.0]), np.array([1.0, 1.0, 1.0]), eps=0.0)
        np.testing.assert_allclose(y, [[1 - 2 * np.sqrt(1.5), 1.0, 1 + 2 * np.sqrt(1.5)]])

    def test_feed_forward(self):
        x = np.array([[1.0, -1.0]])
        out = S.feed_forward(x, np.eye(2), np.zeros(2), np.array([[1.0], [1.0]]), np.array([0.5]))
        np.testing.assert_allclose(out, [[1.5]])

    def test_zero_sublayers_identity(self):
        p = make_params()
        for k in ("Wo", "W2", "b2"):
            p[k] = np.zeros_like(p[k])
        x = np.random.default_rng(2).normal(size=(5, 8))
        np.testing.assert_allclose(S.transformer_block(x, p, 2), x)

    def test_shape_and_reference(self):
        p = make_params()
        x = np.random.default_rng(3).normal(size=(6, 8))
        y = S.transformer_block(x, p, 2)
        self.assertEqual(y.shape, (6, 8))
        ln = lambda z, g, b: g * (z - z.mean(-1, keepdims=True)) / np.sqrt(z.var(-1, keepdims=True) + 1e-5) + b
        h1 = x + S.multi_head_attention(ln(x, p["ln1_g"], p["ln1_b"]), p["Wq"], p["Wk"], p["Wv"], p["Wo"], 2, causal=True)
        ref = h1 + np.maximum(ln(h1, p["ln2_g"], p["ln2_b"]) @ p["W1"] + p["b1"], 0) @ p["W2"] + p["b2"]
        np.testing.assert_allclose(y, ref, atol=1e-12)

    def test_causal(self):
        p = make_params(seed=4)
        x = np.random.default_rng(5).normal(size=(5, 8))
        x2 = x.copy()
        x2[3:] += 10.0
        y, y2 = S.transformer_block(x, p, 4), S.transformer_block(x2, p, 4)
        np.testing.assert_allclose(y[:3], y2[:3], atol=1e-12)
        self.assertFalse(np.allclose(y[3:], y2[3:]))


try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_layer_norm_matches_torch(self):
        rng = np.random.default_rng(6)
        x, g, b = rng.normal(size=(3, 5)), rng.normal(size=5), rng.normal(size=5)
        ln = torch.nn.LayerNorm(5, eps=1e-5, dtype=torch.float64)
        with torch.no_grad():
            ln.weight.copy_(torch.tensor(g))
            ln.bias.copy_(torch.tensor(b))
            theirs = ln(torch.tensor(x)).numpy()
        np.testing.assert_allclose(S.layer_norm(x, g, b), theirs, atol=1e-12)


if __name__ == "__main__":
    unittest.main()
