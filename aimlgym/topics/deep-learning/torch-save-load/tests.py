"""Tests for DL-26 Saving, Loading and Reproducibility.

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


import os
import random
import tempfile

import numpy as np
import torch


class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "model.pt")

    def test_roundtrip_same_outputs(self):
        S.set_seed(0)
        model = S.MLP(4, 8, 3)
        S.save_model(model, self.path)
        loaded = S.load_model(self.path, 4, 8, 3)
        x = torch.randn(5, 4)
        self.assertTrue(torch.equal(model(x), loaded(x)))

    def test_file_holds_state_dict(self):
        S.save_model(S.MLP(2, 3, 1), self.path)
        state = torch.load(self.path, weights_only=True)
        self.assertEqual(list(state), ["net.0.weight", "net.0.bias", "net.2.weight", "net.2.bias"])

    def test_loaded_model_in_eval(self):
        S.save_model(S.MLP(2, 3, 1), self.path)
        self.assertFalse(S.load_model(self.path, 2, 3, 1).training)

    def test_wrong_architecture_rejected(self):
        S.save_model(S.MLP(4, 8, 3), self.path)
        with self.assertRaises(RuntimeError):
            S.load_model(self.path, 4, 16, 3)

    def test_seed_controls_all_generators(self):
        S.set_seed(42)
        a = (random.random(), np.random.rand(), torch.rand(1).item())
        S.set_seed(42)
        b = (random.random(), np.random.rand(), torch.rand(1).item())
        self.assertEqual(a, b)

    def test_seeded_models_identical(self):
        S.set_seed(3); a = S.MLP(3, 3, 3)
        S.set_seed(3); b = S.MLP(3, 3, 3)
        self.assertTrue(all(torch.equal(p, q) for p, q in zip(a.parameters(), b.parameters())))


if __name__ == "__main__":
    unittest.main()
