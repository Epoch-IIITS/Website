"""Tests for DL-03 Cross-Entropy Loss.

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

class TestCE(unittest.TestCase):
    def test_single(self):
        z = np.array([[2., 0., -1.]])
        p = np.exp(z) / np.exp(z).sum()
        self.assertAlmostEqual(S.cross_entropy(z, np.array([0])), -np.log(p[0, 0]))

    def test_uniform(self):
        self.assertAlmostEqual(S.cross_entropy(np.zeros((2, 2)), np.array([0, 1])), np.log(2))

    def test_large_logits(self):
        self.assertAlmostEqual(S.cross_entropy(np.array([[1000., 0.]]), np.array([1])), 1000.0)

    def test_grad_formula(self):
        z = np.array([[2., 0., -1.]])
        p = np.exp(z) / np.exp(z).sum()
        np.testing.assert_allclose(S.cross_entropy_grad(z, np.array([0])), p - [[1, 0, 0]])

    def test_grad_numeric(self):
        rng = np.random.default_rng(0)
        z, y = rng.normal(size=(4, 3)), np.array([0, 2, 1, 2])
        g = S.cross_entropy_grad(z, y)
        h = 1e-6
        for i in range(4):
            for j in range(3):
                e = np.zeros_like(z); e[i, j] = h
                num = (S.cross_entropy(z + e, y) - S.cross_entropy(z - e, y)) / (2 * h)
                self.assertAlmostEqual(g[i, j], num, places=6)

    def test_grad_rows_sum_zero(self):
        g = S.cross_entropy_grad(np.random.default_rng(1).normal(size=(5, 4)), np.array([0, 1, 2, 3, 0]))
        np.testing.assert_allclose(g.sum(axis=1), 0, atol=1e-12)

    def test_bad_label(self):
        with self.assertRaises(ValueError):
            S.cross_entropy(np.zeros((1, 3)), np.array([3]))


try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_library_matches_torch(self):
        import numpy as np
        logits = np.array([[2.0, -1.0, 0.5], [0.1, 0.2, 3.0], [-2.0, 4.0, 1.0]])
        labels = np.array([0, 2, 1])
        t = torch.tensor(logits, requires_grad=True)
        loss = torch.nn.functional.cross_entropy(t, torch.tensor(labels))
        loss.backward()
        self.assertAlmostEqual(S.cross_entropy(logits, labels), loss.item(), places=12)
        np.testing.assert_allclose(S.cross_entropy_grad(logits, labels), t.grad.numpy(), atol=1e-12)


if __name__ == "__main__":
    unittest.main()
