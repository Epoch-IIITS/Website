"""Tests for FL-03 Client Updates as Deltas.

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

class TestDelta(unittest.TestCase):
    def test_delta(self):
        np.testing.assert_allclose(S.client_delta(np.array([1., 2.]), np.array([1.5, 0.])), [0.5, -2.])

    def test_server_lr(self):
        out = S.server_update(np.zeros(2), [np.array([1., 1.]), np.array([3., -1.])], [1, 1], server_lr=0.5)
        np.testing.assert_allclose(out, [1., 0.])

    def test_equals_fedavg(self):
        rng = np.random.default_rng(0)
        g = rng.normal(size=4); locals_ = [rng.normal(size=4) for _ in range(3)]; sizes = [5, 1, 14]
        deltas = [S.client_delta(g, l) for l in locals_]
        fedavg = sum(n * l for n, l in zip(sizes, locals_)) / sum(sizes)
        np.testing.assert_allclose(S.server_update(g, deltas, sizes), fedavg)

    def test_no_mutation(self):
        g = np.zeros(2)
        S.server_update(g, [np.ones(2)], [1])
        np.testing.assert_array_equal(g, [0, 0])

    def test_zero_lr(self):
        np.testing.assert_allclose(S.server_update(np.array([3.]), [np.array([9.])], [2], server_lr=0.0), [3.])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.client_delta(np.ones(2), np.ones(3))
        with self.assertRaises(ValueError):
            S.server_update(np.ones(2), [], [])


if __name__ == "__main__":
    unittest.main()
