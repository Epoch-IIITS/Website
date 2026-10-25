"""Tests for PY-15 Importing the Standard Library.

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


import heapq
import itertools
import random


class TestStandardLibrary(unittest.TestCase):
    def test_hypotenuse(self):
        self.assertAlmostEqual(S.hypotenuse(3, 4), 5.0)
        self.assertAlmostEqual(S.hypotenuse(1, 1), math.sqrt(2))

    def test_pages_needed(self):
        self.assertEqual(S.pages_needed(21, 10), 3)
        self.assertEqual(S.pages_needed(20, 10), 2)
        self.assertEqual(S.pages_needed(0, 10), 0)
        self.assertEqual(S.pages_needed(1, 10), 1)

    def test_most_common_letter(self):
        self.assertEqual(S.most_common_letter("Hello, World"), "l")

    def test_most_common_tie_and_case(self):
        self.assertEqual(S.most_common_letter("bBaA!"), "a")
        self.assertIsNone(S.most_common_letter("123 !?"))

    def test_dice_reproducible(self):
        rng = random.Random(7)
        expected = [int(rng.random() * 6) + 1 for _ in range(20)]
        self.assertEqual(S.dice_rolls(7, 20), expected)
        self.assertEqual(S.dice_rolls(7, 20), S.dice_rolls(7, 20))

    def test_dice_range(self):
        rolls = S.dice_rolls(1, 600)
        self.assertEqual(len(rolls), 600)
        self.assertEqual(set(rolls), {1, 2, 3, 4, 5, 6})

    def test_smallest_k(self):
        self.assertEqual(S.smallest_k([5, 1, 4, 1], 2), [1, 1])
        nums = [9, 3, 7, 3, 8, 1]
        self.assertEqual(S.smallest_k(nums, 3), sorted(nums)[:3])

    def test_all_pairs(self):
        self.assertEqual(S.all_pairs(["a", "b", "c"]), [("a", "b"), ("a", "c"), ("b", "c")])
        self.assertEqual(S.all_pairs([1]), [])
        self.assertEqual(len(S.all_pairs(list(range(6)))), 15)


if __name__ == "__main__":
    unittest.main()
