"""Tests for DL-07 MLP Forward Pass.

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

P = [(np.eye(2), np.zeros(2)), (np.array([[2.], [3.]]), np.array([0.5]))]

class TestMLP(unittest.TestCase):
    def test_example(self):
        logits, cache = S.mlp_forward(np.array([[1., -1.]]), P)
        np.testing.assert_allclose(logits, [[2.5]])
        np.testing.assert_allclose(cache[1]["a_prev"], [[1., 0.]])
        np.testing.assert_allclose(cache[0]["z"], [[1., -1.]])

    def test_no_relu_on_output(self):
        logits, _ = S.mlp_forward(np.array([[1., 1.]]), [(np.array([[-1.], [-1.]]), np.array([0.]))])
        np.testing.assert_allclose(logits, [[-2.]])

    def test_cache_length(self):
        rng = np.random.default_rng(0)
        params = [(rng.normal(size=(3, 5)), np.zeros(5)), (rng.normal(size=(5, 4)), np.zeros(4)),
                  (rng.normal(size=(4, 2)), np.zeros(2))]
        logits, cache = S.mlp_forward(rng.normal(size=(6, 3)), params)
        self.assertEqual(len(cache), 3)
        self.assertEqual(logits.shape, (6, 2))
        self.assertTrue((cache[2]["a_prev"] >= 0).all())

    def test_matches_manual(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(4, 3)); W1, b1 = rng.normal(size=(3, 2)), rng.normal(size=2)
        W2, b2 = rng.normal(size=(2, 3)), rng.normal(size=3)
        exp = np.maximum(X @ W1 + b1, 0) @ W2 + b2
        np.testing.assert_allclose(S.mlp_forward(X, [(W1, b1), (W2, b2)])[0], exp)

    def test_predict(self):
        params = [(np.array([[1., -1.]]), np.array([0., 0.]))]
        np.testing.assert_array_equal(S.predict_classes(np.array([[2.], [-3.]]), params), [0, 1])

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.mlp_forward(np.ones((1, 2)), [])


if __name__ == "__main__":
    unittest.main()
