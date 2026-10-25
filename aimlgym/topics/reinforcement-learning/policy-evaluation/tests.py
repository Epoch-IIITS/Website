"""Tests for RL-08 Iterative Policy Evaluation.

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

CORR = {0: {0: [(1.0, 1, -1.0, False)]}, 1: {0: [(1.0, 2, 10.0, True)]}, 2: {0: [(1.0, 2, 0.0, True)]}}

class TestPolicyEval(unittest.TestCase):
    def test_corridor(self):
        V, _ = S.policy_evaluation(CORR, np.ones((3, 1)), gamma=0.9)
        np.testing.assert_allclose(V, [8., 10., 0.])

    def test_stochastic_policy(self):
        P = {0: {0: [(1.0, 1, 1.0, True)], 1: [(1.0, 1, 3.0, True)]}, 1: {0: [(1.0, 1, 0.0, True)], 1: [(1.0, 1, 0.0, True)]}}
        V, _ = S.policy_evaluation(P, np.array([[0.25, 0.75], [0.5, 0.5]]), gamma=0.5)
        np.testing.assert_allclose(V, [2.5, 0.0])

    def test_stochastic_transitions(self):
        P = {0: {0: [(0.5, 0, 1.0, False), (0.5, 1, 0.0, True)]}, 1: {0: [(1.0, 1, 0.0, True)]}}
        V, _ = S.policy_evaluation(P, np.ones((2, 1)), gamma=0.9)
        self.assertAlmostEqual(V[0], 0.5 / (1 - 0.45), places=8)

    def test_bellman_fixed_point(self):
        P = {0: {0: [(1.0, 0, 1.0, False)]}}
        V, _ = S.policy_evaluation(P, np.ones((1, 1)), gamma=0.8)
        self.assertAlmostEqual(V[0], 5.0, places=8)

    def test_iterations_reported(self):
        _, it = S.policy_evaluation(CORR, np.ones((3, 1)), gamma=0.9)
        self.assertTrue(1 <= it <= 5)

    def test_bad_policy(self):
        with self.assertRaises(ValueError):
            S.policy_evaluation(CORR, np.full((3, 1), 0.5))


if __name__ == "__main__":
    unittest.main()
