"""Tests for PY-26 Inheritance, Special Methods and Dataclasses.

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


class TestShapes(unittest.TestCase):
    def test_rectangle(self):
        r = S.Rectangle(2, 3)
        self.assertEqual((r.area(), r.perimeter()), (6, 10))
        self.assertEqual(r.describe(), "rectangle with area 6.00")

    def test_square_inherits(self):
        sq = S.Square(2)
        self.assertIsInstance(sq, S.Rectangle)
        self.assertIsInstance(sq, S.Shape)
        self.assertEqual((sq.width, sq.height, sq.perimeter()), (2, 2, 8))
        self.assertEqual(sq.describe(), "square with area 4.00")

    def test_circle(self):
        c = S.Circle(1)
        self.assertAlmostEqual(c.area(), math.pi)
        self.assertAlmostEqual(c.perimeter(), 2 * math.pi)
        self.assertEqual(c.describe(), "circle with area 3.14")

    def test_base_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            S.Shape().area()

    def test_equality_and_sorting(self):
        self.assertEqual(S.Rectangle(1, 4), S.Square(2))
        self.assertNotEqual(S.Square(1), S.Square(2))
        self.assertFalse(S.Square(1) == "square")
        shapes = sorted([S.Square(2), S.Circle(1), S.Rectangle(1, 1)])
        self.assertEqual([s.name for s in shapes], ["rectangle", "circle", "square"])

    def test_total_area(self):
        self.assertAlmostEqual(S.total_area([S.Square(1), S.Rectangle(2, 5)]), 11)
        self.assertEqual(S.total_area([]), 0)

    def test_point_dataclass(self):
        self.assertEqual(S.Point(1, 2), S.Point(1, 2))
        self.assertEqual(repr(S.Point(1, 2)), "Point(x=1, y=2)")
        self.assertAlmostEqual(S.Point(0, 0).distance_to(S.Point(3, 4)), 5.0)


if __name__ == "__main__":
    unittest.main()
