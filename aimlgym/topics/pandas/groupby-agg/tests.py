"""Tests for PD-08 Group-by Aggregation.

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
import pandas as pd

DF = pd.DataFrame({"category": ["a", "b", "a", "b", "a"], "value": [1, 2, 3, np.nan, 5]})

class TestGroupby(unittest.TestCase):
    def test_columns(self):
        self.assertEqual(list(S.category_summary(DF).columns), ["category", "n", "n_valid", "total", "mean"])

    def test_values(self):
        exp = pd.DataFrame({"category": ["a", "b"], "n": [3, 2], "n_valid": [3, 1],
                            "total": [9.0, 2.0], "mean": [3.0, 2.0]})
        pd.testing.assert_frame_equal(S.category_summary(DF), exp, check_dtype=False)

    def test_sorted(self):
        d = pd.DataFrame({"category": ["z", "m", "a"], "value": [1.0, 2.0, 3.0]})
        self.assertEqual(S.category_summary(d)["category"].tolist(), ["a", "m", "z"])

    def test_all_nan_group(self):
        d = pd.DataFrame({"category": ["x", "x"], "value": [np.nan, np.nan]})
        out = S.category_summary(d)
        self.assertEqual(out["n"].iloc[0], 2)
        self.assertEqual(out["n_valid"].iloc[0], 0)
        self.assertTrue(np.isnan(out["mean"].iloc[0]))

    def test_index(self):
        self.assertEqual(list(S.category_summary(DF).index), [0, 1])

    def test_single_group(self):
        out = S.category_summary(pd.DataFrame({"category": ["q"] * 4, "value": [1.0, 2, 3, 4]}))
        self.assertAlmostEqual(out["mean"].iloc[0], 2.5)


import math

import numpy as np
import pandas as pd


class TestAgainstPlainPython(unittest.TestCase):
    def test_library_matches_dict_version(self):
        rows = [("b", 4.0), ("a", 1.0), ("b", None), ("a", 3.0), ("c", 10.0), ("b", 2.0)]
        df = pd.DataFrame(rows, columns=["category", "value"])
        groups = {}
        for cat, val in rows:
            groups.setdefault(cat, []).append(val)
        out = S.category_summary(df)
        for _, r in out.iterrows():
            vals = groups[r["category"]]
            valid = [v for v in vals if v is not None]
            self.assertEqual(r["n"], len(vals))
            self.assertEqual(r["n_valid"], len(valid))
            self.assertAlmostEqual(r["total"], sum(valid))
            self.assertAlmostEqual(r["mean"], sum(valid) / len(valid))
        self.assertEqual(out["category"].tolist(), sorted(groups))


if __name__ == "__main__":
    unittest.main()
