"""Tests for NL-15 A Text Classification Pipeline.

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

def reviews(seed=0, n=200):
    """Synthetic product reviews: positive and negative phrases mixed with neutral filler."""
    import random
    rng = random.Random(seed)
    good = ["great", "excellent", "love it", "works perfectly", "highly recommend", "fantastic", "very happy"]
    bad = ["terrible", "broke quickly", "waste of money", "very disappointed", "awful", "does not work", "poor quality"]
    filler = ["the phone", "this charger", "the delivery", "my order", "the battery", "the screen", "it", "the case"]
    texts, labels = [], []
    for i in range(n):
        label = i % 2
        words = rng.sample(good if label else bad, 2) + rng.sample(filler, 2)
        rng.shuffle(words)
        texts.append(" ".join(words))
        labels.append(label)
    return texts, labels


class TestTextClassifier(unittest.TestCase):
    def test_accuracy_on_new_reviews(self):
        texts, labels = reviews(0)
        pipe = S.train_text_classifier(texts, labels)
        test_texts, test_labels = reviews(1, 100)
        self.assertGreater(np.mean(pipe.predict(test_texts) == np.array(test_labels)), 0.95)

    def test_pipeline_structure(self):
        texts, labels = reviews(2, 40)
        pipe = S.train_text_classifier(texts, labels, C=3.0)
        self.assertEqual(list(pipe.named_steps), ["tfidf", "clf"])
        self.assertEqual(pipe.named_steps["tfidf"].ngram_range, (1, 2))
        self.assertTrue(pipe.named_steps["tfidf"].sublinear_tf)
        self.assertEqual(pipe.named_steps["clf"].C, 3.0)

    def test_top_features_make_sense(self):
        texts, labels = reviews(3)
        top = S.top_features(S.train_text_classifier(texts, labels), n=8)
        good = {"great", "excellent", "love", "love it", "fantastic", "happy", "very happy", "recommend", "highly", "highly recommend", "perfectly", "works perfectly", "works"}
        bad = {"terrible", "awful", "broke", "broke quickly", "quickly", "waste", "money", "waste of", "of money", "disappointed", "very disappointed", "poor", "quality", "poor quality", "does", "not", "work", "does not", "not work"}
        self.assertGreater(len(set(top["positive"]) & good), 4)
        self.assertGreater(len(set(top["negative"]) & bad), 4)

    def test_top_features_order_and_types(self):
        texts, labels = reviews(4, 60)
        pipe = S.train_text_classifier(texts, labels)
        top = S.top_features(pipe, n=3)
        names = list(pipe.named_steps["tfidf"].get_feature_names_out())
        w = pipe.named_steps["clf"].coef_[0]
        pos = [w[names.index(t)] for t in top["positive"]]
        self.assertEqual(pos, sorted(pos, reverse=True))
        self.assertTrue(all(type(t) is str for t in top["positive"] + top["negative"]))

    def test_probabilities(self):
        texts, labels = reviews(5, 60)
        proba = S.train_text_classifier(texts, labels).predict_proba(["great and fantastic", "awful and terrible"])
        self.assertTrue(np.allclose(proba.sum(axis=1), 1))
        self.assertGreater(proba[0, 1], proba[1, 1])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.train_text_classifier(["a b", "c d"], [1, 1])
        with self.assertRaises(ValueError):
            S.train_text_classifier(["a b"], [0, 1])


if __name__ == "__main__":
    unittest.main()
