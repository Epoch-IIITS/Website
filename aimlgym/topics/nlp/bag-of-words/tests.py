"""Tests for NL-07 Bag-of-Words Vectors.

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

DOCS = [["a", "b", "a"], ["b", "c"]]

class TestBoW(unittest.TestCase):
    def test_vocab(self):
        self.assertEqual(S.build_vocab(DOCS), {"a": 0, "b": 1, "c": 2})

    def test_vectors(self):
        np.testing.assert_array_equal(S.vectorize(DOCS, S.build_vocab(DOCS)), [[2, 1, 0], [0, 1, 1]])

    def test_min_count(self):
        self.assertEqual(S.build_vocab(DOCS, min_count=2), {"a": 0, "b": 1})

    def test_oov(self):
        X = S.vectorize([["z", "a"]], S.build_vocab(DOCS))
        np.testing.assert_array_equal(X, [[1, 0, 0]])

    def test_empty_doc(self):
        X = S.vectorize([[]], S.build_vocab(DOCS))
        self.assertEqual(X.shape, (1, 3))
        self.assertEqual(X.sum(), 0)

    def test_alphabetical(self):
        self.assertEqual(list(S.build_vocab([["zeta", "alpha", "mid"]])), ["alpha", "mid", "zeta"])

    def test_row_sums(self):
        docs = [["x", "y", "x", "x"], ["y"]]
        np.testing.assert_array_equal(S.vectorize(docs, S.build_vocab(docs)).sum(axis=1), [4, 1])


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_count_vectorizer(self):
        import numpy as np
        from sklearn.feature_extraction.text import CountVectorizer
        docs = [["the", "cat", "sat"], ["the", "dog", "sat", "sat"], ["a", "cat"]]
        vocab = S.build_vocab(docs)
        cv = CountVectorizer(analyzer=lambda d: d).fit(docs)
        self.assertEqual(vocab, {k: int(v) for k, v in cv.vocabulary_.items()})
        np.testing.assert_array_equal(S.vectorize(docs, vocab), cv.transform(docs).toarray())


if __name__ == "__main__":
    unittest.main()
