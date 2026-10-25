"""Tests for FL-02 Weighted Federated Averaging.

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

class TestFedAvg(unittest.TestCase):
    def test_example(self):
        out = S.fedavg([{"w": np.array([1., 2.])}, {"w": np.array([3., 6.])}], [10, 30])
        np.testing.assert_allclose(out["w"], [2.5, 5.0])

    def test_multiple_keys(self):
        out = S.fedavg([{"w": np.ones((2, 2)), "b": np.array([0.])}, {"w": np.zeros((2, 2)), "b": np.array([4.])}], [1, 3])
        np.testing.assert_allclose(out["w"], 0.25)
        np.testing.assert_allclose(out["b"], [3.0])

    def test_equal_sizes_mean(self):
        ps = [{"w": np.array([float(i)])} for i in range(5)]
        np.testing.assert_allclose(S.fedavg(ps, [7] * 5)["w"], [2.0])

    def test_zero_size_client(self):
        out = S.fedavg([{"w": np.array([100.])}, {"w": np.array([1.])}], [0, 5])
        np.testing.assert_allclose(out["w"], [1.0])

    def test_not_plain_mean(self):
        out = S.fedavg([{"w": np.array([0.])}, {"w": np.array([10.])}], [9, 1])
        np.testing.assert_allclose(out["w"], [1.0])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.fedavg([{"w": np.ones(2)}, {"w": np.ones(3)}], [1, 1])
        with self.assertRaises(ValueError):
            S.fedavg([{"w": np.ones(2)}], [0])
        with self.assertRaises(ValueError):
            S.fedavg([{"w": np.ones(2)}, {"v": np.ones(2)}], [1, 1])


if __name__ == "__main__":
    unittest.main()
