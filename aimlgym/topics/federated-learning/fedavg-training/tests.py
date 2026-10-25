"""Tests for FL-10 Full FedAvg Training Loop.

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

def make_clients(skew=False, seed=0):
    rng = np.random.default_rng(seed)
    cl = []
    for k in range(5):
        if skew:
            X = np.column_stack([rng.normal(k - 2, 0.3, 20), rng.normal(2 - k, 0.3, 20)])
        else:
            X = rng.normal(size=(20, 2))
        cl.append((X, X @ np.array([2., -1.])))
    return cl

class TestFedAvgTrain(unittest.TestCase):
    def test_global_loss(self):
        cl = [(np.eye(2), np.array([1., 0.])), (np.array([[1., 1.]]), np.array([3.]))]
        self.assertAlmostEqual(S.global_loss(np.zeros(2), cl), (1 + 0 + 9) / 3)

    def test_converges_iid(self):
        w, h = S.train_fedavg(make_clients(), np.zeros(2), 40, 1.0, 0.05, 2, 5, 0)
        np.testing.assert_allclose(w, [2, -1], atol=1e-4)
        self.assertLess(h[-1], 1e-6)

    def test_partial_participation(self):
        w, h = S.train_fedavg(make_clients(), np.zeros(2), 80, 0.4, 0.05, 1, 5, 1)
        self.assertEqual(len(h), 80)
        self.assertLess(h[-1], 1e-3 * h[0])

    def test_reproducible(self):
        a = S.train_fedavg(make_clients(), np.zeros(2), 5, 0.6, 0.05, 1, 4, 3)
        b = S.train_fedavg(make_clients(), np.zeros(2), 5, 0.6, 0.05, 1, 4, 3)
        np.testing.assert_array_equal(a[0], b[0])

    def test_first_round_matches_manual(self):
        cl = make_clients()
        w, h = S.train_fedavg(cl, np.zeros(2), 1, 0.4, 0.05, 1, 5, 2)
        chosen = S.sample_clients(5, 0.4, 2, 0)
        locs = [S.local_sgd(np.zeros(2), *cl[k], 0.05, 1, 5, 2 * 1000 + 0 * 5 + int(k)) for k in chosen]
        np.testing.assert_allclose(w, sum(locs) / len(locs))

    def test_noniid_still_learns(self):
        _, h = S.train_fedavg(make_clients(skew=True), np.zeros(2), 60, 1.0, 0.02, 3, 5, 0)
        self.assertLess(h[-1], h[0])


if __name__ == "__main__":
    unittest.main()
