"""Tests for DL-05 PyTorch Tensors.

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


class TestDenseRelu(unittest.TestCase):
    def test_example(self):
        out = S.dense_relu([[1, -2]], [[1, 0, 2], [3, 1, -1]], [0.5, 0, 0])
        self.assertIsInstance(out, torch.Tensor)
        self.assertEqual(out.tolist(), [[0.0, 0.0, 4.0]])

    def test_float32_from_float64(self):
        out = S.dense_relu(np.ones((2, 3)), np.ones((3, 4)), np.zeros(4))
        self.assertEqual(out.dtype, torch.float32)
        self.assertEqual(tuple(out.shape), (2, 4))

    def test_matches_numpy(self):
        rng = np.random.default_rng(0)
        x, W, b = rng.normal(size=(5, 3)), rng.normal(size=(3, 2)), rng.normal(size=2)
        expected = np.maximum(x @ W + b, 0)
        self.assertTrue(np.allclose(S.dense_relu(x, W, b).numpy(), expected, atol=1e-5))

    def test_accepts_tensors(self):
        x = torch.tensor([[1.0, 2.0]]); W = torch.eye(2); b = torch.tensor([-1.5, 0.0])
        self.assertEqual(S.dense_relu(x, W, b).tolist(), [[0.0, 2.0]])

    def test_inputs_unchanged(self):
        x = np.array([[-1.0, 2.0]]); W = np.eye(2); b = np.zeros(2)
        S.dense_relu(x, W, b)
        self.assertEqual(x.tolist(), [[-1.0, 2.0]])

    def test_shape_errors(self):
        for args in [([1, 2], [[1], [1]], [0]), ([[1, 2]], [[1, 2, 3]], [0, 0, 0]), ([[1, 2]], [[1], [1]], [0, 0])]:
            with self.assertRaises(ValueError):
                S.dense_relu(*args)


if __name__ == "__main__":
    unittest.main()
