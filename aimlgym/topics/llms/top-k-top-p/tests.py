"""Tests for LM-13 Top-k and Top-p Filtering.

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

P = np.array([0.5, 0.2, 0.15, 0.1, 0.05])

class TestSampling(unittest.TestCase):
    def test_top_k(self):
        np.testing.assert_allclose(S.top_k_filter(P, 2), [0.5 / 0.7, 0.2 / 0.7, 0, 0, 0])

    def test_top_k_ties(self):
        np.testing.assert_allclose(S.top_k_filter(np.array([0.25, 0.25, 0.5]), 2), [1 / 3, 0, 2 / 3])

    def test_top_p(self):
        np.testing.assert_allclose(S.top_p_filter(P, 0.8), [0.5 / 0.85, 0.2 / 0.85, 0.15 / 0.85, 0, 0])

    def test_top_p_exact_boundary(self):
        np.testing.assert_allclose(S.top_p_filter(P, 0.7), [0.5 / 0.7, 0.2 / 0.7, 0, 0, 0])

    def test_top_p_keeps_one(self):
        np.testing.assert_allclose(S.top_p_filter(P, 0.01), [1, 0, 0, 0, 0])

    def test_top_p_full(self):
        np.testing.assert_allclose(S.top_p_filter(P, 1.0), P)

    def test_order_preserved(self):
        p = np.array([0.1, 0.6, 0.3])
        np.testing.assert_allclose(S.top_k_filter(p, 2), [0, 2 / 3, 1 / 3])

    def test_sample(self):
        self.assertEqual(S.sample(P, 0.6), 1)
        self.assertEqual(S.sample(P, 0.0), 0)
        self.assertEqual(S.sample(P, 0.999), 4)
        self.assertEqual(S.sample(S.top_k_filter(P, 1), 0.99), 0)

    def test_sample_frequencies(self):
        rng = np.random.default_rng(0)
        draws = np.bincount([S.sample(P, rng.random()) for _ in range(20000)], minlength=5) / 20000
        np.testing.assert_allclose(draws, P, atol=0.015)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.top_k_filter(P, 0)
        with self.assertRaises(ValueError):
            S.top_p_filter(P, 0)


if __name__ == "__main__":
    unittest.main()
