"""Tests for DL-11 Backpropagation Through a Dense Layer.

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


def numeric_grad(f, P, h=1e-6):
    g = np.zeros_like(P)
    for idx in np.ndindex(P.shape):
        old = P[idx]
        P[idx] = old + h; up = f()
        P[idx] = old - h; down = f()
        P[idx] = old
        g[idx] = (up - down) / (2 * h)
    return g


class TestDenseBackward(unittest.TestCase):
    def test_example(self):
        dX, dW, db = S.dense_backward([[1.0, 2.0]], [[1.0], [-1.0]], [[3.0]])
        np.testing.assert_allclose(dW, [[3.0], [6.0]])
        np.testing.assert_allclose(db, [3.0])
        np.testing.assert_allclose(dX, [[3.0, -3.0]])

    def test_shapes(self):
        rng = np.random.default_rng(0)
        X, W, dY = rng.normal(size=(5, 3)), rng.normal(size=(3, 4)), rng.normal(size=(5, 4))
        dX, dW, db = S.dense_backward(X, W, dY)
        self.assertEqual((dX.shape, dW.shape, db.shape), (X.shape, W.shape, (4,)))

    def test_dense_numeric(self):
        rng = np.random.default_rng(1)
        X, W, b = rng.normal(size=(4, 3)), rng.normal(size=(3, 2)), rng.normal(size=2)
        T = rng.normal(size=(4, 2))
        loss = lambda: float(np.sum((X @ W + b) * T))
        dX, dW, db = S.dense_backward(X, W, T)
        np.testing.assert_allclose(dW, numeric_grad(loss, W), atol=1e-6)
        np.testing.assert_allclose(db, numeric_grad(loss, b), atol=1e-6)
        np.testing.assert_allclose(dX, numeric_grad(loss, X), atol=1e-6)

    def test_relu_backward(self):
        Z = np.array([[-1.0, 0.0, 2.0]])
        np.testing.assert_array_equal(S.relu_backward(Z, np.array([[5.0, 5.0, 5.0]])), [[0.0, 0.0, 5.0]])

    def test_mse(self):
        loss, g = S.mse_and_grad([[1.0, 2.0], [3.0, 4.0]], [[1.0, 0.0], [3.0, 2.0]])
        self.assertAlmostEqual(loss, 2.0)
        np.testing.assert_allclose(g, [[0.0, 1.0], [0.0, 1.0]])

    def test_two_layer_numeric(self):
        rng = np.random.default_rng(2)
        X, Y = rng.normal(size=(6, 3)), rng.normal(size=(6, 2))
        params = {"W1": rng.normal(size=(3, 5)), "b1": rng.normal(size=5) * 0.1,
                  "W2": rng.normal(size=(5, 2)), "b2": np.zeros(2)}
        loss, grads = S.two_layer_grads(X, Y, params)
        self.assertEqual(set(grads), set(params))
        for k in params:
            num = numeric_grad(lambda: S.two_layer_grads(X, Y, params)[0], params[k])
            np.testing.assert_allclose(grads[k], num, atol=1e-5, err_msg=k)


try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_matches_torch(self):
        rng = np.random.default_rng(3)
        X, Y = rng.normal(size=(4, 3)), rng.normal(size=(4, 2))
        params = {"W1": rng.normal(size=(3, 4)), "b1": rng.normal(size=4),
                  "W2": rng.normal(size=(4, 2)), "b2": rng.normal(size=2)}
        loss, grads = S.two_layer_grads(X, Y, params)
        t = {k: torch.tensor(v, requires_grad=True) for k, v in params.items()}
        H = torch.relu(torch.tensor(X) @ t["W1"] + t["b1"])
        tloss = torch.mean((H @ t["W2"] + t["b2"] - torch.tensor(Y)) ** 2)
        tloss.backward()
        self.assertAlmostEqual(loss, tloss.item(), places=10)
        for k in params:
            np.testing.assert_allclose(grads[k], t[k].grad.numpy(), atol=1e-10)


if __name__ == "__main__":
    unittest.main()
