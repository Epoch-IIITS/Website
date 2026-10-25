"""Tests for ML-04 Splitting Data with scikit-learn.

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


class TestSplitData(unittest.TestCase):
    def test_stratified_ratio(self):
        X = np.arange(20).reshape(10, 2); y = np.array([0] * 8 + [1] * 2)
        Xtr, Xte, ytr, yte = S.split_data(X, y, test_size=0.5, seed=1, stratify=True)
        self.assertEqual(sorted(yte.tolist()), [0, 0, 0, 0, 1])
        self.assertEqual(sorted(ytr.tolist()), [0, 0, 0, 0, 1])

    def test_rows_stay_paired(self):
        X = np.arange(30).reshape(15, 2); y = X[:, 0] * 10
        Xtr, Xte, ytr, yte = S.split_data(X, y, seed=3)
        self.assertTrue(np.array_equal(ytr, Xtr[:, 0] * 10))
        self.assertTrue(np.array_equal(yte, Xte[:, 0] * 10))

    def test_sizes_and_disjoint(self):
        X = np.arange(40).reshape(20, 2); y = np.arange(20)
        Xtr, Xte, ytr, yte = S.split_data(X, y, test_size=0.25, seed=0)
        self.assertEqual((len(ytr), len(yte)), (15, 5))
        self.assertEqual(sorted(ytr.tolist() + yte.tolist()), list(range(20)))

    def test_reproducible(self):
        X = np.arange(40).reshape(20, 2); y = np.arange(20)
        a = S.split_data(X, y, seed=7)[3]
        b = S.split_data(X, y, seed=7)[3]
        c = S.split_data(X, y, seed=8)[3]
        self.assertTrue(np.array_equal(a, b))
        self.assertFalse(np.array_equal(a, c))

    def test_stratified_splits(self):
        X = np.zeros((12, 1)); y = np.array([0] * 9 + [1] * 3)
        splits = S.stratified_splits(X, y, n_splits=4, test_size=4, seed=0)
        self.assertEqual(len(splits), 4)
        for train, test in splits:
            self.assertEqual(len(test), 4)
            self.assertEqual(sorted(train + test), list(range(12)))
            self.assertEqual(sum(y[test]), 1)
            self.assertTrue(all(type(i) is int for i in train + test))

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.split_data(np.zeros((4, 1)), np.zeros(3))
        with self.assertRaises(ValueError):
            S.stratified_splits(np.zeros((4, 1)), np.zeros(3))


if __name__ == "__main__":
    unittest.main()
