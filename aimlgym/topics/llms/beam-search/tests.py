"""Tests for LM-14 Beam Search.

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

VOCAB = ["a", "b", "</s>"]
TABLE = {"<s>": [0.6, 0.4, 1e-9], "a": [0.3, 0.3, 0.4], "b": [0.05, 0.05, 0.9]}
def F(t):
    return np.log(np.array(TABLE.get(t[-1], [1e-9, 1e-9, 1.0])))

class TestBeam(unittest.TestCase):
    def test_beats_greedy(self):
        toks, score = S.beam_search(F, ["<s>"], VOCAB, beam_width=2, max_new=3)
        self.assertEqual(toks, ["<s>", "b", "</s>"])
        self.assertAlmostEqual(score, np.log(0.36))

    def test_width1_is_greedy(self):
        toks, score = S.beam_search(F, ["<s>"], VOCAB, beam_width=1, max_new=3)
        self.assertEqual(toks, ["<s>", "a", "</s>"])
        self.assertAlmostEqual(score, np.log(0.24))

    def test_max_new_limit(self):
        toks, _ = S.beam_search(F, ["<s>"], VOCAB, beam_width=2, max_new=1)
        self.assertEqual(toks, ["<s>", "a"])

    def test_finished_not_extended(self):
        calls = []
        def f(t):
            calls.append(tuple(t)); return F(t)
        S.beam_search(f, ["<s>"], VOCAB, beam_width=2, max_new=5)
        self.assertFalse(any(c[-1] == "</s>" for c in calls))

    def test_tie_break(self):
        g = lambda t: np.log(np.array([0.5, 0.5, 1e-12])) if len(t) == 1 else np.log(np.array([1e-12, 1e-12, 1.0]))
        toks, _ = S.beam_search(g, ["<s>"], VOCAB, beam_width=1, max_new=2)
        self.assertEqual(toks, ["<s>", "a", "</s>"])

    def test_score_is_sum_logprobs(self):
        toks, score = S.beam_search(F, ["<s>"], VOCAB, beam_width=3, max_new=2)
        exp = sum(F(toks[:i])[VOCAB.index(toks[i])] for i in range(1, len(toks)))
        self.assertAlmostEqual(score, exp)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.beam_search(F, ["<s>"], VOCAB, beam_width=0)


if __name__ == "__main__":
    unittest.main()
