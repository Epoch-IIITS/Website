"""Tests for DL-22 Batch Normalisation with nn.BatchNorm1d.

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


class TestBatchNorm(unittest.TestCase):
    def test_worked_example(self):
        r = S.run_batchnorm([[[1.0], [3.0]]], [[2.0]])
        self.assertAlmostEqual(r["running_mean"][0], 0.2, places=6)
        self.assertAlmostEqual(r["running_var"][0], 1.1, places=6)
        self.assertAlmostEqual(r["train_output"][0][0], -1 / math.sqrt(1 + 1e-5), places=5)

    def test_running_statistics_formula(self):
        torch.manual_seed(0)
        batches = [torch.randn(8, 3) * 2 + 5 for _ in range(4)]
        r = S.run_batchnorm([b.tolist() for b in batches], [[0.0, 0.0, 0.0]], momentum=0.2)
        mean, var = torch.zeros(3), torch.ones(3)
        for b in batches:
            mean = 0.8 * mean + 0.2 * b.mean(dim=0)
            var = 0.8 * var + 0.2 * b.var(dim=0, unbiased=True)
        self.assertTrue(torch.allclose(torch.tensor(r["running_mean"]), mean, atol=1e-5))
        self.assertTrue(torch.allclose(torch.tensor(r["running_var"]), var, atol=1e-4))

    def test_train_output_standardised(self):
        torch.manual_seed(1)
        r = S.run_batchnorm([(torch.randn(64, 2) * 3 + 10).tolist()], [[10.0, 10.0]])
        out = torch.tensor(r["train_output"])
        self.assertTrue(torch.allclose(out.mean(dim=0), torch.zeros(2), atol=1e-5))
        self.assertTrue(torch.allclose(out.var(dim=0, unbiased=False), torch.ones(2), atol=1e-3))

    def test_eval_uses_running_statistics(self):
        r = S.run_batchnorm([[[1.0, 0.0], [3.0, 4.0]], [[2.0, 2.0], [6.0, 2.0]]], [[4.0, 1.0], [0.0, 0.0]])
        mean, var = torch.tensor(r["running_mean"]), torch.tensor(r["running_var"])
        expected = (torch.tensor([[4.0, 1.0], [0.0, 0.0]]) - mean) / torch.sqrt(var + 1e-5)
        self.assertTrue(torch.allclose(torch.tensor(r["eval_output"]), expected, atol=1e-5))

    def test_single_eval_row_allowed(self):
        r = S.run_batchnorm([[[0.0], [2.0]]], [[1.0]])
        self.assertEqual(len(r["eval_output"]), 1)

    def test_invalid_batches(self):
        with self.assertRaises(ValueError):
            S.run_batchnorm([], [[1.0]])
        with self.assertRaises(ValueError):
            S.run_batchnorm([[[1.0, 2.0]]], [[1.0, 2.0]])


if __name__ == "__main__":
    unittest.main()
