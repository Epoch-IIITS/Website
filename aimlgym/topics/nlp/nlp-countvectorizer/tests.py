"""Tests for NL-03 Counting Words with Counter and CountVectorizer.

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


from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer


class TestCounting(unittest.TestCase):
    def test_count_matrix_example(self):
        vocab, rows = S.count_matrix(["The cat sat on the mat", "The dog sat"], stop_words="english")
        self.assertEqual(vocab, ["cat", "dog", "mat", "sat"])
        self.assertEqual(rows, [[1, 0, 1, 1], [0, 1, 0, 1]])

    def test_top_words(self):
        texts = ["the cat and the hat", "The cat sat", "a dog"]
        self.assertEqual(S.top_words(texts, 2), [("the", 3), ("cat", 2)])
        self.assertEqual(S.top_words(texts, 2, stop_words={"the", "and", "a"}), [("cat", 2), ("dog", 1)])

    def test_top_words_ties_alphabetical(self):
        self.assertEqual(S.top_words(["b a c", "c b a"], 3), [("a", 2), ("b", 2), ("c", 2)])

    def test_min_df(self):
        vocab, rows = S.count_matrix(["red apple", "green apple", "red car"], min_df=2)
        self.assertEqual(vocab, ["apple", "red"])
        self.assertEqual(rows, [[1, 1], [1, 0], [0, 1]])

    def test_single_letters_dropped_and_types(self):
        vocab, rows = S.count_matrix(["I saw a cat", "a cat saw me"])
        self.assertNotIn("i", vocab)
        self.assertNotIn("a", vocab)
        self.assertTrue(all(type(v) is int for row in rows for v in row))
        self.assertTrue(all(type(w) is str for w in vocab))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.count_matrix([])
        with self.assertRaises(ValueError):
            S.top_words(["x"], 0)


if __name__ == "__main__":
    unittest.main()
