"""Tests for FL-05 Client Training with a PyTorch Model.

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


def line(seed, n=40, slope=2.0):
    g = torch.Generator().manual_seed(seed)
    X = torch.rand(n, 1, generator=g) * 2 - 1
    return X, slope * X[:, 0] + 0.5


def zero_model():
    model = nn.Linear(1, 1)
    with torch.no_grad():
        model.weight.zero_(); model.bias.zero_()
    return model


class TestClientUpdate(unittest.TestCase):
    def test_global_unchanged(self):
        model = zero_model()
        X, y = line(0)
        S.client_update(model, X, y, epochs=3)
        self.assertEqual((model.weight.item(), model.bias.item()), (0.0, 0.0))

    def test_learns_towards_client_data(self):
        X, y = line(1)
        state, n = S.client_update(zero_model(), X, y, epochs=20, lr=0.1)
        self.assertEqual(n, 40)
        self.assertAlmostEqual(state["weight"].item(), 2.0, delta=0.2)
        self.assertAlmostEqual(state["bias"].item(), 0.5, delta=0.1)

    def test_more_epochs_lower_loss(self):
        X, y = line(2)
        def loss(state):
            m = zero_model(); m.load_state_dict(state)
            return nn.functional.mse_loss(m(X), y.reshape(-1, 1)).item()
        one, _ = S.client_update(zero_model(), X, y, epochs=1)
        five, _ = S.client_update(zero_model(), X, y, epochs=5)
        self.assertLess(loss(five), loss(one))

    def test_reproducible(self):
        X, y = line(3)
        a, _ = S.client_update(zero_model(), X, y, seed=4)
        b, _ = S.client_update(zero_model(), X, y, seed=4)
        self.assertTrue(all(torch.equal(a[k], b[k]) for k in a))

    def test_state_dict_keys(self):
        X, y = line(4)
        model = nn.Sequential(nn.Linear(1, 4), nn.ReLU(), nn.Linear(4, 1))
        state, _ = S.client_update(model, X, y)
        self.assertEqual(list(state), list(model.state_dict()))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.client_update(zero_model(), torch.zeros(0, 1), torch.zeros(0), epochs=1)
        with self.assertRaises(ValueError):
            S.client_update(zero_model(), *line(5), epochs=0)


if __name__ == "__main__":
    unittest.main()
