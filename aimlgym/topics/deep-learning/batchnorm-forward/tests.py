"""Tests for DL-23 Batch Normalization by Hand (train/eval).

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

class TestBN(unittest.TestCase):
    def test_train_output(self):
        bn = S.BatchNorm1d(1)
        np.testing.assert_allclose(bn.forward(np.array([[1.], [3.]])), [[-1.], [1.]], atol=1e-5)

    def test_running_stats(self):
        bn = S.BatchNorm1d(1)
        bn.forward(np.array([[1.], [3.]]))
        np.testing.assert_allclose(bn.running_mean, [0.2])
        np.testing.assert_allclose(bn.running_var, [1.1])

    def test_normalised_stats(self):
        x = np.random.default_rng(0).normal(5, 3, size=(64, 4))
        y = S.BatchNorm1d(4).forward(x)
        np.testing.assert_allclose(y.mean(0), 0, atol=1e-10)
        np.testing.assert_allclose(y.std(0), 1, atol=1e-3)

    def test_gamma_beta(self):
        bn = S.BatchNorm1d(2); bn.gamma = np.array([2., 3.]); bn.beta = np.array([1., -1.])
        y = bn.forward(np.array([[0., 0.], [2., 4.]]))
        np.testing.assert_allclose(y, [[-1., -4.], [3., 2.]], atol=1e-4)

    def test_eval_uses_running(self):
        bn = S.BatchNorm1d(1)
        bn.running_mean = np.array([10.]); bn.running_var = np.array([4.])
        y = bn.forward(np.array([[12.]]), training=False)
        np.testing.assert_allclose(y, [[1.0]], atol=1e-5)
        np.testing.assert_allclose(bn.running_mean, [10.])

    def test_converges_to_population(self):
        bn = S.BatchNorm1d(1, momentum=0.1)
        rng = np.random.default_rng(1)
        for _ in range(300):
            bn.forward(rng.normal(2.0, 0.5, size=(32, 1)))
        self.assertAlmostEqual(bn.running_mean[0], 2.0, delta=0.05)
        self.assertAlmostEqual(bn.running_var[0], 0.25, delta=0.03)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.BatchNorm1d(2).forward(np.ones((3, 3)))
        with self.assertRaises(ValueError):
            S.BatchNorm1d(1).forward(np.ones((1, 1)))


try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_library_matches_torch_batchnorm(self):
        import numpy as np
        rng = np.random.default_rng(0)
        batches = [rng.normal(2, 3, (8, 4)) for _ in range(3)]
        ours = S.BatchNorm1d(4)
        theirs = torch.nn.BatchNorm1d(4, dtype=torch.float64)
        theirs.train()
        for b in batches:
            np.testing.assert_allclose(ours.forward(b, training=True),
                                       theirs(torch.tensor(b)).detach().numpy(), atol=1e-10)
        np.testing.assert_allclose(ours.running_var, theirs.running_var.numpy(), atol=1e-10)
        theirs.eval()
        test = rng.normal(size=(5, 4))
        np.testing.assert_allclose(ours.forward(test, training=False),
                                   theirs(torch.tensor(test)).detach().numpy(), atol=1e-10)


if __name__ == "__main__":
    unittest.main()
