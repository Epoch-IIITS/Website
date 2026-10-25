"""Tests for LM-09 Sinusoidal Positional Encoding.

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

class TestPE(unittest.TestCase):
    def test_pos0(self):
        np.testing.assert_allclose(S.positional_encoding(1, 6)[0], [0, 1, 0, 1, 0, 1])

    def test_pos1(self):
        np.testing.assert_allclose(S.positional_encoding(2, 4)[1],
                                   [np.sin(1), np.cos(1), np.sin(0.01), np.cos(0.01)])

    def test_shape_bounds(self):
        pe = S.positional_encoding(50, 16)
        self.assertEqual(pe.shape, (50, 16))
        self.assertTrue((np.abs(pe) <= 1).all())

    def test_pair_norm(self):
        pe = S.positional_encoding(20, 8)
        np.testing.assert_allclose(pe[:, 0::2] ** 2 + pe[:, 1::2] ** 2, 1.0)

    def test_relative_rotation(self):
        pe = S.positional_encoding(30, 8); k = 3
        w = 1 / 10000 ** (2 * np.arange(4) / 8)
        for j in range(4):
            c, s = np.cos(k * w[j]), np.sin(k * w[j])
            R = np.array([[c, -s], [s, c]])
            for p in range(25):
                np.testing.assert_allclose(pe[p, 2*j:2*j+2] @ R, pe[p + k, 2*j:2*j+2], atol=1e-10)

    def test_distinct_positions(self):
        pe = S.positional_encoding(100, 32)
        self.assertEqual(len({tuple(np.round(r, 8)) for r in pe}), 100)

    def test_errors(self):
        for T, d in [(0, 4), (3, 5), (3, 0)]:
            with self.assertRaises(ValueError):
                S.positional_encoding(T, d)


if __name__ == "__main__":
    unittest.main()
