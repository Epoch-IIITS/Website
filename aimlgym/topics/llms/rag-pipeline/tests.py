"""Tests for LM-21 Retrieval-Augmented Generation by Hand.

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


CHUNKS = ["Paris is the capital of France.",
          "Bananas are yellow and rich in potassium.",
          "Berlin is the capital of Germany.",
          "France borders Germany and Spain."]


def scripted_model(prompt):
    if "Paris" in prompt:
        return "The capital of France is Paris [1]."
    return "I don't know."


class TestRag(unittest.TestCase):
    def test_chunking(self):
        text = " ".join(f"w{i}" for i in range(10))
        self.assertEqual(S.chunk_words(text, 4, 1), ["w0 w1 w2 w3", "w3 w4 w5 w6", "w6 w7 w8 w9"])
        self.assertEqual(S.chunk_words(text, 4, 0)[-1], "w8 w9")
        self.assertEqual(S.chunk_words("", 3, 1), [])
        with self.assertRaises(ValueError):
            S.chunk_words(text, 3, 3)

    def test_retrieve_ranking(self):
        hits = S.retrieve("What is the capital of France?", CHUNKS, 2)
        self.assertEqual([i for i, _ in hits], [0, 2])
        self.assertGreater(hits[0][1], hits[1][1])
        self.assertIsInstance(hits[0][1], float)

    def test_retrieve_scores_are_cosines(self):
        hits = S.retrieve("bananas yellow", CHUNKS, 4)
        self.assertEqual(hits[0][0], 1)
        self.assertTrue(all(0.0 <= s <= 1.0 + 1e-12 for _, s in hits))
        self.assertEqual([s for _, s in hits[1:]], [0.0, 0.0, 0.0])
        self.assertEqual([i for i, _ in hits[1:]], [0, 2, 3])

    def test_prompt(self):
        p = S.build_prompt("Q?", ["alpha", "beta"])
        self.assertEqual(p, "Answer using only the sources below. Cite sources like [1].\n[1] alpha\n[2] beta\nQuestion: Q?")

    def test_answer_grounded(self):
        calls = []
        def model(prompt):
            calls.append(prompt)
            return scripted_model(prompt)
        out = S.answer("capital of France", CHUNKS, model, k=2)
        self.assertEqual(len(calls), 1)
        self.assertIn("[1] Paris is the capital of France.", calls[0])
        self.assertEqual(out["sources"], [0, 2])
        self.assertEqual((out["cited"], out["grounded"]), ([1], True))

    def test_answer_ungrounded(self):
        out = S.answer("capital of France", CHUNKS, lambda p: "Paris [1][3]", k=2)
        self.assertEqual(out["cited"], [1, 3])
        self.assertFalse(out["grounded"])
        self.assertFalse(S.answer("capital of France", CHUNKS, lambda p: "Paris", k=2)["grounded"])


try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import linear_kernel
except ImportError:
    TfidfVectorizer = None


@unittest.skipIf(TfidfVectorizer is None, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_scores_match_tfidf_vectorizer(self):
        vec = TfidfVectorizer(token_pattern=r"[a-z0-9]+")
        M = vec.fit_transform(CHUNKS)
        query = "is France the capital of Germany"
        expected = linear_kernel(vec.transform([query]), M)[0]
        for i, score in S.retrieve(query, CHUNKS, len(CHUNKS)):
            self.assertAlmostEqual(score, float(expected[i]), places=10)


if __name__ == "__main__":
    unittest.main()
