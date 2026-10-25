"""Tests for FL-07 One FedAvg Round.

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

rng0 = np.random.default_rng(0)
CL = [(rng0.normal(size=(n, 2)), rng0.normal(size=n)) for n in (5, 12, 3)]

class TestRound(unittest.TestCase):
    def test_equals_centralised_step(self):
        w0 = np.array([0.3, -0.2])
        new, _ = S.fedavg_round(w0, CL, 0.1, 1, None, 0)
        X = np.vstack([c[0] for c in CL]); y = np.concatenate([c[1] for c in CL])
        np.testing.assert_allclose(new, w0 - 0.1 * 2 / len(y) * X.T @ (X @ w0 - y))

    def test_locals_count(self):
        _, locs = S.fedavg_round(np.zeros(2), CL, 0.05, 2, 2, 1)
        self.assertEqual(len(locs), 3)

    def test_seeds_per_client(self):
        w0 = np.zeros(2)
        _, locs = S.fedavg_round(w0, CL, 0.05, 2, 2, 7)
        for k, (X, y) in enumerate(CL):
            np.testing.assert_allclose(locs[k], S.local_sgd(w0, X, y, 0.05, 2, 2, 7 + k))

    def test_identical_clients(self):
        c = (np.eye(2), np.array([1., 2.]))
        new, locs = S.fedavg_round(np.zeros(2), [c, c], 0.1, 3, 1, 0)
        self.assertEqual(new.shape, (2,))
        np.testing.assert_allclose(new, (locs[0] + locs[1]) / 2)

    def test_weighting(self):
        new, locs = S.fedavg_round(np.zeros(2), CL, 0.05, 1, 2, 3)
        np.testing.assert_allclose(new, (5 * locs[0] + 12 * locs[1] + 3 * locs[2]) / 20)

    def test_global_unchanged(self):
        g = np.zeros(2)
        S.fedavg_round(g, CL, 0.1, 1, None, 0)
        np.testing.assert_array_equal(g, [0, 0])

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.fedavg_round(np.zeros(2), [], 0.1, 1, None, 0)


if __name__ == "__main__":
    unittest.main()
