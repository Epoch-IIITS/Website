"""Tests for NL-04 Stopwords and Word Counts.

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


TOKS = ["the", "cat", "and", "the", "hat", "cat", "sat"]

class TestCounts(unittest.TestCase):
    def test_remove(self):
        self.assertEqual(S.remove_stopwords(TOKS, {"the", "and"}), ["cat", "hat", "cat", "sat"])

    def test_top(self):
        self.assertEqual(S.top_words(TOKS, 2, {"the", "and"}), [("cat", 2), ("hat", 1)])

    def test_no_stopwords(self):
        self.assertEqual(S.top_words(TOKS, 1), [("cat", 2)])
        self.assertEqual(S.top_words(TOKS, 2), [("cat", 2), ("the", 2)])

    def test_n_larger(self):
        self.assertEqual(len(S.top_words(["a", "b"], 10)), 2)

    def test_empty(self):
        self.assertEqual(S.top_words([], 3), [])

    def test_bad_n(self):
        with self.assertRaises(ValueError):
            S.top_words(TOKS, 0)

    def test_order_independent(self):
        self.assertEqual(S.top_words(["b", "a", "b", "a"], 2), [("a", 2), ("b", 2)])


from collections import Counter


class TestAgainstLibrary(unittest.TestCase):
    def test_library_counts_match_counter(self):
        tokens = "the cat and the dog and the bird saw a cat".split()
        top = S.top_words(tokens, 10, stopwords={"the", "and", "a"})
        expected = Counter(t for t in tokens if t not in {"the", "and", "a"})
        self.assertEqual(dict(top), dict(expected))


if __name__ == "__main__":
    unittest.main()
