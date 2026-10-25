"""Tests for DL-24 1-D Convolution with nn.Conv1d.

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
import torch
from torch import nn


def manual(x, w, b, stride, padding):
    x = np.pad(np.asarray(x, dtype=float), ((0, 0), (0, 0), (padding, padding)))
    B, C, L = x.shape
    O, _, K = np.shape(w)
    n = (L - K) // stride + 1
    out = np.zeros((B, O, n))
    for bi in range(B):
        for o in range(O):
            for t in range(n):
                out[bi, o, t] = np.sum(np.asarray(w)[o] * x[bi, :, t * stride:t * stride + K]) + (b[o] if b is not None else 0)
    return out


class TestConv1d(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.conv1d_layer([[[1, 2, 3, 4, 5]]], [[[1, 0, -1]]]).tolist(), [[[-2.0, -2.0, -2.0]]])

    def test_padding(self):
        out = S.conv1d_layer([[[1, 2, 3, 4, 5]]], [[[1, 0, -1]]], padding=1)
        self.assertEqual(out.tolist(), [[[-2.0, -2.0, -2.0, -2.0, 4.0]]])

    def test_not_flipped(self):
        signal = [1.0, 2.0, 0.0, 5.0, 3.0]; kernel = [1.0, 2.0, 3.0]
        out = S.conv1d_layer([[signal]], [[kernel]])[0, 0].numpy()
        self.assertTrue(np.allclose(out, np.correlate(signal, kernel, mode="valid")))

    def test_channels_stride_bias(self):
        rng = np.random.default_rng(0)
        x, w, b = rng.normal(size=(2, 3, 11)), rng.normal(size=(4, 3, 3)), rng.normal(size=4)
        out = S.conv1d_layer(x, w, b, stride=2, padding=1)
        self.assertEqual(tuple(out.shape), (2, 4, (11 + 2 - 3) // 2 + 1))
        self.assertTrue(np.allclose(out.numpy(), manual(x, w, b, 2, 1), atol=1e-5))

    def test_matches_nn_conv1d(self):
        torch.manual_seed(0)
        layer = nn.Conv1d(2, 3, kernel_size=4)
        x = torch.randn(5, 2, 9)
        out = S.conv1d_layer(x, layer.weight.detach(), layer.bias.detach())
        self.assertTrue(torch.allclose(out, layer(x).detach(), atol=1e-6))

    def test_invalid(self):
        cases = [([[1, 2, 3]], [[[1]]], None), ([[[1, 2, 3]]], [[[1], [1]]], None),
                 ([[[1, 2]]], [[[1, 1, 1]]], None), ([[[1, 2, 3]]], [[[1]]], [1, 2])]
        for x, w, b in cases:
            with self.assertRaises(ValueError):
                S.conv1d_layer(x, w, b)


if __name__ == "__main__":
    unittest.main()
