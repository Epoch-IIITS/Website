"""Tests for DL-16 The Adam Optimiser.

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


class TestAdam(unittest.TestCase):
    def test_first_step_is_lr_sign(self):
        opt = S.Adam(lr=0.1)
        out = opt.step({"w": np.array([1.0, 1.0, 1.0])}, {"w": np.array([4.0, -0.01, 0.0])})
        np.testing.assert_allclose(out["w"], [0.9, 1.1, 1.0], atol=1e-6)
        self.assertEqual(opt.t, 1)

    def test_matches_reference_recurrence(self):
        opt = S.Adam(lr=0.05, beta1=0.8, beta2=0.99, eps=1e-6)
        p = {"a": np.array([0.5, -1.0])}
        m = v = np.zeros(2)
        ref = p["a"].copy()
        for t, g in enumerate([np.array([1.0, 2.0]), np.array([-0.5, 1.0]), np.array([0.2, 0.2])], 1):
            p = opt.step(p, {"a": g})
            m = 0.8 * m + 0.2 * g
            v = 0.99 * v + 0.01 * g * g
            ref = ref - 0.05 * (m / (1 - 0.8 ** t)) / (np.sqrt(v / (1 - 0.99 ** t)) + 1e-6)
            np.testing.assert_allclose(p["a"], ref, rtol=1e-12)

    def test_scale_invariance(self):
        a, b = S.Adam(lr=0.01), S.Adam(lr=0.01)
        p = {"w": np.array([2.0])}
        pa, pb = dict(p), dict(p)
        for g in (0.3, -0.1, 0.7):
            pa = a.step(pa, {"w": np.array([g])})
            pb = b.step(pb, {"w": np.array([g * 1000])})
        np.testing.assert_allclose(pa["w"], pb["w"], rtol=1e-6)

    def test_minimises_quadratic(self):
        opt = S.Adam(lr=0.1)
        p = {"w": np.array([5.0, -3.0])}
        for _ in range(500):
            p = opt.step(p, {"w": 2 * (p["w"] - np.array([1.0, 2.0]))})
        np.testing.assert_allclose(p["w"], [1.0, 2.0], atol=1e-2)

    def test_does_not_mutate_and_counts_once(self):
        opt = S.Adam()
        params = {"w": np.ones(2), "b": np.zeros(1)}
        opt.step(params, {"w": np.ones(2), "b": np.ones(1)})
        np.testing.assert_array_equal(params["w"], np.ones(2))
        self.assertEqual(opt.t, 1)

    def test_validation(self):
        for kwargs in ({"lr": 0}, {"beta1": 1.0}, {"beta2": -0.1}):
            with self.assertRaises(ValueError):
                S.Adam(**kwargs)
        opt = S.Adam()
        with self.assertRaises(ValueError):
            opt.step({"w": np.ones(2)}, {"b": np.ones(2)})
        with self.assertRaises(ValueError):
            opt.step({"w": np.ones(2)}, {"w": np.ones(3)})


try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_matches_torch_adam(self):
        w0 = np.array([0.5, -2.0, 3.0])
        grads = [np.array([1.0, -1.0, 0.5]), np.array([0.2, 0.3, -0.4]), np.array([-1.0, 2.0, 0.0])]
        ours = S.Adam(lr=0.01)
        p = {"w": w0}
        tw = torch.tensor(w0, requires_grad=True)
        topt = torch.optim.Adam([tw], lr=0.01)
        for g in grads:
            p = ours.step(p, {"w": g})
            topt.zero_grad()
            tw.grad = torch.tensor(g)
            topt.step()
        np.testing.assert_allclose(p["w"], tw.detach().numpy(), rtol=1e-7)


if __name__ == "__main__":
    unittest.main()
