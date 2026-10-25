"""Tests for LM-01 Vocabularies and Token IDs.

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


TEXTS = ["the cat sat", "The dog", "a cat"]


class TestTokenIds(unittest.TestCase):
    def test_vocab_order(self):
        v = S.build_vocab(TEXTS)
        self.assertEqual(list(v)[:4], ["<pad>", "<unk>", "<bos>", "<eos>"])
        self.assertEqual(v, {"<pad>": 0, "<unk>": 1, "<bos>": 2, "<eos>": 3,
                             "cat": 4, "the": 5, "a": 6, "dog": 7, "sat": 8})

    def test_min_count(self):
        v = S.build_vocab(TEXTS, min_count=2)
        self.assertEqual(set(v) - set(S.SPECIALS), {"cat", "the"})

    def test_encode_unknown(self):
        v = S.build_vocab(TEXTS)
        self.assertEqual(S.encode("The bird", v), [2, 5, 1, 3])
        self.assertEqual(S.encode("cat", v, add_special=False), [4])

    def test_round_trip(self):
        v = S.build_vocab(TEXTS)
        self.assertEqual(S.decode(S.encode("the dog sat", v), v), "the dog sat")
        self.assertEqual(S.decode([2, 4, 0, 3], v, skip_special=False), "<bos> cat <pad> <eos>")

    def test_pad_batch(self):
        padded, mask = S.pad_batch([[2, 4, 3], [2, 3], [2, 5, 6, 7, 3]])
        self.assertEqual(padded, [[2, 4, 3, 0, 0], [2, 3, 0, 0, 0], [2, 5, 6, 7, 3]])
        self.assertEqual(mask, [[1, 1, 1, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 1]])

    def test_pad_custom_and_empty(self):
        self.assertEqual(S.pad_batch([[1], [1, 2]], pad_id=-1)[0], [[1, -1], [1, 2]])
        self.assertEqual(S.pad_batch([]), ([], []))


if __name__ == "__main__":
    unittest.main()
