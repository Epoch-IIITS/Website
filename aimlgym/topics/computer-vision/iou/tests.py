"""Tests for CV-23 Intersection over Union.

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

class TestIoU(unittest.TestCase):
    def test_example(self):
        np.testing.assert_allclose(
            S.iou_matrix(np.array([[0, 0, 2, 2]]), np.array([[1, 1, 3, 3], [5, 5, 6, 6], [0, 0, 2, 2]])),
            [[1 / 7, 0.0, 1.0]])

    def test_area(self):
        np.testing.assert_allclose(S.box_area(np.array([[0, 0, 2, 3], [1, 1, 1.5, 2]])), [6, 0.5])

    def test_degenerate(self):
        with self.assertRaises(ValueError):
            S.box_area(np.array([[0, 0, 0, 1]]))

    def test_contained(self):
        np.testing.assert_allclose(S.iou_matrix(np.array([[0, 0, 4, 4]]), np.array([[1, 1, 3, 3]])), [[4 / 16]])

    def test_touching(self):
        np.testing.assert_allclose(S.iou_matrix(np.array([[0, 0, 1, 1]]), np.array([[1, 0, 2, 1]])), [[0.0]])

    def test_symmetric_shape(self):
        rng = np.random.default_rng(0)
        xy = rng.uniform(0, 10, (5, 2)); wh = rng.uniform(1, 3, (5, 2))
        boxes = np.hstack([xy, xy + wh])
        M = S.iou_matrix(boxes, boxes[:3])
        self.assertEqual(M.shape, (5, 3))
        np.testing.assert_allclose(M[:3], M[:3].T)
        np.testing.assert_allclose(np.diag(M[:3]), 1.0)


if __name__ == "__main__":
    unittest.main()
