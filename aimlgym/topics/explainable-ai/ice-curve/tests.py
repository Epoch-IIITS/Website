"""Tests for XA-04 Individual Conditional Expectation.

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

class TestICE(unittest.TestCase):
    def test_example(self):
        f = lambda X: X[:, 0] * X[:, 1]
        np.testing.assert_allclose(S.ice_curve(f, np.array([2., 3.]), 0, [0, 1, 2]), [0, 3, 6])

    def test_single_call(self):
        calls = []
        def f(X):
            calls.append(X.shape); return X.sum(axis=1)
        S.ice_curve(f, np.array([1., 2., 3.]), 2, [0, 5, 10, 15])
        self.assertEqual(calls, [(4, 3)])

    def test_no_mutation(self):
        x = np.array([1., 2.])
        S.ice_curve(lambda X: X[:, 0], x, 0, [9, 9])
        np.testing.assert_array_equal(x, [1., 2.])

    def test_other_features_fixed(self):
        seen = {}
        def f(X):
            seen["X"] = X.copy(); return X[:, 0]
        S.ice_curve(f, np.array([7., 8., 9.]), 1, [0, 1])
        np.testing.assert_array_equal(seen["X"][:, [0, 2]], [[7, 9], [7, 9]])

    def test_flat_for_unused_feature(self):
        r = S.ice_curve(lambda X: 2 * X[:, 0], np.array([1., 1.]), 1, np.linspace(-5, 5, 11))
        np.testing.assert_allclose(r, 2.0)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.ice_curve(lambda X: X[:, 0], np.array([1.]), 3, [1])
        with self.assertRaises(ValueError):
            S.ice_curve(lambda X: X[:, 0], np.array([1.]), 0, [])


if __name__ == "__main__":
    unittest.main()
