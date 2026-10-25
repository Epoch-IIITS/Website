"""Tests for ML-21 Decision Stump with Gini Impurity.

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

class TestStump(unittest.TestCase):
    def test_gini(self):
        self.assertAlmostEqual(S.gini(np.array([0, 0, 1, 1])), 0.5)
        self.assertEqual(S.gini(np.array([2, 2, 2])), 0.0)
        self.assertAlmostEqual(S.gini(np.array([0, 1, 2])), 2 / 3)
        self.assertEqual(S.gini(np.array([], dtype=int)), 0.0)

    def test_perfect(self):
        self.assertEqual(S.best_split(np.array([[1], [2], [3], [4]]), np.array([0, 0, 1, 1])),
                         {"feature": 0, "threshold": 2.5, "impurity": 0.0, "left_class": 0, "right_class": 1})

    def test_second_feature(self):
        X = np.array([[5, 1], [5, 2], [5, 8], [5, 9]]); y = np.array([1, 1, 0, 0])
        r = S.best_split(X, y)
        self.assertEqual((r["feature"], r["threshold"], r["left_class"], r["right_class"]), (1, 5.0, 1, 0))

    def test_weighted_impurity(self):
        X = np.array([[1], [2], [3], [4], [5]]); y = np.array([0, 0, 1, 0, 1])
        r = S.best_split(X, y)
        self.assertAlmostEqual(r["impurity"], 4 / 15)
        self.assertEqual(r["threshold"], 2.5)

    def test_tie_lowest_feature(self):
        X = np.array([[1, 1], [2, 2]]); y = np.array([0, 1])
        self.assertEqual(S.best_split(X, y)["feature"], 0)

    def test_duplicates_midpoints(self):
        X = np.array([[1], [1], [3], [3]]); y = np.array([0, 0, 1, 1])
        self.assertEqual(S.best_split(X, y)["threshold"], 2.0)

    def test_unsplittable(self):
        with self.assertRaises(ValueError):
            S.best_split(np.array([[1], [1]]), np.array([0, 1]))


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_depth_one_tree(self):
        import numpy as np
        from sklearn.tree import DecisionTreeClassifier
        X = np.array([[2.0, 7.0], [3.0, 1.0], [5.0, 6.0], [6.0, 2.0], [8.0, 3.0], [9.0, 8.0]])
        y = np.array([0, 0, 0, 1, 1, 1])
        best = S.best_split(X, y)
        tree = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).tree_
        self.assertEqual(best["feature"], tree.feature[0])
        self.assertAlmostEqual(best["threshold"], tree.threshold[0])


if __name__ == "__main__":
    unittest.main()
