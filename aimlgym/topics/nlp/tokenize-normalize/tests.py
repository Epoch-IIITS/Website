"""Tests for NL-02 Tokenize and Normalize.

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


class TestTokenize(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(S.normalize("Café ÉLAN"), "cafe elan")

    def test_tokens(self):
        self.assertEqual(S.tokenize("Café's menu: 2 croissants, NO coffee!"),
                         ["cafe's", "menu", "2", "croissants", "no", "coffee"])

    def test_empty_and_punct(self):
        self.assertEqual(S.tokenize(""), [])
        self.assertEqual(S.tokenize("--- ..."), [])

    def test_contraction(self):
        self.assertEqual(S.tokenize("I don't know, it's fine."), ["i", "don't", "know", "it's", "fine"])

    def test_numbers(self):
        self.assertEqual(S.tokenize("Version 3.11 in 2026"), ["version", "3", "11", "in", "2026"])

    def test_whitespace_variants(self):
        self.assertEqual(S.tokenize("a\tb\nc  d"), ["a", "b", "c", "d"])

    def test_accent_mid_word(self):
        self.assertEqual(S.tokenize("naïve résumé"), ["naive", "resume"])


if __name__ == "__main__":
    unittest.main()
