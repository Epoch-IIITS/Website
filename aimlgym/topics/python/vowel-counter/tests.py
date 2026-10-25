"""Tests for PY-13 Vowel Counter.

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


ZERO = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

class TestVowels(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.count_vowels("Banana Split!"),
                         (4, {"a": 3, "e": 0, "i": 1, "o": 0, "u": 0}))

    def test_no_vowels(self):
        self.assertEqual(S.count_vowels("rhythm"), (0, ZERO))

    def test_empty(self):
        self.assertEqual(S.count_vowels(""), (0, ZERO))

    def test_uppercase(self):
        self.assertEqual(S.count_vowels("AEIOU aeiou"),
                         (10, {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}))

    def test_keys_exact(self):
        self.assertEqual(set(S.count_vowels("xyz")[1].keys()), set("aeiou"))

    def test_total_matches(self):
        total, counts = S.count_vowels("Machine Learning")
        self.assertEqual(total, sum(counts.values()))
        self.assertEqual(total, 6)


if __name__ == "__main__":
    unittest.main()
