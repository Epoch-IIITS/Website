"""Tests for PD-07 Sort and Rank.

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


import pandas as pd

DF = pd.DataFrame({"name": ["bob", "ann", "dee", "cy"], "score": [85, 90, 70, 90]})

class TestLeaderboard(unittest.TestCase):
    def test_order(self):
        self.assertEqual(S.leaderboard(DF)["name"].tolist(), ["ann", "cy", "bob", "dee"])

    def test_ranks(self):
        self.assertEqual(S.leaderboard(DF)["rank"].tolist(), [1, 1, 3, 4])

    def test_rank_int(self):
        self.assertTrue(pd.api.types.is_integer_dtype(S.leaderboard(DF)["rank"]))

    def test_top_n(self):
        out = S.leaderboard(DF, n=2)
        self.assertEqual(out["name"].tolist(), ["ann", "cy"])

    def test_index(self):
        self.assertEqual(list(S.leaderboard(DF).index), [0, 1, 2, 3])

    def test_all_tied(self):
        out = S.leaderboard(pd.DataFrame({"name": ["z", "y"], "score": [5, 5]}))
        self.assertEqual(out["name"].tolist(), ["y", "z"])
        self.assertEqual(out["rank"].tolist(), [1, 1])

    def test_input_unchanged(self):
        before = DF.copy()
        S.leaderboard(DF)
        pd.testing.assert_frame_equal(DF, before)


if __name__ == "__main__":
    unittest.main()
