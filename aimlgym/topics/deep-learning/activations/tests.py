"""Tests for DL-01 Activation Functions.

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

Z = np.array([-2., 0., 3.])

def num_grad(f, z, h=1e-6):
    return (f(z + h) - f(z - h)) / (2 * h)

class TestAct(unittest.TestCase):
    def test_relu(self):
        np.testing.assert_allclose(S.relu(Z), [0, 0, 3])
        np.testing.assert_allclose(S.relu_grad(Z), [0, 0, 1])

    def test_leaky(self):
        np.testing.assert_allclose(S.leaky_relu(np.array([-2., 3.]), alpha=0.1), [-0.2, 3])
        np.testing.assert_allclose(S.leaky_relu_grad(Z, alpha=0.1), [0.1, 0.1, 1])

    def test_tanh(self):
        np.testing.assert_allclose(S.tanh(Z), np.tanh(Z))
        self.assertAlmostEqual(S.tanh_grad(np.array([0.]))[0], 1.0)

    def test_numeric_grads(self):
        z = np.array([-1.3, -0.2, 0.4, 2.1])
        np.testing.assert_allclose(S.tanh_grad(z), num_grad(S.tanh, z), atol=1e-8)
        np.testing.assert_allclose(S.relu_grad(z), num_grad(S.relu, z), atol=1e-6)
        np.testing.assert_allclose(S.leaky_relu_grad(z, 0.2), num_grad(lambda v: S.leaky_relu(v, 0.2), z), atol=1e-6)

    def test_no_mutation(self):
        z = Z.copy()
        S.relu(z); S.leaky_relu(z); S.tanh_grad(z)
        np.testing.assert_array_equal(z, Z)

    def test_2d_shape(self):
        self.assertEqual(S.relu_grad(np.zeros((3, 4))).shape, (3, 4))

    def test_saturation(self):
        self.assertLess(S.tanh_grad(np.array([10.]))[0], 1e-7)


if __name__ == "__main__":
    unittest.main()
