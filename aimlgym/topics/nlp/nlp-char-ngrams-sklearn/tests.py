"""Tests for NL-05 Character n-grams with CountVectorizer.

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


class TestCharNgrams(unittest.TestCase):
    def test_cat_bigrams(self):
        features, rows = S.char_ngrams(["cat"], 2, 2)
        self.assertEqual(features, [" c", "at", "ca", "t "])
        self.assertEqual(rows, [[1, 1, 1, 1]])

    def test_range_includes_both_sizes(self):
        features, _ = S.char_ngrams(["cat"], 2, 3)
        self.assertEqual(features, [" c", " ca", "at", "at ", "ca", "cat", "t "])

    def test_word_boundaries(self):
        features, _ = S.char_ngrams(["ab cd"], 2, 2)
        self.assertEqual(features, [" a", " c", "ab", "b ", "cd", "d "])

    def test_typo_closer_than_unrelated(self):
        typo = S.char_similarity("receive", "recieve")
        other = S.char_similarity("receive", "banana")
        self.assertGreater(typo, 0.3)
        self.assertLess(other, 0.1)

    def test_identical_and_type(self):
        self.assertAlmostEqual(S.char_similarity("hello", "hello"), 1.0)
        self.assertIs(type(S.char_similarity("a b", "b a")), float)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.char_ngrams(["x"], 3, 2)
        with self.assertRaises(ValueError):
            S.char_similarity("a", "b", 0)


if __name__ == "__main__":
    unittest.main()
