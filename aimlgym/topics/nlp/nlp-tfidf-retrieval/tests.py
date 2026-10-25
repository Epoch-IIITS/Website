"""Tests for NL-10 Search with TfidfVectorizer and Cosine Similarity.

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


DOCS = ["python lists are mutable", "tuples are immutable", "pandas dataframes hold tables",
        "lists and tuples are sequences"]


class TestTfidfSearch(unittest.TestCase):
    def test_best_match_first(self):
        index = S.build_index(DOCS)
        self.assertEqual(S.search(index, "mutable lists", k=1)[0][0], 0)
        self.assertEqual(S.search(index, "pandas tables", k=1)[0][0], 2)

    def test_scores_sorted_and_bounded(self):
        results = S.search(S.build_index(DOCS), "lists tuples", k=4)
        scores = [s for _, s in results]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertTrue(all(0.0 <= s <= 1.0 + 1e-9 for s in scores))
        self.assertEqual(results[0][0], 3)

    def test_rows_normalised(self):
        _, matrix = S.build_index(DOCS)
        self.assertTrue(np.allclose(np.linalg.norm(matrix.toarray(), axis=1), 1.0))

    def test_unknown_words(self):
        results = S.search(S.build_index(DOCS), "quantum chromodynamics", k=2)
        self.assertEqual(results, [(0, 0.0), (1, 0.0)])

    def test_k_larger_than_corpus(self):
        results = S.search(S.build_index(DOCS[:2]), "immutable", k=10)
        self.assertEqual(len(results), 2)
        self.assertIs(type(results[0][1]), float)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.build_index([])
        with self.assertRaises(ValueError):
            S.search(S.build_index(DOCS), "x", k=0)


if __name__ == "__main__":
    unittest.main()
