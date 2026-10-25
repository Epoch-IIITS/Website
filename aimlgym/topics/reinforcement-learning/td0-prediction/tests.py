"""Tests for RL-12 TD(0) Prediction.

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

class TestTD0(unittest.TestCase):
    def test_example(self):
        np.testing.assert_allclose(S.td0([[(0, 1.0, 1, False), (1, 2.0, 1, True)]], 2, 0.5, 1.0), [0.5, 1.0])

    def test_td_error(self):
        V = np.array([1.0, 3.0])
        self.assertAlmostEqual(S.td_error(V, 0, 0.5, 1, False, 0.9), 0.5 + 2.7 - 1.0)
        self.assertAlmostEqual(S.td_error(V, 0, 0.5, 1, True, 0.9), -0.5)

    def test_order_matters(self):
        ep = [(0, 0.0, 1, False), (1, 1.0, 1, True)]
        V1 = S.td0([ep], 2, 1.0, 1.0)
        np.testing.assert_allclose(V1, [0.0, 1.0])
        V2 = S.td0([ep], 2, 1.0, 1.0, sweeps=2)
        np.testing.assert_allclose(V2, [1.0, 1.0])

    def test_converges_chain(self):
        eps = [[(0, 0.0, 1, False), (1, 0.0, 2, False), (2, 1.0, 2, True)]] * 1
        V = S.td0(eps, 3, 0.1, 0.9, sweeps=2000)
        np.testing.assert_allclose(V, [0.81, 0.9, 1.0], atol=1e-6)

    def test_batch_td_vs_mc(self):
        eps = [[(0, 0.0, 1, False), (1, 0.0, 1, True)]] + [[(1, 1.0, 1, True)]] * 6 + [[(1, 0.0, 1, True)]]
        V = S.td0(eps, 2, 0.01, 1.0, sweeps=3000)
        self.assertAlmostEqual(V[1], 0.75, delta=0.02)
        self.assertAlmostEqual(V[0], 0.75, delta=0.03)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.td0([], 2, 0.0, 0.9)


if __name__ == "__main__":
    unittest.main()
