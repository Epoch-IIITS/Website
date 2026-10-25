"""Tests for NL-19 Word Embeddings in PyTorch.

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
import torch

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


class TestEmbeddingBag(unittest.TestCase):
    def test_vocab_order(self):
        vocab = S.build_vocab(["b a", "a c", "a b"])
        self.assertEqual(vocab, {"<unk>": 0, "a": 1, "b": 2, "c": 3})
        self.assertEqual(S.build_vocab(["x y x"], min_count=2), {"<unk>": 0, "x": 1})

    def test_encode_offsets_and_unknown(self):
        vocab = {"<unk>": 0, "phone": 1, "good": 2, "bad": 3}
        ids, offsets = S.encode(["good phone", "bad", "excellent phone"], vocab)
        self.assertEqual(ids.tolist(), [2, 1, 3, 0, 1])
        self.assertEqual(offsets.tolist(), [0, 2, 3])
        self.assertEqual((ids.dtype, offsets.dtype), (torch.long, torch.long))

    def test_model_output_and_mean(self):
        torch.manual_seed(0)
        model = S.BagClassifier(5, 4, 2)
        out = model(torch.tensor([1, 2, 3]), torch.tensor([0, 2]))
        self.assertEqual(tuple(out.shape), (2, 2))
        emb = model.embedding.weight
        expected = model.fc((emb[1] + emb[2]) / 2)
        self.assertTrue(torch.allclose(out[0], expected, atol=1e-6))

    def test_learns_reviews(self):
        texts, labels = reviews(0)
        model, vocab, history = S.train_bag(texts, labels, epochs=40)
        test_texts, test_labels = reviews(1, 100)
        ids, offsets = S.encode(test_texts, vocab)
        with torch.no_grad():
            preds = model(ids, offsets).argmax(dim=1).numpy()
        self.assertGreater(np.mean(preds == np.array(test_labels)), 0.9)
        self.assertLess(history[-1], history[0])

    def test_reproducible_and_eval(self):
        texts, labels = reviews(2, 40)
        a = S.train_bag(texts, labels, epochs=5, seed=1)
        b = S.train_bag(texts, labels, epochs=5, seed=1)
        self.assertEqual(a[2], b[2])
        self.assertFalse(a[0].training)

    def test_empty_text_is_zero_bag(self):
        model = S.BagClassifier(3, 2, 2)
        ids, offsets = S.encode(["", "a"], {"<unk>": 0, "a": 1})
        out = model.embedding(ids, offsets)
        self.assertEqual(out[0].tolist(), [0.0, 0.0])


if __name__ == "__main__":
    unittest.main()
