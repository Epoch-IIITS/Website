"""Tests for DL-19 Train an MLP on XOR.

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

class TestXOR(unittest.TestCase):
    def test_init_shapes(self):
        p = S.init_params(5, 0)
        self.assertEqual({k: v.shape for k, v in p.items()}, {"W1": (2, 5), "b1": (5,), "W2": (5, 1), "b2": (1,)})

    def test_init_recipe(self):
        rng = np.random.default_rng(3)
        W1 = rng.normal(0, 1, (2, 4)); W2 = rng.normal(0, 1, (4, 1))
        p = S.init_params(4, 3)
        np.testing.assert_allclose(p["W1"], W1); np.testing.assert_allclose(p["W2"], W2)

    def test_gradients_numeric(self):
        params = S.init_params(3, 1)
        X, y = S.X_XOR, S.Y_XOR
        _, g = S.forward_backward(X, y, params)
        h = 1e-6
        for k in params:
            it = np.nditer(params[k], flags=["multi_index"])
            for _ in it:
                idx = it.multi_index
                pp = {kk: vv.copy() for kk, vv in params.items()}; pm = {kk: vv.copy() for kk, vv in params.items()}
                pp[k][idx] += h; pm[k][idx] -= h
                num = (S.forward_backward(X, y, pp)[0] - S.forward_backward(X, y, pm)[0]) / (2 * h)
                self.assertAlmostEqual(g[k][idx], num, places=6, msg=f"{k}{idx}")

    def test_trains(self):
        params, hist = S.train_xor()
        self.assertEqual(len(hist), 3000)
        self.assertLess(hist[-1], 0.05)

    def test_predictions(self):
        params, _ = S.train_xor()
        h = np.tanh(S.X_XOR @ params["W1"] + params["b1"])
        p = 1 / (1 + np.exp(-(h @ params["W2"] + params["b2"])))[:, 0]
        np.testing.assert_array_equal((p > 0.5).astype(int), [0, 1, 1, 0])

    def test_loss_decreases_overall(self):
        _, hist = S.train_xor(epochs=500)
        self.assertLess(hist[-1], hist[0])

    def test_initial_loss_value(self):
        loss, _ = S.forward_backward(S.X_XOR, S.Y_XOR,
                                     {"W1": np.zeros((2, 2)), "b1": np.zeros(2), "W2": np.zeros((2, 1)), "b2": np.zeros(1)})
        self.assertAlmostEqual(loss, np.log(2))


if __name__ == "__main__":
    unittest.main()
