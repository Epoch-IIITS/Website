"""Tests for NP-01 Create an Array and Inspect It.

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

class TestArrayInfo(unittest.TestCase):
    def test_2d(self):
        self.assertEqual(S.describe(S.to_array([[1, 2, 3], [4, 5, 6]])),
                         {"shape": (2, 3), "ndim": 2, "size": 6, "dtype": "float64"})

    def test_1d_int(self):
        d = S.describe(S.to_array([1, 2], dtype=int))
        self.assertEqual(d["shape"], (2,))
        self.assertTrue(d["dtype"].startswith("int"))

    def test_column(self):
        self.assertEqual(S.describe(S.to_array([[7], [8], [9]]))["shape"], (3, 1))

    def test_ragged(self):
        with self.assertRaises(ValueError):
            S.to_array([[1, 2], [3]])

    def test_returns_ndarray(self):
        a = S.to_array([[1.5, 2.5]])
        self.assertIsInstance(a, np.ndarray)
        np.testing.assert_array_equal(a, np.array([[1.5, 2.5]]))

    def test_bool_dtype(self):
        self.assertEqual(S.describe(S.to_array([1, 0, 1], dtype=bool))["dtype"], "bool")

    def test_3d(self):
        d = S.describe(S.to_array([[[1, 2]], [[3, 4]], [[5, 6]]]))
        self.assertEqual((d["shape"], d["ndim"], d["size"]), ((3, 1, 2), 3, 6))


if __name__ == "__main__":
    unittest.main()
