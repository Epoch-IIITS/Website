"""Tests for FL-01 IID Client Partitioning.

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

class TestIID(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual(S.client_sizes(S.iid_partition(10, 3, 0)), [4, 3, 3])

    def test_cover_disjoint(self):
        parts = S.iid_partition(53, 7, seed=4)
        allidx = np.concatenate(parts)
        self.assertEqual(sorted(allidx.tolist()), list(range(53)))
        self.assertEqual(len(set(allidx.tolist())), 53)

    def test_recipe(self):
        perm = np.random.default_rng(2).permutation(12)
        parts = S.iid_partition(12, 4, 2)
        for p, q in zip(parts, np.array_split(perm, 4)):
            np.testing.assert_array_equal(p, np.sort(q))

    def test_reproducible(self):
        a, b = S.iid_partition(20, 5, 9), S.iid_partition(20, 5, 9)
        for p, q in zip(a, b):
            np.testing.assert_array_equal(p, q)

    def test_one_client(self):
        np.testing.assert_array_equal(S.iid_partition(5, 1, 0)[0], np.arange(5))

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.iid_partition(3, 4, 0)


if __name__ == "__main__":
    unittest.main()
