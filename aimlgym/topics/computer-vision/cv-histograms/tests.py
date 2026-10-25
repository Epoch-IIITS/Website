"""Tests for CV-08 Histograms and Equalisation.

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


class TestHistograms(unittest.TestCase):
    def test_worked_example(self):
        r = S.histogram_and_equalise(np.array([[0, 50], [50, 100]], np.uint8))
        self.assertEqual(r["equalized"].tolist(), [[0, 170], [170, 255]])

    def test_matches_bincount(self):
        rng = np.random.default_rng(0)
        gray = rng.integers(0, 256, size=(30, 40), dtype=np.uint8)
        r = S.histogram_and_equalise(gray)
        self.assertEqual(r["hist"], np.bincount(gray.ravel(), minlength=256).tolist())

    def test_coarse_bins(self):
        gray = np.array([[0, 63, 64, 255]], np.uint8)
        self.assertEqual(S.histogram_and_equalise(gray, bins=4)["hist"], [2, 1, 0, 1])

    def test_equalisation_spreads_and_keeps_order(self):
        rng = np.random.default_rng(1)
        gray = rng.integers(100, 140, size=(50, 50)).astype(np.uint8)
        eq = S.histogram_and_equalise(gray)["equalized"]
        self.assertEqual((int(eq.min()), int(eq.max())), (0, 255))
        order = np.argsort(gray.ravel(), kind="stable")
        self.assertTrue(np.all(np.diff(eq.ravel()[order].astype(int)) >= 0))

    def test_types(self):
        r = S.histogram_and_equalise(np.zeros((3, 3), np.uint8))
        self.assertTrue(all(type(v) is int for v in r["hist"]))
        self.assertEqual(sum(r["hist"]), 9)
        self.assertEqual(r["equalized"].dtype, np.uint8)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.histogram_and_equalise(np.zeros((2, 2, 3), np.uint8))
        with self.assertRaises(ValueError):
            S.histogram_and_equalise(np.zeros((2, 2), np.uint8), bins=0)


if __name__ == "__main__":
    unittest.main()
