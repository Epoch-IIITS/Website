"""Tests for DL-18 A Full Training Loop.

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


XOR_X = [[0, 0], [0, 1], [1, 0], [1, 1]]
XOR_Y = [0, 1, 1, 0]


def rings(seed=0, n=200):
    rng = np.random.default_rng(seed)
    r = np.where(np.arange(n) % 2 == 0, 1.0, 2.5) + rng.normal(scale=0.2, size=n)
    angle = rng.uniform(0, 2 * np.pi, n)
    return np.c_[r * np.cos(angle), r * np.sin(angle)], (np.arange(n) % 2)


class TestTrainingLoop(unittest.TestCase):
    def test_learns_xor(self):
        model, history = S.train_classifier(XOR_X, XOR_Y, epochs=150, batch_size=4)
        self.assertEqual(S.predict(model, XOR_X), XOR_Y)
        self.assertLess(history[-1], 0.1)

    def test_loss_falls(self):
        X, y = rings()
        _, history = S.train_classifier(X, y, epochs=40)
        self.assertEqual(len(history), 40)
        self.assertLess(history[-1], history[0] / 2)

    def test_generalises_on_rings(self):
        X, y = rings(1)
        Xt, yt = rings(2)
        model, _ = S.train_classifier(X, y, epochs=60)
        self.assertGreater(np.mean(np.array(S.predict(model, Xt)) == yt), 0.9)

    def test_reproducible(self):
        X, y = rings(3, n=60)
        _, a = S.train_classifier(X, y, epochs=5, seed=7)
        _, b = S.train_classifier(X, y, epochs=5, seed=7)
        self.assertEqual(a, b)

    def test_eval_mode_and_shapes(self):
        X, y = rings(4, n=40)
        model, history = S.train_classifier(X, y, n_hidden=8, epochs=2)
        self.assertFalse(model.training)
        self.assertEqual(model[-1].out_features, 2)
        self.assertTrue(all(type(v) is float for v in history))

    def test_three_classes(self):
        X = [[0, 0], [5, 5], [-5, 5]] * 10
        y = [0, 1, 2] * 10
        model, _ = S.train_classifier(X, y, epochs=60)
        self.assertEqual(S.predict(model, [[0, 0.2], [5, 4.8], [-4.8, 5]]), [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
