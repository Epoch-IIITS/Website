"""Tests for CV-25 Connected Components with OpenCV.

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


def scene():
    mask = np.zeros((30, 30), np.uint8)
    mask[5:10, 4:12] = 255
    mask[14:18, 14:18] = 255
    mask[25, 25] = 255
    return mask


class TestLabelObjects(unittest.TestCase):
    def test_counts_and_areas(self):
        r = S.label_objects(scene())
        self.assertEqual(r["count"], 3)
        self.assertEqual(r["areas"], [40, 16, 1])

    def test_boxes_and_centroids(self):
        r = S.label_objects(scene())
        self.assertEqual(r["boxes"][:2], [(4, 5, 8, 5), (14, 14, 4, 4)])
        self.assertAlmostEqual(r["centroids"][0][0], 7.5)
        self.assertAlmostEqual(r["centroids"][1][1], 15.5)

    def test_min_area(self):
        r = S.label_objects(scene(), min_area=20)
        self.assertEqual((r["count"], r["areas"]), (1, [40]))

    def test_connectivity(self):
        diagonal = np.zeros((4, 4), np.uint8)
        diagonal[0, 0] = diagonal[1, 1] = diagonal[2, 2] = 255
        self.assertEqual(S.label_objects(diagonal, connectivity=8)["count"], 1)
        self.assertEqual(S.label_objects(diagonal, connectivity=4)["count"], 3)

    def test_types_and_empty(self):
        r = S.label_objects(scene())
        self.assertTrue(all(type(v) is int for box in r["boxes"] for v in box))
        self.assertTrue(all(type(v) is float for c in r["centroids"] for v in c))
        self.assertEqual(S.label_objects(np.zeros((5, 5), np.uint8))["count"], 0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.label_objects(scene(), connectivity=6)
        with self.assertRaises(ValueError):
            S.label_objects(scene().astype(np.int32))


if __name__ == "__main__":
    unittest.main()
