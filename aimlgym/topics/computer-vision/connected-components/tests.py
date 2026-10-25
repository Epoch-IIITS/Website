"""Tests for CV-26 Connected Components Labeling by Hand.

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

M = np.array([[1, 1, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1]], bool)

class TestCC(unittest.TestCase):
    def test_example(self):
        labels, sizes = S.label_components(M)
        np.testing.assert_array_equal(labels, [[1, 1, 0, 0], [0, 1, 0, 2], [0, 0, 0, 2]])
        self.assertEqual(sizes, [3, 2])

    def test_diagonal(self):
        d = np.array([[1, 0], [0, 1]], bool)
        self.assertEqual(S.label_components(d, 4)[1], [1, 1])
        self.assertEqual(S.label_components(d, 8)[1], [2])

    def test_empty(self):
        labels, sizes = S.label_components(np.zeros((3, 3), bool))
        self.assertEqual(sizes, [])
        self.assertEqual(labels.sum(), 0)

    def test_full(self):
        labels, sizes = S.label_components(np.ones((4, 5), bool))
        self.assertEqual(sizes, [20])
        self.assertTrue((labels == 1).all())

    def test_raster_order(self):
        m = np.array([[0, 0, 1], [1, 0, 0]], bool)
        np.testing.assert_array_equal(S.label_components(m)[0], [[0, 0, 1], [2, 0, 0]])

    def test_large_no_recursion(self):
        m = np.ones((200, 200), bool)
        self.assertEqual(S.label_components(m)[1], [40000])

    def test_spiral(self):
        m = np.array([[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0]], bool)
        self.assertEqual(S.label_components(m)[1], [8])

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.label_components(M, 6)


try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_ndimage_label(self):
        import numpy as np
        from scipy import ndimage
        mask = np.array([[1, 1, 0, 0, 1],
                         [0, 1, 0, 1, 1],
                         [1, 0, 0, 0, 0],
                         [1, 0, 1, 1, 0],
                         [0, 0, 0, 1, 1]], dtype=bool)
        for conn, structure in ((4, ndimage.generate_binary_structure(2, 1)), (8, np.ones((3, 3)))):
            labels, sizes = S.label_components(mask, connectivity=conn)
            ref, n = ndimage.label(mask, structure=structure)
            np.testing.assert_array_equal(labels, ref)
            self.assertEqual(len(sizes), n)


if __name__ == "__main__":
    unittest.main()
