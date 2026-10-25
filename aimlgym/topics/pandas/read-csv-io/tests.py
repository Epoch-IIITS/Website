"""Tests for PD-03 Reading and Writing CSV.

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


import io

import pandas as pd

TEXT = "name,score,height,passed\nada,91,1.68,True\nbob,78,1.80,False\n\"lee, jo\",85,1.75,True\n"


class TestReadCsv(unittest.TestCase):
    def test_manual(self):
        rows = S.parse_manual(TEXT)
        self.assertEqual(rows[0], {"name": "ada", "score": 91, "height": 1.68, "passed": "True"})
        self.assertEqual(rows[2]["name"], "lee, jo")
        self.assertIs(type(rows[1]["score"]), int)

    def test_pandas_dtypes(self):
        df = S.parse_pandas(TEXT)
        self.assertEqual(df.shape, (3, 4))
        self.assertTrue(pd.api.types.is_integer_dtype(df["score"]))
        self.assertTrue(pd.api.types.is_float_dtype(df["height"]))
        self.assertTrue(pd.api.types.is_bool_dtype(df["passed"]))
        self.assertTrue(pd.api.types.is_string_dtype(df["name"]))

    def test_manual_matches_pandas(self):
        df = S.parse_pandas(TEXT)
        manual = S.parse_manual(TEXT)
        self.assertEqual([r["score"] for r in manual], df["score"].tolist())
        self.assertEqual([r["name"] for r in manual], df["name"].tolist())

    def test_missing_becomes_float(self):
        df = S.parse_pandas("a,b\n1,2.5\n3,\n")
        self.assertTrue(pd.api.types.is_integer_dtype(df["a"]))
        self.assertTrue(df["b"].isna().iloc[1])

    def test_numeric_means(self):
        means = S.numeric_means(S.parse_pandas(TEXT))
        self.assertEqual(sorted(means), ["height", "score"])
        self.assertAlmostEqual(means["score"], 254 / 3)
        self.assertAlmostEqual(means["height"], (1.68 + 1.80 + 1.75) / 3)

    def test_round_trip(self):
        df = S.parse_pandas(TEXT)
        text = S.to_csv_text(df)
        self.assertTrue(text.startswith("name,score,height,passed\n"))
        pd.testing.assert_frame_equal(pd.read_csv(io.StringIO(text)), df)


if __name__ == "__main__":
    unittest.main()
