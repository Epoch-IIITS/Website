"""Tests for NL-18 Word Embedding Analogies.

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

EMB = {"man": np.array([1., 0, 0]), "woman": np.array([1., 1, 0]),
       "king": np.array([1., 0, 1]), "queen": np.array([1., 1, 1]),
       "apple": np.array([0., 0, -1]), "zero": np.zeros(3)}

class TestEmbeddings(unittest.TestCase):
    def test_analogy(self):
        self.assertEqual(S.analogy("man", "woman", "king", EMB), "queen")

    def test_analogy_reverse(self):
        self.assertEqual(S.analogy("woman", "man", "queen", EMB), "king")

    def test_excludes_inputs(self):
        emb = {"a": np.array([1., 0]), "b": np.array([1., 0.1]), "c": np.array([0., 1]), "d": np.array([-1., 0])}
        self.assertNotIn(S.analogy("a", "b", "c", emb), {"a", "b", "c"})

    def test_most_similar(self):
        r = S.most_similar("king", EMB, k=2)
        self.assertEqual(r[0][0], "queen")
        self.assertAlmostEqual(r[0][1], 2 / np.sqrt(6))
        self.assertNotIn("king", [w for w, _ in S.most_similar("king", EMB, k=10)])

    def test_zero_vector(self):
        self.assertEqual(dict(S.most_similar("man", EMB, k=10))["zero"], 0.0)

    def test_ties_alphabetical(self):
        emb = {"q": np.array([1., 0]), "b": np.array([0., 1]), "a": np.array([0., -1])}
        self.assertEqual([w for w, _ in S.most_similar("q", emb, k=2)], ["a", "b"])

    def test_unknown(self):
        with self.assertRaises(KeyError):
            S.most_similar("xyz", EMB)


if __name__ == "__main__":
    unittest.main()
