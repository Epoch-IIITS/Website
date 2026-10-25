"""Tests for FL-12 Secure Aggregation with Pairwise Masks.

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

UPS = [np.array([1., 2.]), np.array([3., 4.]), np.array([5., 6.])]

class TestSecAgg(unittest.TestCase):
    def test_full_sum(self):
        masked = {i: S.mask_update(i, UPS[i], 3, 7) for i in range(3)}
        np.testing.assert_allclose(S.aggregate(masked, 3, 2, 7), [9., 12.], atol=1e-10)

    def test_individual_hidden(self):
        for i in range(3):
            self.assertGreater(np.linalg.norm(S.mask_update(i, UPS[i], 3, 7) - UPS[i]), 0.1)

    def test_dropout(self):
        masked = {i: S.mask_update(i, UPS[i], 3, 7) for i in (0, 2)}
        np.testing.assert_allclose(S.aggregate(masked, 3, 2, 7, dropped=[1]), [6., 8.], atol=1e-10)

    def test_dropout_uncorrected_is_wrong(self):
        masked = {i: S.mask_update(i, UPS[i], 3, 7) for i in (0, 2)}
        self.assertGreater(np.linalg.norm(S.aggregate(masked, 3, 2, 7) - np.array([6., 8.])), 1e-3)

    def test_many_clients_two_drops(self):
        rng = np.random.default_rng(0)
        ups = [rng.normal(size=5) for _ in range(8)]
        alive = [0, 1, 3, 4, 6, 7]
        masked = {i: S.mask_update(i, ups[i], 8, 11) for i in alive}
        np.testing.assert_allclose(S.aggregate(masked, 8, 5, 11, dropped=[2, 5]), sum(ups[i] for i in alive), atol=1e-9)

    def test_pair_mask(self):
        np.testing.assert_allclose(S.pair_mask(1, 4, 3, 9), np.random.default_rng([9, 1, 4]).normal(size=3))
        with self.assertRaises(ValueError):
            S.pair_mask(2, 2, 3, 0)

    def test_single_client_no_mask(self):
        np.testing.assert_allclose(S.mask_update(0, np.array([1., 2.]), 1, 0), [1., 2.])


if __name__ == "__main__":
    unittest.main()
