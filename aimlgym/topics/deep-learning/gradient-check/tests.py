"""Tests for DL-13 Gradient Checking by Hand.

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

sq = lambda v: float((v ** 2).sum())

class TestGradCheck(unittest.TestCase):
    def test_rel_error(self):
        self.assertAlmostEqual(S.relative_error(2.0, 1.0), 1 / 3)
        self.assertEqual(S.relative_error(0.0, 0.0), 0.0)

    def test_correct(self):
        self.assertLess(S.grad_check(sq, lambda v: 2 * v, np.array([1., -2.]))["max_rel_error"], 1e-8)

    def test_buggy(self):
        r = S.grad_check(sq, lambda v: v, np.array([1., -2.]))
        self.assertAlmostEqual(r["max_rel_error"], 1 / 3, places=6)

    def test_worst_index_2d(self):
        def bad(v):
            g = 2 * v; g[1, 0] += 5; return g
        r = S.grad_check(sq, bad, np.ones((2, 3)))
        self.assertEqual(r["worst_index"], (1, 0))

    def test_no_mutation(self):
        x = np.array([0.5, 1.5])
        S.grad_check(sq, lambda v: 2 * v, x)
        np.testing.assert_array_equal(x, [0.5, 1.5])

    def test_numerical_returned(self):
        r = S.grad_check(lambda v: float(np.sin(v).sum()), np.cos, np.array([0.3, 1.2]))
        np.testing.assert_allclose(r["numerical"], np.cos([0.3, 1.2]), atol=1e-9)

    def test_softmax_ce(self):
        y = 2
        def f(z):
            s = z - z.max(); return float(-(s[y] - np.log(np.exp(s).sum())))
        def g(z):
            p = np.exp(z - z.max()); p /= p.sum(); p[y] -= 1; return p
        self.assertLess(S.grad_check(f, g, np.array([0.1, -0.4, 0.9, 2.0]))["max_rel_error"], 1e-7)


if __name__ == "__main__":
    unittest.main()
