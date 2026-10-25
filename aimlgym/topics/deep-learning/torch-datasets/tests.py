"""Tests for DL-17 Datasets and DataLoader.

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
import torch


class TestDataLoading(unittest.TestCase):
    def test_dataset_items(self):
        ds = S.ArrayDataset(np.arange(6).reshape(3, 2), [0, 1, 0])
        self.assertEqual(len(ds), 3)
        x, y = ds[1]
        self.assertEqual((x.dtype, y.dtype), (torch.float32, torch.long))
        self.assertEqual((x.tolist(), y.item()), ([2.0, 3.0], 1))

    def test_batch_sizes(self):
        loader = S.make_loader(np.zeros((10, 3)), np.zeros(10), batch_size=4, shuffle=False)
        self.assertEqual([len(yb) for _, yb in loader], [4, 4, 2])

    def test_unshuffled_order(self):
        X = np.arange(10).reshape(5, 2); y = np.arange(5)
        first_x, first_y = next(iter(S.make_loader(X, y, batch_size=2, shuffle=False)))
        self.assertEqual(first_y.tolist(), [0, 1])
        self.assertEqual(first_x.tolist(), [[0.0, 1.0], [2.0, 3.0]])

    def test_shuffle_covers_everything_once(self):
        y = np.arange(23)
        seen = [v for _, yb in S.make_loader(np.zeros((23, 1)), y, batch_size=5, seed=1) for v in yb.tolist()]
        self.assertEqual(sorted(seen), list(range(23)))
        self.assertNotEqual(seen, list(range(23)))

    def test_seeded_shuffle_reproducible(self):
        y = np.arange(20)
        a = [yb.tolist() for _, yb in S.make_loader(np.zeros((20, 1)), y, batch_size=5, seed=3)]
        b = [yb.tolist() for _, yb in S.make_loader(np.zeros((20, 1)), y, batch_size=5, seed=3)]
        c = [yb.tolist() for _, yb in S.make_loader(np.zeros((20, 1)), y, batch_size=5, seed=4)]
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.ArrayDataset(np.zeros((3, 2)), [0, 1])


if __name__ == "__main__":
    unittest.main()
