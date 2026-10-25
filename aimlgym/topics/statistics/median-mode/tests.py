"""Tests for ST-02 Median and Mode.

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


class TestMedianMode(unittest.TestCase):
    def test_odd(self):
        self.assertEqual(S.median([7, 1, 3, 3, 100]), 3.0)

    def test_even(self):
        self.assertEqual(S.median([4, 1, 2, 3]), 2.5)

    def test_single(self):
        self.assertEqual(S.median([42]), 42.0)

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.median([])

    def test_not_modified(self):
        d = [3, 1, 2]
        S.median(d)
        self.assertEqual(d, [3, 1, 2])

    def test_modes_tie(self):
        self.assertEqual(S.modes([3, 3, 1, 2, 2]), [2, 3])

    def test_modes_single_and_empty(self):
        self.assertEqual(S.modes([5]), [5])
        self.assertEqual(S.modes([]), [])

    def test_all_unique(self):
        self.assertEqual(S.modes([4, 2, 9]), [2, 4, 9])


import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_statistics(self):
        for data in ([3, 1, 4, 1, 5, 9, 2, 6], [7], [2, 2, 3, 3, 1]):
            self.assertAlmostEqual(S.median(data), statistics.median(data))
            self.assertEqual(S.modes(data), sorted(statistics.multimode(data)))


if __name__ == "__main__":
    unittest.main()
