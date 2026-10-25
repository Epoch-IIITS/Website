"""Tests for LM-11 A Transformer Block as nn.Module.

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


import torch
from torch import nn


class TestTransformerBlock(unittest.TestCase):
    def test_shape(self):
        torch.manual_seed(0)
        block = S.TransformerBlock(16, 2)
        self.assertEqual(tuple(block(torch.randn(2, 5, 16)).shape), (2, 5, 16))

    def test_causal(self):
        torch.manual_seed(1)
        block = S.TransformerBlock(8, 2)
        x = torch.randn(1, 6, 8)
        y = x.clone(); y[0, 4] += torch.randn(8)
        a, b = block(x), block(y)
        self.assertTrue(torch.allclose(a[0, :4], b[0, :4], atol=1e-6))
        self.assertFalse(torch.allclose(a[0, 4], b[0, 4]))

    def test_non_causal_sees_everything(self):
        torch.manual_seed(2)
        block = S.TransformerBlock(8, 2)
        x = torch.randn(1, 4, 8)
        y = x.clone(); y[0, 3] += torch.randn(8)
        self.assertFalse(torch.allclose(block(x, causal=False)[0, 0], block(y, causal=False)[0, 0]))

    def test_matches_encoder_layer(self):
        torch.manual_seed(3)
        ref = nn.TransformerEncoderLayer(16, 4, 64, dropout=0.0, activation="gelu", batch_first=True, norm_first=True)
        block = S.TransformerBlock(16, 4)
        block.load_state_dict(ref.state_dict())
        x = torch.randn(3, 7, 16)
        mask = torch.triu(torch.ones(7, 7, dtype=torch.bool), diagonal=1)
        ref.train()
        self.assertTrue(torch.allclose(block(x), ref(x, src_mask=mask), atol=1e-5))

    def test_parameter_count(self):
        d = 32
        block = S.TransformerBlock(d, 4)
        expected = 2 * (2 * d) + (3 * d * d + 3 * d) + (d * d + d) + (d * 4 * d + 4 * d) + (4 * d * d + d)
        self.assertEqual(sum(p.numel() for p in block.parameters()), expected)

    def test_invalid_heads(self):
        with self.assertRaises(ValueError):
            S.TransformerBlock(10, 3)


if __name__ == "__main__":
    unittest.main()
