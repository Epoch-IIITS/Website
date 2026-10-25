"""Tests for DL-09 Autograd in PyTorch.

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


def by_hand(x, w, b, t):
    z = sum(xi * wi for xi, wi in zip(x, w)) + b
    p = 1 / (1 + math.exp(-z))
    dz = 2 * (p - t) * p * (1 - p)
    return (p - t) ** 2, [dz * xi for xi in x], dz


class TestNeuronGradients(unittest.TestCase):
    def test_example(self):
        r = S.neuron_gradients([1, 2], [0.5, -1], 0.0, 1.0)
        loss, dw, db = by_hand([1, 2], [0.5, -1], 0.0, 1.0)
        self.assertAlmostEqual(r["loss"], loss, places=5)
        for a, e in zip(r["dw"], dw):
            self.assertAlmostEqual(a, e, places=5)
        self.assertAlmostEqual(r["db"], db, places=5)

    def test_other_point(self):
        r = S.neuron_gradients([0.3, -1.2, 2.0], [1.0, 0.4, -0.7], 0.25, 0.0)
        loss, dw, db = by_hand([0.3, -1.2, 2.0], [1.0, 0.4, -0.7], 0.25, 0.0)
        self.assertAlmostEqual(r["loss"], loss, places=5)
        self.assertTrue(all(abs(a - e) < 1e-5 for a, e in zip(r["dw"], dw)))

    def test_no_accumulation_between_calls(self):
        a = S.neuron_gradients([1, 2], [0.5, -1], 0.0, 1.0)
        b = S.neuron_gradients([1, 2], [0.5, -1], 0.0, 1.0)
        self.assertEqual(a, b)

    def test_caller_tensor_untouched(self):
        w = torch.tensor([0.5, -1.0], requires_grad=True)
        S.neuron_gradients([1, 2], w.tolist(), 0.0, 1.0)
        self.assertIsNone(w.grad)

    def test_types(self):
        r = S.neuron_gradients([1.0], [2.0], 1.0, 0.5)
        self.assertIs(type(r["loss"]), float)
        self.assertIs(type(r["db"]), float)
        self.assertTrue(all(type(v) is float for v in r["dw"]))

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.neuron_gradients([1, 2, 3], [1, 2], 0.0, 1.0)


if __name__ == "__main__":
    unittest.main()
