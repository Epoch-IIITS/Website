"""Tests for LM-04 Greedy Decoding.

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


import numpy as np

VOCAB = ["i", "like", "tea", "</s>"]
TABLE = {"i": [0, 5, 1, 0], "like": [0, 0, 3, 1], "tea": [0, 0, 0, 9], "</s>": [1, 0, 0, 0]}
F = lambda toks: np.array(TABLE[toks[-1]], float)

class TestGreedy(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.greedy_decode(F, ["i"], VOCAB), ["i", "like", "tea", "</s>"])

    def test_max_new(self):
        self.assertEqual(S.greedy_decode(F, ["i"], VOCAB, max_new=2), ["i", "like", "tea"])

    def test_zero_new(self):
        self.assertEqual(S.greedy_decode(F, ["i"], VOCAB, max_new=0), ["i"])

    def test_loop_capped(self):
        loop = lambda toks: np.array([0, 1, 0, 0], float)
        self.assertEqual(S.greedy_decode(loop, ["i"], VOCAB, max_new=3), ["i", "like", "like", "like"])

    def test_tie_lowest_index(self):
        tie = lambda toks: np.array([0, 2, 2, 0], float) if len(toks) < 2 else np.array([0, 0, 0, 1], float)
        self.assertEqual(S.greedy_decode(tie, ["i"], VOCAB), ["i", "like", "</s>"])

    def test_uses_full_context(self):
        seen = []
        def f(toks):
            seen.append(list(toks)); return np.array([0, 0, 0, 1], float)
        S.greedy_decode(f, ["i", "like"], VOCAB)
        self.assertEqual(seen, [["i", "like"]])

    def test_prompt_not_mutated(self):
        p = ["i"]
        S.greedy_decode(F, p, VOCAB)
        self.assertEqual(p, ["i"])

    def test_bad_logits(self):
        with self.assertRaises(ValueError):
            S.greedy_decode(lambda t: np.zeros(3), ["i"], VOCAB)


if __name__ == "__main__":
    unittest.main()
