"""Tests for ML-06 Confusion Matrix, Precision, Recall, F1.

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

YT, YP = [0, 0, 1, 1, 2], [0, 1, 1, 1, 0]

class TestClsMetrics(unittest.TestCase):
    def test_cm(self):
        np.testing.assert_array_equal(S.confusion_matrix(YT, YP, 3), [[1, 1, 0], [0, 2, 0], [1, 0, 0]])

    def test_precision_recall(self):
        r = S.classification_report(YT, YP, 3)
        np.testing.assert_allclose(r["precision"], [0.5, 2 / 3, 0.0])
        np.testing.assert_allclose(r["recall"], [0.5, 1.0, 0.0])

    def test_f1_macro(self):
        r = S.classification_report(YT, YP, 3)
        np.testing.assert_allclose(r["f1"], [0.5, 0.8, 0.0])
        self.assertAlmostEqual(r["macro_f1"], 1.3 / 3)

    def test_accuracy(self):
        self.assertAlmostEqual(S.classification_report(YT, YP, 3)["accuracy"], 0.6)

    def test_unused_class(self):
        r = S.classification_report([0, 1], [0, 1], 3)
        np.testing.assert_allclose(r["f1"], [1, 1, 0])

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            S.confusion_matrix([0, 3], [0, 1], 3)

    def test_cm_total(self):
        rng = np.random.default_rng(0)
        a, b = rng.integers(0, 4, 50), rng.integers(0, 4, 50)
        C = S.confusion_matrix(a, b, 4)
        self.assertEqual(C.sum(), 50)
        np.testing.assert_array_equal(C.sum(axis=1), np.bincount(a, minlength=4))


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn(self):
        import numpy as np
        from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support
        yt = [0, 1, 2, 2, 1, 0, 2, 3]
        yp = [0, 2, 2, 2, 1, 1, 0, 0]
        np.testing.assert_array_equal(S.confusion_matrix(yt, yp, 4), confusion_matrix(yt, yp, labels=range(4)))
        rep = S.classification_report(yt, yp, 4)
        p, r, f, _ = precision_recall_fscore_support(yt, yp, labels=range(4), zero_division=0)
        np.testing.assert_allclose(rep["precision"], p)
        np.testing.assert_allclose(rep["recall"], r)
        np.testing.assert_allclose(rep["f1"], f)
        self.assertAlmostEqual(rep["macro_f1"], f1_score(yt, yp, labels=range(4), average="macro", zero_division=0))


if __name__ == "__main__":
    unittest.main()
