"""Tests for NL-06 Character n-grams by Hand.

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
    def test_cat(self):
        self.assertEqual(S.char_ngrams("cat"), ["<ca", "cat", "at>"])

    def test_range(self):
        self.assertEqual(S.char_ngrams("ab", 2, 3), ["<a", "ab", "b>", "<ab", "ab>"])

    def test_short_word(self):
        self.assertEqual(S.char_ngrams("a", 4, 4), [])
        self.assertEqual(S.char_ngrams("", 2, 2), ["<>"])

    def test_count(self):
        self.assertEqual(len(S.char_ngrams("banana", 3, 3)), len("<banana>") - 2)

    def test_jaccard(self):
        self.assertAlmostEqual(S.jaccard("cat", "cart"), 1 / 6)
        self.assertEqual(S.jaccard("same", "same"), 1.0)

    def test_jaccard_disjoint_and_empty(self):
        self.assertEqual(S.jaccard("abc", "xyz"), 0.0)
        self.assertEqual(S.jaccard("a", "b", n=5), 1.0)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.char_ngrams("x", 3, 2)


if __name__ == "__main__":
    unittest.main()
