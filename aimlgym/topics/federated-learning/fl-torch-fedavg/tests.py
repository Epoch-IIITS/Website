"""Tests for FL-11 FedAvg with PyTorch state_dicts.

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


def client(seed, n, slope=2.0, shift=0.0):
    g = torch.Generator().manual_seed(seed)
    X = torch.rand(n, 1, generator=g) * 2 - 1 + shift
    return X, slope * X[:, 0] + 0.5


class TestFedAvg(unittest.TestCase):
    def test_weighted_average(self):
        a = {"w": torch.tensor([1.0]), "steps": torch.tensor(3)}
        b = {"w": torch.tensor([2.0]), "steps": torch.tensor(7)}
        out = S.average_states([a, b], [30, 10])
        self.assertAlmostEqual(out["w"].item(), 1.25)
        self.assertEqual((out["steps"].item(), out["steps"].dtype), (3, torch.int64))

    def test_equal_counts_is_mean(self):
        torch.manual_seed(0)
        states = [nn.Linear(3, 2).state_dict() for _ in range(3)]
        out = S.average_states(states, [5, 5, 5])
        self.assertTrue(torch.allclose(out["weight"], sum(s["weight"] for s in states) / 3))

    def test_batchnorm_model(self):
        torch.manual_seed(1)
        states = [nn.Sequential(nn.Linear(2, 2), nn.BatchNorm1d(2)).state_dict() for _ in range(2)]
        out = S.average_states(states, [1, 3])
        self.assertEqual(out["1.num_batches_tracked"].dtype, torch.int64)
        nn.Sequential(nn.Linear(2, 2), nn.BatchNorm1d(2)).load_state_dict(out)

    def test_training_improves(self):
        torch.manual_seed(2)
        model = nn.Linear(1, 1)
        clients = [client(0, 30), client(1, 10, shift=0.5), client(2, 20, shift=-0.5)]
        losses = S.federated_training(model, clients, rounds=8, epochs=2, lr=0.1)
        self.assertEqual(len(losses), 8)
        self.assertLess(losses[-1], losses[0] / 4)
        self.assertAlmostEqual(model.weight.item(), 2.0, delta=0.2)

    def test_reproducible(self):
        clients = [client(3, 16), client(4, 16)]
        torch.manual_seed(3); a = S.federated_training(nn.Linear(1, 1), clients, rounds=3)
        torch.manual_seed(3); b = S.federated_training(nn.Linear(1, 1), clients, rounds=3)
        self.assertEqual(a, b)

    def test_invalid(self):
        s = nn.Linear(1, 1).state_dict()
        with self.assertRaises(ValueError):
            S.average_states([], [])
        with self.assertRaises(ValueError):
            S.average_states([s, s], [1, 0])
        with self.assertRaises(ValueError):
            S.average_states([s, {"weight": s["weight"]}], [1, 1])


if __name__ == "__main__":
    unittest.main()
