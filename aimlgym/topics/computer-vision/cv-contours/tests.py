"""Tests for CV-20 Contours and Bounding Boxes.

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


def two_rectangles():
    mask = np.zeros((30, 30), np.uint8)
    mask[5:10, 4:12] = 255          # 8 wide, 5 tall
    mask[15:27, 18:26] = 255        # 8 wide, 12 tall
    return mask


class TestFindObjects(unittest.TestCase):
    def test_boxes(self):
        objs = S.find_objects(two_rectangles())
        self.assertEqual([(o["x"], o["y"], o["w"], o["h"]) for o in objs], [(4, 5, 8, 5), (18, 15, 8, 12)])

    def test_area_and_centroid(self):
        first = S.find_objects(two_rectangles())[0]
        self.assertEqual(first["area"], 28.0)
        self.assertAlmostEqual(first["centroid"][0], 7.5)
        self.assertAlmostEqual(first["centroid"][1], 7.0)

    def test_min_area_filter(self):
        objs = S.find_objects(two_rectangles(), min_area=50)
        self.assertEqual([(o["x"], o["y"]) for o in objs], [(18, 15)])

    def test_holes_ignored(self):
        mask = np.zeros((20, 20), np.uint8)
        mask[2:18, 2:18] = 255
        mask[7:13, 7:13] = 0
        self.assertEqual(len(S.find_objects(mask)), 1)

    def test_empty_and_single_pixel(self):
        self.assertEqual(S.find_objects(np.zeros((5, 5), np.uint8)), [])
        dot = np.zeros((5, 5), np.uint8); dot[2, 3] = 255
        [obj] = S.find_objects(dot)
        self.assertEqual((obj["x"], obj["y"], obj["w"], obj["h"], obj["area"]), (3, 2, 1, 1, 0.0))
        self.assertEqual(obj["centroid"], (3.0, 2.0))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.find_objects(np.zeros((5, 5), np.float32))


if __name__ == "__main__":
    unittest.main()
