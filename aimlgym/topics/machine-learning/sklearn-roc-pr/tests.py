"""Tests for ML-24 Thresholds, ROC and Precision–Recall Curves.

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


import itertools
import numpy as np


def pairwise_auc(y, s):
    pos = [v for v, t in zip(s, y) if t == 1]
    neg = [v for v, t in zip(s, y) if t == 0]
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p, n in itertools.product(pos, neg))
    return wins / (len(pos) * len(neg))


class TestThresholdReport(unittest.TestCase):
    def test_example(self):
        r = S.threshold_report([1, 1, 0, 1, 0, 0], [0.9, 0.8, 0.7, 0.6, 0.4, 0.2], 0.9)
        self.assertAlmostEqual(r["roc_auc"], 8 / 9)
        self.assertEqual(r["threshold"], 0.6)
        self.assertAlmostEqual(r["precision"], 0.75)
        self.assertEqual(r["recall"], 1.0)

    def test_lower_target_allows_higher_threshold(self):
        r = S.threshold_report([1, 1, 0, 1, 0, 0], [0.9, 0.8, 0.7, 0.6, 0.4, 0.2], 0.6)
        self.assertEqual(r["threshold"], 0.8)
        self.assertEqual(r["precision"], 1.0)

    def test_auc_is_pairwise_ranking(self):
        rng = np.random.default_rng(0)
        y = rng.integers(0, 2, 60); s = np.round(rng.random(60) + 0.3 * y, 2)
        r = S.threshold_report(y.tolist(), s.tolist(), 0.5)
        self.assertAlmostEqual(r["roc_auc"], pairwise_auc(y.tolist(), s.tolist()), places=10)

    def test_perfect_ranking(self):
        r = S.threshold_report([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9], 1.0)
        self.assertEqual((r["roc_auc"], r["average_precision"]), (1.0, 1.0))
        self.assertEqual((r["threshold"], r["precision"]), (0.8, 1.0))

    def test_recall_target_met(self):
        rng = np.random.default_rng(1)
        y = rng.integers(0, 2, 80); s = rng.random(80) + 0.5 * y
        for target in (0.5, 0.8, 0.95):
            r = S.threshold_report(y.tolist(), s.tolist(), target)
            predicted = s >= r["threshold"]
            self.assertGreaterEqual(predicted[y == 1].mean(), target)
            self.assertAlmostEqual(r["precision"], y[predicted].mean())

    def test_invalid(self):
        for args in [([1, 1], [0.2, 0.3], 0.5), ([0, 1], [0.1], 0.5), ([0, 1], [0.1, 0.9], 0)]:
            with self.assertRaises(ValueError):
                S.threshold_report(*args)


if __name__ == "__main__":
    unittest.main()
