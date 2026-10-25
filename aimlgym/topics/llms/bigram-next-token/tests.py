"""Tests for LM-02 Next-Token Probabilities (Add-k).

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


B = {("like", "tea"): 1, ("like", "coffee"): 1, ("i", "like"): 2}
VOCAB = ["tea", "coffee", "i", "like"]

class TestNextToken(unittest.TestCase):
    def test_example(self):
        d = S.next_token_dist(B, "like", VOCAB)
        self.assertAlmostEqual(d["tea"], 2 / 6)
        self.assertAlmostEqual(d["i"], 1 / 6)

    def test_sums_to_one(self):
        for prev in ["like", "i", "tea", "unknown"]:
            self.assertAlmostEqual(sum(S.next_token_dist(B, prev, VOCAB, 0.5).values()), 1.0)

    def test_full_vocab(self):
        self.assertEqual(set(S.next_token_dist(B, "i", VOCAB)), set(VOCAB))

    def test_unseen_context_uniform(self):
        d = S.next_token_dist(B, "zzz", VOCAB)
        for v in d.values():
            self.assertAlmostEqual(v, 0.25)

    def test_mle(self):
        d = S.next_token_dist(B, "i", VOCAB, k=0)
        self.assertEqual(d["like"], 1.0)
        self.assertEqual(d["tea"], 0.0)

    def test_mle_unseen_raises(self):
        with self.assertRaises(ValueError):
            S.next_token_dist(B, "zzz", VOCAB, k=0)

    def test_smaller_k_sharper(self):
        a = S.next_token_dist(B, "i", VOCAB, 1.0)["like"]
        b = S.next_token_dist(B, "i", VOCAB, 0.1)["like"]
        self.assertGreater(b, a)


if __name__ == "__main__":
    unittest.main()
