"""Tests for CV-21 A Small CNN in PyTorch.

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
import torch
from torch import nn


def make_shapes(n, seed, size=16):
    """Class 0: horizontal bar, 1: vertical bar, 2: square outline; random positions and noise."""
    rng = np.random.default_rng(seed)
    images = np.zeros((n, size, size), np.uint8)
    labels = np.arange(n) % 3
    for i, label in enumerate(labels):
        r, c = rng.integers(2, size - 8, 2)
        if label == 0:
            images[i, r + 3, c:c + 7] = 255
        elif label == 1:
            images[i, r:r + 7, c + 3] = 255
        else:
            images[i, r:r + 6, c] = images[i, r:r + 6, c + 5] = 255
            images[i, r, c:c + 6] = images[i, r + 5, c:c + 6] = 255
        images[i] = np.clip(images[i].astype(int) + rng.integers(0, 40, (size, size)), 0, 255)
    return images, labels


class TestSmallCNN(unittest.TestCase):
    def test_shapes_through_network(self):
        model = S.SmallCNN(3, 16)
        self.assertEqual(tuple(model(torch.zeros(5, 1, 16, 16)).shape), (5, 3))
        self.assertEqual(model.classifier.in_features, 256)

    def test_layers(self):
        model = S.SmallCNN(4, 32)
        convs = [m for m in model.features if isinstance(m, nn.Conv2d)]
        pools = [m for m in model.features if isinstance(m, nn.MaxPool2d)]
        self.assertEqual([(c.in_channels, c.out_channels) for c in convs], [(1, 8), (8, 16)])
        self.assertEqual(len(pools), 2)
        self.assertEqual(model.classifier.in_features, 16 * 8 * 8)

    def test_learns_shapes(self):
        X, y = make_shapes(300, 0)
        model, history = S.train_cnn(X, y, epochs=8)
        Xt, yt = make_shapes(150, 1)
        self.assertGreater(np.mean(np.array(S.predict(model, Xt)) == yt), 0.9)
        self.assertLess(history[-1], history[0])

    def test_reproducible(self):
        X, y = make_shapes(64, 2)
        _, a = S.train_cnn(X, y, epochs=2, seed=3)
        _, b = S.train_cnn(X, y, epochs=2, seed=3)
        self.assertEqual(a, b)

    def test_eval_mode_and_types(self):
        X, y = make_shapes(30, 3)
        model, history = S.train_cnn(X, y, epochs=1)
        self.assertFalse(model.training)
        preds = S.predict(model, X[:4])
        self.assertEqual(len(preds), 4)
        self.assertTrue(all(type(p) is int for p in preds))

    def test_parameter_count(self):
        n = sum(p.numel() for p in S.SmallCNN(3, 16).parameters())
        self.assertEqual(n, (1 * 8 * 9 + 8) + (8 * 16 * 9 + 16) + (256 * 3 + 3))


if __name__ == "__main__":
    unittest.main()
