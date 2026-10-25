"""Tests for DL-10 Backprop Through One Neuron.

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

X, W = np.array([1., 2.]), np.array([0.5, -0.25])

def loss_at(w, b, x, y):
    p = 1 / (1 + np.exp(-(w @ x + b)))
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))

class TestNeuron(unittest.TestCase):
    def test_example(self):
        r = S.neuron_forward_backward(X, 1, W, 0.0)
        self.assertAlmostEqual(r["z"], 0.0)
        self.assertAlmostEqual(r["loss"], np.log(2))
        self.assertAlmostEqual(r["dL_dp"], -2.0)
        self.assertAlmostEqual(r["dp_dz"], 0.25)
        np.testing.assert_allclose(r["grad_w"], [-0.5, -1.0])

    def test_p_minus_y(self):
        for y in (0, 1):
            r = S.neuron_forward_backward(np.array([0.3, -1.1]), y, np.array([1.2, 0.4]), -0.2)
            self.assertAlmostEqual(r["dL_dz"], r["p"] - y, places=10)

    def test_numeric_w(self):
        x, w, b, y = np.array([0.7, -0.3, 1.5]), np.array([0.2, 0.9, -0.4]), 0.1, 0
        r = S.neuron_forward_backward(x, y, w, b)
        h = 1e-6
        for j in range(3):
            e = np.zeros(3); e[j] = h
            num = (loss_at(w + e, b, x, y) - loss_at(w - e, b, x, y)) / (2 * h)
            self.assertAlmostEqual(r["grad_w"][j], num, places=6)

    def test_numeric_b(self):
        x, w, b, y = np.array([0.7, -0.3]), np.array([0.2, 0.9]), 0.1, 1
        r = S.neuron_forward_backward(x, y, w, b)
        num = (loss_at(w, b + 1e-6, x, y) - loss_at(w, b - 1e-6, x, y)) / 2e-6
        self.assertAlmostEqual(r["grad_b"], num, places=6)

    def test_large_z_stable(self):
        r = S.neuron_forward_backward(np.array([100.]), 1, np.array([10.]), 0.0)
        self.assertTrue(np.isfinite(r["loss"]))
        self.assertAlmostEqual(r["dL_dz"], 0.0, places=6)

    def test_keys(self):
        r = S.neuron_forward_backward(X, 0, W, 0.0)
        self.assertEqual(set(r), {"z", "p", "loss", "dL_dp", "dp_dz", "dL_dz", "grad_w", "grad_b"})


if __name__ == "__main__":
    unittest.main()
