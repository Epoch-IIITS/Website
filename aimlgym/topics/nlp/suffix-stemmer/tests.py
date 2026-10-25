"""Tests for NL-13 Rule-Based Suffix Stemmer.

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


PAIRS_1A = {"caresses": "caress", "ponies": "poni", "ties": "ti", "caress": "caress", "cats": "cat"}
PAIRS_1B = {"feed": "feed", "agreed": "agree", "plastered": "plaster", "bled": "bled",
            "motoring": "motor", "sing": "sing", "conflated": "conflate", "troubled": "trouble",
            "sized": "size", "hopping": "hop", "tanned": "tan", "falling": "fall",
            "hissing": "hiss", "fizzed": "fizz", "failing": "fail", "filing": "file"}

class TestPorter(unittest.TestCase):
    def test_measure(self):
        for w, m in {"tr": 0, "tree": 0, "y": 0, "by": 0, "trouble": 1, "oats": 1, "trees": 1,
                     "ivy": 1, "troubles": 2, "private": 2, "oaten": 2, "orrery": 2}.items():
            self.assertEqual(S.measure(w), m, w)

    def test_y_consonant(self):
        self.assertTrue(S.is_consonant("toy", 2))
        self.assertFalse(S.is_consonant("syzygy", 1))
        self.assertTrue(S.is_consonant("yes", 0))

    def test_step1a(self):
        for w, e in PAIRS_1A.items():
            self.assertEqual(S.step1ab(w), e, w)

    def test_step1b(self):
        for w, e in PAIRS_1B.items():
            self.assertEqual(S.step1ab(w), e, w)

    def test_eed_blocks_ed(self):
        self.assertEqual(S.step1ab("feed"), "feed")

    def test_no_vowel_stem_kept(self):
        self.assertEqual(S.step1ab("bled"), "bled")
        self.assertEqual(S.step1ab("sing"), "sing")

    def test_short(self):
        self.assertEqual(S.step1ab("s"), "")
        self.assertEqual(S.step1ab("as"), "a")


if __name__ == "__main__":
    unittest.main()
