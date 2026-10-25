"""Tests for PY-16 Unique Words in Order.

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


class TestUniqueWords(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.unique_words("The cat saw the CAT, then the dog."),
                         ["the", "cat", "saw", "then", "dog"])

    def test_apostrophe_and_dash(self):
        self.assertEqual(S.unique_words("Don't stop -- don't!"), ["don't", "stop"])

    def test_empty(self):
        self.assertEqual(S.unique_words(""), [])

    def test_only_punctuation(self):
        self.assertEqual(S.unique_words("!!! ... ,"), [])

    def test_multiple_spaces(self):
        self.assertEqual(S.unique_words("a   b\tA\nb"), ["a", "b"])

    def test_order_not_sorted(self):
        self.assertEqual(S.unique_words("zebra apple zebra mango"), ["zebra", "apple", "mango"])

    def test_returns_list(self):
        self.assertIsInstance(S.unique_words("x"), list)


import string


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_dict_fromkeys(self):
        text = "The cat; the CAT and a dog, a Dog!"
        words = [w.strip(string.punctuation).lower() for w in text.split()]
        self.assertEqual(S.unique_words(text), list(dict.fromkeys(w for w in words if w)))


if __name__ == "__main__":
    unittest.main()
