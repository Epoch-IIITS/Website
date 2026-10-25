"""Tests for DL-27 Debugging Training.

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


def big_regression(seed=0):
    g = torch.Generator().manual_seed(seed)
    X = torch.randn(32, 3, generator=g) * 20
    return X, X @ torch.tensor([[1.0], [-2.0], [0.5]])


class TestDebugging(unittest.TestCase):
    def test_diagnose_patterns(self):
        self.assertEqual(S.diagnose([1.0, 0.5, 0.2]), "learning")
        self.assertEqual(S.diagnose([1.0, 0.99, 0.98]), "stuck")
        self.assertEqual(S.diagnose([1.0, 3.0, 9.0]), "diverging")
        self.assertEqual(S.diagnose([1.0, float("nan")]), "diverging")

    def test_overfit_tiny_batch(self):
        torch.manual_seed(0)
        model = nn.Sequential(nn.Linear(4, 32), nn.ReLU(), nn.Linear(32, 3))
        X = torch.randn(12, 4, generator=torch.Generator().manual_seed(1))
        y = torch.arange(12) % 3
        self.assertLess(S.overfit_one_batch(model, X, y, steps=300, lr=0.01), 0.05)

    def test_more_steps_lower_loss(self):
        X = torch.randn(12, 4, generator=torch.Generator().manual_seed(2))
        y = torch.arange(12) % 3
        torch.manual_seed(0)
        short = S.overfit_one_batch(nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3)), X, y, steps=5)
        torch.manual_seed(0)
        long = S.overfit_one_batch(nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3)), X, y, steps=100)
        self.assertIs(type(short), float)
        self.assertLess(long, short)

    def test_high_lr_diverges_without_clipping(self):
        X, y = big_regression()
        torch.manual_seed(0)
        losses = S.train_with_clipping(nn.Linear(3, 1), X, y, lr=0.05, steps=15)
        self.assertEqual(S.diagnose(losses), "diverging")

    def test_clipping_keeps_training_stable(self):
        X, y = big_regression()
        torch.manual_seed(0)
        losses = S.train_with_clipping(nn.Linear(3, 1), X, y, lr=0.05, steps=150, max_norm=1.0)
        self.assertTrue(all(math.isfinite(v) for v in losses))
        self.assertLess(losses[-1], losses[0] / 10)

    def test_short_history_rejected(self):
        with self.assertRaises(ValueError):
            S.diagnose([1.0])


if __name__ == "__main__":
    unittest.main()
