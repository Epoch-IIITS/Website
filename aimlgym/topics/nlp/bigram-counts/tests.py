"""Tests for NL-08 Bigram Counts with Sentence Markers.

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


SENTS = [["i", "like", "tea"], ["i", "like", "coffee"]]

class TestBigrams(unittest.TestCase):
    def test_counts(self):
        c = S.bigram_counts(SENTS)
        self.assertEqual(c["bigrams"][("i", "like")], 2)
        self.assertEqual(c["bigrams"][("tea", "</s>")], 1)
        self.assertEqual(c["contexts"]["<s>"], 2)

    def test_prob(self):
        c = S.bigram_counts(SENTS)
        self.assertEqual(S.bigram_prob("like", "tea", c), 0.5)
        self.assertEqual(S.bigram_prob("<s>", "i", c), 1.0)

    def test_unseen_pair(self):
        self.assertEqual(S.bigram_prob("i", "tea", S.bigram_counts(SENTS)), 0.0)

    def test_unknown_context(self):
        with self.assertRaises(KeyError):
            S.bigram_prob("</s>", "i", S.bigram_counts(SENTS))

    def test_no_cross_sentence(self):
        self.assertEqual(S.bigram_counts(SENTS)["bigrams"][("tea", "i")], 0)

    def test_sums_to_one(self):
        c = S.bigram_counts([["a", "b", "a", "c"], ["a", "a"]])
        vocab = {w for pair in c["bigrams"] for w in pair}
        for ctx in c["contexts"]:
            self.assertAlmostEqual(sum(S.bigram_prob(ctx, w, c) for w in vocab), 1.0)

    def test_empty_sentence(self):
        c = S.bigram_counts([[]])
        self.assertEqual(c["bigrams"][("<s>", "</s>")], 1)


if __name__ == "__main__":
    unittest.main()
