"""Tests for ML-05 Seeded Train/Test Split.

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

X = np.arange(40).reshape(20, 2)
y = np.array([0] * 15 + [1] * 5)

class TestSplit(unittest.TestCase):
    def test_sizes(self):
        Xtr, Xte, ytr, yte = S.train_test_split(X, y, test_size=0.25, seed=0)
        self.assertEqual((len(Xtr), len(Xte), len(ytr), len(yte)), (15, 5, 15, 5))

    def test_disjoint_cover(self):
        Xtr, Xte, _, _ = S.train_test_split(X, y, seed=3)
        rows = sorted(Xtr[:, 0].tolist() + Xte[:, 0].tolist())
        self.assertEqual(rows, list(range(0, 40, 2)))

    def test_alignment(self):
        Xtr, Xte, ytr, yte = S.train_test_split(X, y, seed=5)
        np.testing.assert_array_equal(ytr, (Xtr[:, 0] // 2 >= 15).astype(int))
        np.testing.assert_array_equal(yte, (Xte[:, 0] // 2 >= 15).astype(int))

    def test_reproducible(self):
        a = S.train_test_split(X, y, seed=9)
        b = S.train_test_split(X, y, seed=9)
        np.testing.assert_array_equal(a[1], b[1])

    def test_recipe(self):
        perm = np.random.default_rng(2).permutation(20)
        _, Xte, _, _ = S.train_test_split(X, y, test_size=0.25, seed=2)
        np.testing.assert_array_equal(Xte, X[perm[:5]])

    def test_stratified(self):
        _, _, ytr, yte = S.train_test_split(X, y, test_size=0.4, seed=1, stratify=True)
        self.assertEqual((int((yte == 1).sum()), int((yte == 0).sum())), (2, 6))
        self.assertEqual(int((ytr == 1).sum()), 3)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.train_test_split(X, y[:5])
        with self.assertRaises(ValueError):
            S.train_test_split(X, y, test_size=1.0)


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_same_contract(self):
        import numpy as np
        from sklearn.model_selection import train_test_split as sk_split
        X = np.arange(40).reshape(20, 2)
        y = np.array([0] * 12 + [1] * 8)
        for split in (S.train_test_split(X, y, test_size=0.25, seed=0, stratify=True),
                      sk_split(X, y, test_size=0.25, random_state=0, stratify=y)):
            Xtr, Xte, ytr, yte = split
            self.assertEqual(sorted(np.concatenate([Xtr[:, 0], Xte[:, 0]]).tolist()), X[:, 0].tolist())
            self.assertEqual(np.bincount(yte).tolist(), [3, 2])


if __name__ == "__main__":
    unittest.main()
