"""Tests for LM-16 A Tiny GPT in PyTorch.

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

TEXT = "hello world. " * 40
TRAINED = []


def trained():
    """Train once and share the result, so each test reports its own failure."""
    if not TRAINED:
        TRAINED.append(S.train_tiny_gpt(TEXT, context=16, steps=200))
    return TRAINED[0]


class TestTinyGPT(unittest.TestCase):
    def test_loss_falls(self):
        losses = trained()[3]
        self.assertGreater(losses[0], 1.5)
        self.assertLess(sum(losses[-10:]) / 10, 0.3)

    def test_generates_pattern(self):
        model, stoi, itos, _ = trained()
        self.assertEqual(S.generate(model, stoi, itos, "hello w", 11), "hello world. hello")

    def test_vocab_and_mode(self):
        model, stoi, itos, _ = trained()
        self.assertEqual(itos, sorted(set(TEXT)))
        self.assertEqual(stoi["h"], itos.index("h"))
        self.assertFalse(model.training)

    def test_output_shape_and_causality(self):
        torch.manual_seed(0)
        model = S.TinyGPT(10, 8)
        idx = torch.randint(0, 10, (2, 8))
        out = model(idx)
        self.assertEqual(tuple(out.shape), (2, 8, 10))
        changed = idx.clone(); changed[:, 5] = (changed[:, 5] + 1) % 10
        self.assertTrue(torch.allclose(out[:, :5], model(changed)[:, :5], atol=1e-5))

    def test_long_prompt_is_cropped(self):
        model, stoi, itos, _ = trained()
        text = S.generate(model, stoi, itos, TEXT[:40], 3)
        self.assertEqual(len(text), 43)

    def test_unknown_prompt_character(self):
        with self.assertRaises(ValueError):
            model, stoi, itos, _ = trained()
            S.generate(model, stoi, itos, "HELLO", 2)


if __name__ == "__main__":
    unittest.main()
