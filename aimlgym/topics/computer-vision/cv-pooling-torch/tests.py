"""Tests for CV-13 Pooling with nn.MaxPool2d and nn.AvgPool2d.

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


MAP = torch.tensor([[1.0, 3, 2, 0], [4, 2, 1, 1], [0, 1, 5, 6], [2, 2, 7, 8]])[None, None]


class TestPooling(unittest.TestCase):
    def test_max_example(self):
        self.assertEqual(S.pool(MAP, "max", 2).tolist(), [[[[4.0, 2.0], [2.0, 8.0]]]])

    def test_avg_example(self):
        self.assertEqual(S.pool(MAP, "avg", 2).tolist(), [[[[2.5, 1.0], [1.25, 6.5]]]])

    def test_sizes(self):
        x = torch.randn(2, 3, 11, 9)
        out = S.pool(x, "max", 3, stride=2, padding=1)
        self.assertEqual(tuple(out.shape), (2, 3, S.pooled_size(11, 3, 2, 1), S.pooled_size(9, 3, 2, 1)))
        self.assertEqual((S.pooled_size(4, 2), S.pooled_size(7, 3, 1, 1)), (2, 7))

    def test_max_gradient_goes_to_argmax(self):
        x = MAP.clone().requires_grad_(True)
        S.pool(x, "max", 2).sum().backward()
        expected = torch.zeros(4, 4); expected[1, 0] = expected[0, 2] = expected[3, 0] = expected[3, 3] = 1
        self.assertTrue(torch.equal(x.grad[0, 0], expected))

    def test_avg_gradient_spreads(self):
        x = MAP.clone().requires_grad_(True)
        S.pool(x, "avg", 2).sum().backward()
        self.assertTrue(torch.allclose(x.grad, torch.full_like(x, 0.25)))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.pool(MAP, "median", 2)
        with self.assertRaises(ValueError):
            S.pool(torch.zeros(4, 4), "max", 2)


if __name__ == "__main__":
    unittest.main()
