"""Tests for CV-15 A Convolution Layer with Channels.

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


def reference(x, w, b, s, p):
    c_out, c_in, k, _ = w.shape
    xp = np.pad(x, ((0, 0), (p, p), (p, p)))
    ho = (x.shape[1] + 2 * p - k) // s + 1
    wo = (x.shape[2] + 2 * p - k) // s + 1
    out = np.zeros((c_out, ho, wo))
    for o in range(c_out):
        for i in range(ho):
            for j in range(wo):
                total = b[o]
                for c in range(c_in):
                    for u in range(k):
                        for v in range(k):
                            total += w[o, c, u, v] * xp[c, i * s + u, j * s + v]
                out[o, i, j] = total
    return out


class TestConv2dLayer(unittest.TestCase):
    def test_output_size(self):
        self.assertEqual(S.conv_output_size(4, 3, 1, 2), 2)
        self.assertEqual(S.conv_output_size(28, 5), 24)
        self.assertEqual(S.conv_output_size(7, 3, 1, 1), 7)
        with self.assertRaises(ValueError):
            S.conv_output_size(2, 5)

    def test_single_channel_matches_filter(self):
        x = np.arange(16.0).reshape(1, 4, 4)
        w = np.ones((1, 1, 3, 3))
        out = S.conv2d(x, w)
        self.assertEqual(out.shape, (1, 2, 2))
        self.assertEqual(out[0, 0, 0], x[0, :3, :3].sum())

    def test_sums_over_channels(self):
        x = np.stack([np.ones((3, 3)), 2 * np.ones((3, 3))])
        w = np.ones((1, 2, 3, 3))
        self.assertEqual(S.conv2d(x, w)[0, 0, 0], 9 + 18)

    def test_matches_reference(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=(2, 5, 6))
        w = rng.normal(size=(3, 2, 3, 3))
        b = rng.normal(size=3)
        for s, p in [(1, 0), (2, 1), (1, 2)]:
            np.testing.assert_allclose(S.conv2d(x, w, b, stride=s, padding=p), reference(x, w, b, s, p), atol=1e-12)

    def test_no_flip(self):
        x = np.zeros((1, 3, 3)); x[0, 0, 0] = 1.0
        w = np.zeros((1, 1, 3, 3)); w[0, 0, 0, 0] = 5.0
        self.assertEqual(S.conv2d(x, w)[0, 0, 0], 5.0)

    def test_channel_mismatch(self):
        with self.assertRaises(ValueError):
            S.conv2d(np.zeros((3, 4, 4)), np.zeros((2, 1, 3, 3)))

    def test_params(self):
        self.assertEqual(S.conv_params(2, 3, 3), 57)
        self.assertEqual(S.conv_params(3, 16, 5), 16 * 76)


try:
    import torch
    import torch.nn.functional as F
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_matches_torch_conv2d(self):
        rng = np.random.default_rng(1)
        x = rng.normal(size=(3, 7, 7))
        w = rng.normal(size=(4, 3, 3, 3))
        b = rng.normal(size=4)
        theirs = F.conv2d(torch.tensor(x)[None], torch.tensor(w), torch.tensor(b), stride=2, padding=1)[0].numpy()
        np.testing.assert_allclose(S.conv2d(x, w, b, stride=2, padding=1), theirs, atol=1e-10)


if __name__ == "__main__":
    unittest.main()
