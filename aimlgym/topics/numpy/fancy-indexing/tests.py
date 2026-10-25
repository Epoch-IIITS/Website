"""Tests for NP-09 Fancy Indexing and Gather.

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

P = np.array([[0.1, 0.7, 0.2], [0.5, 0.3, 0.2]])

class TestFancy(unittest.TestCase):
    def test_gather(self):
        X = np.arange(12).reshape(4, 3)
        np.testing.assert_array_equal(S.gather_rows(X, [3, 0, 3]), [[9, 10, 11], [0, 1, 2], [9, 10, 11]])

    def test_pick(self):
        np.testing.assert_allclose(S.pick_per_row(P, [1, 0]), [0.7, 0.5])

    def test_pick_shape(self):
        self.assertEqual(S.pick_per_row(P, [2, 2]).shape, (2,))

    def test_pick_bad(self):
        with self.assertRaises(ValueError):
            S.pick_per_row(P, [0])

    def test_topk_ties(self):
        np.testing.assert_array_equal(S.top_k(np.array([3, 9, 9, 1]), 2), [1, 2])

    def test_topk_all(self):
        np.testing.assert_array_equal(S.top_k(np.array([0.2, 0.9, 0.5]), 3), [1, 2, 0])

    def test_topk_bad(self):
        with self.assertRaises(ValueError):
            S.top_k(np.array([1, 2]), 3)


if __name__ == "__main__":
    unittest.main()
