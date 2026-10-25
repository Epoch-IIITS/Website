"""Tests for NL-12 Levenshtein Edit Distance.

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


class TestLev(unittest.TestCase):
    def test_classic(self):
        self.assertEqual(S.levenshtein("kitten", "sitting"), 3)

    def test_empty(self):
        self.assertEqual(S.levenshtein("", "abc"), 3)
        self.assertEqual(S.levenshtein("", ""), 0)

    def test_symmetric(self):
        self.assertEqual(S.levenshtein("flaw", "lawn"), S.levenshtein("lawn", "flaw"))
        self.assertEqual(S.levenshtein("flaw", "lawn"), 2)

    def test_identical(self):
        self.assertEqual(S.levenshtein("same", "same"), 0)

    def test_suggest(self):
        self.assertEqual(S.suggest("teh", ["the", "tea", "ten", "apple"], 2), ["tea", "ten", "the"])

    def test_suggest_ordering(self):
        self.assertEqual(S.suggest("cat", ["cart", "cat", "act", "dog"], 2), ["cat", "cart", "act"])

    def test_triangle(self):
        a, b, c = "intention", "execution", "extension"
        self.assertLessEqual(S.levenshtein(a, c), S.levenshtein(a, b) + S.levenshtein(b, c))
        self.assertEqual(S.levenshtein(a, b), 5)


if __name__ == "__main__":
    unittest.main()
