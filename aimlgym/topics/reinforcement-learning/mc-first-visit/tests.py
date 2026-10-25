"""Tests for RL-11 First-Visit Monte Carlo Prediction.

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

EPS = [[(0, 1), (1, 0), (0, 2)], [(1, 5)]]

class TestMC(unittest.TestCase):
    def test_first_visit(self):
        V, c = S.mc_prediction(EPS, 2, 1.0)
        np.testing.assert_allclose(V, [3.0, 3.5])
        np.testing.assert_array_equal(c, [1, 2])

    def test_every_visit(self):
        V, c = S.mc_prediction(EPS, 2, 1.0, first_visit=False)
        np.testing.assert_allclose(V, [2.5, 3.5])
        np.testing.assert_array_equal(c, [2, 2])

    def test_discount(self):
        V, _ = S.mc_prediction([[(0, 1), (1, 1), (2, 1)]], 3, 0.5)
        np.testing.assert_allclose(V, [1.75, 1.5, 1.0])

    def test_unvisited(self):
        V, c = S.mc_prediction(EPS, 4, 1.0)
        self.assertEqual((V[3], c[3]), (0.0, 0))

    def test_converges(self):
        rng = np.random.default_rng(0)
        eps = []
        for _ in range(4000):
            eps.append([(0, 0.0), (1, float(rng.random() < 0.3))])
        V, _ = S.mc_prediction(eps, 2, 0.9)
        self.assertAlmostEqual(V[1], 0.3, delta=0.03)
        self.assertAlmostEqual(V[0], 0.27, delta=0.03)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.mc_prediction(EPS, 2, 1.1)


if __name__ == "__main__":
    unittest.main()
