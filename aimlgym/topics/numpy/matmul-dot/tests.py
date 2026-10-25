"""Tests for NP-06 Matrix Products with @.

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


class TestMatmul(unittest.TestCase):
    def test_small(self):
        out = S.matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        np.testing.assert_array_equal(out, [[19, 22], [43, 50]])
        self.assertIsInstance(out, np.ndarray)

    def test_loops_match_numpy(self):
        rng = np.random.default_rng(0)
        A = rng.integers(-5, 5, size=(4, 3)).tolist()
        B = rng.integers(-5, 5, size=(3, 6)).tolist()
        self.assertEqual(S.matmul_loops(A, B), S.matmul(A, B).tolist())

    def test_not_elementwise(self):
        A = np.array([[1, 2], [3, 4]])
        self.assertFalse(np.array_equal(S.matmul(A, A), A * A))

    def test_shape_error(self):
        with self.assertRaises(ValueError) as ctx:
            S.matmul(np.ones((3, 2)), np.ones((3, 2)))
        self.assertIn("(3, 2)", str(ctx.exception))
        with self.assertRaises(ValueError):
            S.matmul_loops([[1, 2]], [[1, 2]])

    def test_rectangular_shape(self):
        self.assertEqual(S.matmul(np.ones((2, 5)), np.ones((5, 3))).shape, (2, 3))

    def test_batch_scores(self):
        np.testing.assert_allclose(S.batch_scores([[1, 2], [3, 4], [5, 6]], [0.5, -1.0], 0.1), [-1.4, -2.4, -3.4])
        self.assertEqual(S.batch_scores(np.ones((7, 3)), np.ones(3), 0).shape, (7,))

    def test_gram(self):
        X = np.array([[1.0, 2.0], [3.0, 4.0], [0.0, 1.0]])
        G = S.gram(X)
        self.assertEqual(G.shape, (3, 3))
        np.testing.assert_allclose(G, G.T)
        self.assertAlmostEqual(G[0, 1], 1 * 3 + 2 * 4)


class TestAgainstLibrary(unittest.TestCase):
    def test_equivalent_spellings(self):
        A = np.arange(6.0).reshape(2, 3)
        B = np.arange(12.0).reshape(3, 4)
        out = S.matmul(A, B)
        np.testing.assert_allclose(out, np.dot(A, B))
        np.testing.assert_allclose(out, np.einsum("ik,kj->ij", A, B))


if __name__ == "__main__":
    unittest.main()
