"""Tests for CV-24 Non-Maximum Suppression.

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

B = np.array([[0, 0, 2, 2], [0.1, 0, 2.1, 2], [5, 5, 6, 6]])

class TestNMS(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.nms(B, np.array([0.9, 0.8, 0.7])), [0, 2])

    def test_order_by_score(self):
        self.assertEqual(S.nms(B, np.array([0.5, 0.95, 0.99])), [2, 1])

    def test_threshold_high_keeps_all(self):
        self.assertEqual(S.nms(B, np.array([0.9, 0.8, 0.7]), iou_threshold=0.95), [0, 1, 2])

    def test_score_threshold(self):
        self.assertEqual(S.nms(B, np.array([0.9, 0.8, 0.1]), score_threshold=0.5), [0])

    def test_chain(self):
        boxes = np.array([[0, 0, 4, 4], [2, 0, 6, 4], [4, 0, 8, 4]])
        self.assertEqual(S.nms(boxes, np.array([0.9, 0.8, 0.7]), iou_threshold=0.3), [0, 2])

    def test_empty(self):
        self.assertEqual(S.nms(np.zeros((0, 4)), np.zeros(0)), [])

    def test_ties_lower_index(self):
        self.assertEqual(S.nms(np.array([[0, 0, 2, 2], [0, 0, 2, 2]]), np.array([0.5, 0.5])), [0])

    def test_mismatch(self):
        with self.assertRaises(ValueError):
            S.nms(B, np.array([0.1]))


if __name__ == "__main__":
    unittest.main()
