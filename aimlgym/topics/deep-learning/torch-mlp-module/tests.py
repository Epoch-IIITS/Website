"""Tests for DL-06 Models with nn.Module.

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


class TestMLPModule(unittest.TestCase):
    def test_output_shape(self):
        torch.manual_seed(0)
        model = S.MLP(4, 8, 3)
        self.assertEqual(tuple(model(torch.zeros(5, 4)).shape), (5, 3))

    def test_parameter_count(self):
        self.assertEqual(S.count_parameters(S.MLP(4, 8, 3)), 67)
        self.assertEqual(S.count_parameters(S.MLP(10, 1, 1)), 13)

    def test_is_module_with_registered_layers(self):
        model = S.MLP(2, 3, 1)
        self.assertIsInstance(model, nn.Module)
        names = [name for name, _ in model.named_parameters()]
        self.assertEqual(names, ["net.0.weight", "net.0.bias", "net.2.weight", "net.2.bias"])

    def test_forward_matches_manual(self):
        torch.manual_seed(1)
        model = S.MLP(3, 4, 2)
        x = torch.randn(6, 3)
        l1, l2 = model.net[0], model.net[2]
        manual = torch.relu(x @ l1.weight.T + l1.bias) @ l2.weight.T + l2.bias
        self.assertTrue(torch.allclose(model(x), manual, atol=1e-6))

    def test_seeded_initialisation(self):
        torch.manual_seed(5); a = S.MLP(3, 4, 2)
        torch.manual_seed(5); b = S.MLP(3, 4, 2)
        for pa, pb in zip(a.parameters(), b.parameters()):
            self.assertTrue(torch.equal(pa, pb))

    def test_count_is_int_and_sees_new_modules(self):
        model = S.MLP(2, 2, 2)
        self.assertIs(type(S.count_parameters(model)), int)
        self.assertEqual(S.count_parameters(nn.Linear(5, 2)), 12)


if __name__ == "__main__":
    unittest.main()
