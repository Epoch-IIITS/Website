"""Tests for LM-06 Byte-Pair Encoding Merges.

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


WC = {"low": 5, "lower": 2, "newest": 6, "widest": 3}

class TestBPE(unittest.TestCase):
    def test_first_merges(self):
        self.assertEqual(S.learn_bpe(WC, 3), [("e", "s"), ("es", "t"), ("est", "</w>")])

    def test_apply(self):
        self.assertEqual(S.apply_bpe("lowest", S.learn_bpe(WC, 3)), ["l", "o", "w", "est</w>"])

    def test_more_merges(self):
        m = S.learn_bpe(WC, 5)
        self.assertEqual(m[3:], [("l", "o"), ("lo", "w")])
        self.assertEqual(S.apply_bpe("low", m), ["low", "</w>"])

    def test_no_merges(self):
        self.assertEqual(S.apply_bpe("abc", []), ["a", "b", "c", "</w>"])

    def test_early_stop(self):
        self.assertEqual(S.learn_bpe({"a": 1}, 10), [("a", "</w>")])

    def test_overlap(self):
        self.assertEqual(S.apply_bpe("aaa", [("a", "a")]), ["aa", "a", "</w>"])

    def test_frequency_weighting(self):
        self.assertEqual(S.learn_bpe({"ab": 1, "cd": 5}, 1), [("c", "d")])

    def test_tie_lexicographic(self):
        self.assertEqual(S.learn_bpe({"xy": 1, "ab": 1}, 1), [("a", "b")])


if __name__ == "__main__":
    unittest.main()
