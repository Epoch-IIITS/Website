"""Tests for DL-12 Custom Gradients and gradcheck.

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
import torch.nn.functional as F


class WrongSquare(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return x * x

    @staticmethod
    def backward(ctx, grad_output):
        (x,) = ctx.saved_tensors
        return grad_output * x          # should be 2x


class TestSoftplus(unittest.TestCase):
    def test_forward_matches_library(self):
        x = torch.linspace(-5, 5, 11)
        self.assertTrue(torch.allclose(S.softplus(x), F.softplus(x), atol=1e-6))

    def test_backward_is_sigmoid(self):
        x = torch.tensor([-2.0, 0.0, 3.0], requires_grad=True)
        S.softplus(x).sum().backward()
        self.assertTrue(torch.allclose(x.grad, torch.sigmoid(x.detach()), atol=1e-6))

    def test_passes_gradcheck(self):
        self.assertTrue(S.passes_gradcheck(S.softplus, (4, 3)))

    def test_wrong_backward_fails(self):
        self.assertFalse(S.passes_gradcheck(WrongSquare.apply, (5,)))

    def test_stable_for_large_inputs(self):
        x = torch.tensor([100.0, -100.0], dtype=torch.float64)
        out = S.softplus(x)
        self.assertTrue(torch.isfinite(out).all())
        self.assertAlmostEqual(out[0].item(), 100.0, places=6)
        self.assertAlmostEqual(out[1].item(), 0.0, places=6)

    def test_uses_custom_function(self):
        x = torch.tensor([0.5], requires_grad=True)
        self.assertIn("Softplus", type(S.softplus(x).grad_fn).__name__)
        self.assertIsInstance(S.passes_gradcheck(torch.sin, (2,)), bool)


if __name__ == "__main__":
    unittest.main()
