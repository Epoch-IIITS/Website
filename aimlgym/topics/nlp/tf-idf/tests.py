"""Tests for NL-09 TF-IDF.

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

class TestTFIDF(unittest.TestCase):
    def test_example(self):
        W, idf = S.tfidf(np.array([[1, 1], [2, 0]]))
        np.testing.assert_allclose(idf, [1.0, np.log(1.5) + 1])
        np.testing.assert_allclose(W, [[1 / np.hypot(1, idf[1]), idf[1] / np.hypot(1, idf[1])], [1, 0]])

    def test_unit_rows(self):
        W, _ = S.tfidf(np.array([[3, 0, 1], [0, 2, 2], [1, 1, 1]]))
        np.testing.assert_allclose(np.linalg.norm(W, axis=1), 1.0)

    def test_empty_doc(self):
        W, _ = S.tfidf(np.array([[0, 0], [1, 0]]))
        np.testing.assert_array_equal(W[0], [0, 0])

    def test_common_term_lower_weight(self):
        W, idf = S.tfidf(np.array([[1, 1], [1, 0], [1, 0]]))
        self.assertGreater(idf[1], idf[0])
        self.assertGreater(W[0, 1], W[0, 0])

    def test_idf_formula(self):
        _, idf = S.tfidf(np.array([[1, 0, 0], [1, 1, 0], [1, 1, 0], [0, 0, 1]]))
        np.testing.assert_allclose(idf, np.log(5 / (1 + np.array([3, 2, 1]))) + 1)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.tfidf(np.array([[-1, 2]]))


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_tfidf_transformer(self):
        import numpy as np
        from sklearn.feature_extraction.text import TfidfTransformer
        counts = np.array([[3, 0, 1, 0], [2, 1, 0, 0], [0, 0, 4, 1], [1, 1, 1, 1]])
        W, idf = S.tfidf(counts)
        t = TfidfTransformer().fit(counts)
        np.testing.assert_allclose(idf, t.idf_)
        np.testing.assert_allclose(W, t.transform(counts).toarray(), atol=1e-12)


if __name__ == "__main__":
    unittest.main()
