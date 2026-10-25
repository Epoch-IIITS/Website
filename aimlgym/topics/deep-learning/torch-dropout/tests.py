"""Tests for DL-20 Dropout with train() and eval().

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


class TestDropout(unittest.TestCase):
    def test_training_outputs_vary(self):
        torch.manual_seed(0)
        model = S.DropoutMLP(4, 64, 3, p=0.5)
        model.train()
        x = torch.ones(2, 4)
        self.assertFalse(torch.equal(model(x), model(x)))

    def test_predictions_deterministic(self):
        torch.manual_seed(1)
        model = S.DropoutMLP(4, 32, 3)
        x = torch.randn(5, 4)
        a, b = S.predict_proba(model, x), S.predict_proba(model, x)
        self.assertTrue(torch.equal(a, b))
        self.assertTrue(torch.allclose(a.sum(dim=1), torch.ones(5)))

    def test_mode_restored(self):
        model = S.DropoutMLP(2, 4, 2)
        model.train()
        S.predict_proba(model, [[0.0, 1.0]])
        self.assertTrue(model.training)
        model.eval()
        S.predict_proba(model, [[0.0, 1.0]])
        self.assertFalse(model.training)

    def test_inverted_scaling(self):
        torch.manual_seed(2)
        model = S.DropoutMLP(1, 1, 1, p=0.25)
        dropout = model.net[2]
        self.assertIsInstance(dropout, nn.Dropout)
        dropout.train()
        out = dropout(torch.full((1000,), 2.0))
        kept = out[out != 0]
        self.assertTrue(torch.allclose(kept, torch.full_like(kept, 2.0 / 0.75)))
        self.assertAlmostEqual(out.mean().item(), 2.0, delta=0.15)

    def test_no_gradients_tracked(self):
        model = S.DropoutMLP(3, 4, 2)
        self.assertFalse(S.predict_proba(model, torch.randn(2, 3)).requires_grad)

    def test_invalid_p(self):
        for p in (-0.1, 1.0):
            with self.assertRaises(ValueError):
                S.DropoutMLP(2, 2, 2, p=p)


if __name__ == "__main__":
    unittest.main()
