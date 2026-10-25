"""Tests for DL-14 SGD with Momentum.

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

class TestMomentum(unittest.TestCase):
    def test_example(self):
        opt = S.Momentum(lr=0.1, beta=0.9)
        p = {"w": np.array([0.0])}
        for _ in range(3):
            p = opt.step(p, {"w": np.array([1.0])})
        np.testing.assert_allclose(p["w"], [-0.561])

    def test_beta0_is_sgd(self):
        opt = S.Momentum(lr=0.5, beta=0.0)
        p = opt.step({"a": np.array([1.0, 2.0])}, {"a": np.array([2.0, -2.0])})
        np.testing.assert_allclose(p["a"], [0.0, 3.0])

    def test_no_mutation(self):
        p0, g0 = {"w": np.array([1.0])}, {"w": np.array([0.5])}
        S.Momentum(lr=0.1).step(p0, g0)
        np.testing.assert_array_equal(p0["w"], [1.0])
        np.testing.assert_array_equal(g0["w"], [0.5])

    def test_separate_state(self):
        opt = S.Momentum(lr=1.0, beta=0.5)
        p = {"a": np.zeros(1), "b": np.zeros(1)}
        p = opt.step(p, {"a": np.ones(1), "b": np.zeros(1)})
        p = opt.step(p, {"a": np.zeros(1), "b": np.zeros(1)})
        np.testing.assert_allclose(p["a"], [-1.5])
        np.testing.assert_allclose(p["b"], [0.0])

    def test_faster_on_ravine(self):
        H = np.array([1.0, 50.0])
        def run(beta, lr, steps=60):
            opt = S.Momentum(lr=lr, beta=beta); p = {"x": np.array([1.0, 1.0])}
            for _ in range(steps):
                p = opt.step(p, {"x": H * p["x"]})
            return float(0.5 * (H * p["x"] ** 2).sum())
        self.assertLess(run(0.9, 0.01), run(0.0, 0.01))

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.Momentum(beta=1.0)
        with self.assertRaises(ValueError):
            S.Momentum().step({"a": np.zeros(2)}, {"a": np.zeros(3)})


if __name__ == "__main__":
    unittest.main()
