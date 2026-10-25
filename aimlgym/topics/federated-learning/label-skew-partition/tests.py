"""Tests for FL-04 Label-Skewed (non-IID) Partition.

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

class TestShard(unittest.TestCase):
    def test_one_class_each(self):
        labels = np.array([0, 1, 2, 3, 4] * 2)
        C = S.label_counts(labels, S.shard_partition(labels, 5, 1, 0), 5)
        np.testing.assert_array_equal(C.max(axis=1), 2)
        np.testing.assert_array_equal((C > 0).sum(axis=1), 1)

    def test_cover(self):
        labels = np.random.default_rng(0).integers(0, 10, 300)
        parts = S.shard_partition(labels, 10, 2, 1)
        self.assertEqual(sorted(np.concatenate(parts).tolist()), list(range(300)))

    def test_skewed_vs_iid(self):
        labels = np.repeat(np.arange(10), 30)
        C = S.label_counts(labels, S.shard_partition(labels, 10, 2, 3), 10)
        self.assertLessEqual((C > 0).sum(axis=1).max(), 3)

    def test_recipe(self):
        labels = np.array([2, 0, 1, 0, 2, 1])
        order = np.argsort(labels, kind="stable")
        shards = np.array_split(order, 3)
        ids = np.random.default_rng(5).permutation(3)
        exp = [np.sort(shards[i]) for i in ids]
        for p, e in zip(S.shard_partition(labels, 3, 1, 5), exp):
            np.testing.assert_array_equal(p, e)

    def test_counts_shape(self):
        labels = np.array([0, 1, 1])
        self.assertEqual(S.label_counts(labels, [np.array([0]), np.array([1, 2])], 3).tolist(), [[1, 0, 0], [0, 2, 0]])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.shard_partition(np.arange(3), 2, 2, 0)


if __name__ == "__main__":
    unittest.main()
