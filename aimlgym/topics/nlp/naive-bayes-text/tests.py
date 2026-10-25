"""Tests for NL-14 Multinomial Naive Bayes Text Classifier.

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

class TestNB(unittest.TestCase):
    def test_params(self):
        m = S.MultinomialNB().fit(np.array([[3, 0], [0, 2]]), np.array(["spam", "ham"]))
        self.assertEqual(list(m.classes_), ["ham", "spam"])
        np.testing.assert_allclose(np.exp(m.feature_log_prob_), [[0.25, 0.75], [0.8, 0.2]])
        np.testing.assert_allclose(np.exp(m.class_log_prior_), [0.5, 0.5])

    def test_predict(self):
        m = S.MultinomialNB().fit(np.array([[3, 0], [0, 2]]), np.array(["spam", "ham"]))
        self.assertEqual(list(m.predict(np.array([[1, 0], [0, 1]]))), ["spam", "ham"])

    def test_log_proba_normalised(self):
        rng = np.random.default_rng(0)
        X = rng.integers(0, 4, (12, 5)); y = rng.integers(0, 3, 12)
        lp = S.MultinomialNB().fit(X, y).predict_log_proba(X)
        np.testing.assert_allclose(np.exp(lp).sum(axis=1), 1.0)

    def test_smoothing_unseen_word(self):
        m = S.MultinomialNB(alpha=1.0).fit(np.array([[2, 0, 0], [0, 2, 0]]), np.array([0, 1]))
        self.assertTrue(np.isfinite(m.predict_log_proba(np.array([[0, 0, 5]]))).all())

    def test_prior_matters(self):
        X = np.array([[1, 1]] * 3 + [[1, 1]]); y = np.array([0, 0, 0, 1])
        m = S.MultinomialNB().fit(X, y)
        self.assertEqual(m.predict(np.array([[1, 1]]))[0], 0)

    def test_long_document_no_underflow(self):
        m = S.MultinomialNB().fit(np.array([[5, 1], [1, 5]]), np.array([0, 1]))
        lp = m.predict_log_proba(np.array([[3000, 2900]]))
        self.assertTrue(np.isfinite(lp).all())

    def test_bad_alpha(self):
        with self.assertRaises(ValueError):
            S.MultinomialNB(alpha=0).fit(np.ones((2, 2)), np.array([0, 1]))


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_nb(self):
        import numpy as np
        from sklearn.naive_bayes import MultinomialNB as SkNB
        X = np.array([[2, 1, 0, 0], [3, 0, 1, 0], [0, 0, 2, 3], [0, 1, 1, 4], [1, 0, 0, 2]])
        y = np.array(["spam", "spam", "ham", "ham", "ham"])
        ours, sk = S.MultinomialNB(alpha=0.5).fit(X, y), SkNB(alpha=0.5).fit(X, y)
        np.testing.assert_allclose(ours.feature_log_prob_, sk.feature_log_prob_)
        np.testing.assert_allclose(ours.class_log_prior_, sk.class_log_prior_)
        Xt = np.array([[1, 1, 0, 0], [0, 0, 1, 1]])
        np.testing.assert_allclose(ours.predict_log_proba(Xt), sk.predict_log_proba(Xt), atol=1e-12)


if __name__ == "__main__":
    unittest.main()
