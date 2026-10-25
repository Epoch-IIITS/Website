"""Tests for ML-18 Pipelines and ColumnTransformer.

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


def homes():
    return pd.DataFrame({
        "area": [50.0, 80.0, np.nan, 120.0, 65.0, 90.0],
        "age": [10.0, 5.0, 20.0, 2.0, np.nan, 8.0],
        "city": ["Pune", "Delhi", "Pune", "Delhi", np.nan, "Pune"],
        "price": [40.0, 75.0, 38.0, 120.0, 50.0, 80.0],
    })


class TestBuildModel(unittest.TestCase):
    def test_feature_names(self):
        df = homes()
        model = S.build_model(["area", "age"], ["city"]).fit(df, df["price"])
        self.assertEqual(list(model.named_steps["prep"].get_feature_names_out()),
                         ["num__area", "num__age", "cat__city_Delhi", "cat__city_Pune"])

    def test_unfitted_and_structure(self):
        model = S.build_model(["area"], ["city"])
        self.assertEqual(list(model.named_steps), ["prep", "model"])
        self.assertFalse(hasattr(model.named_steps["model"], "coef_"))

    def test_median_imputation_from_training(self):
        df = homes()
        model = S.build_model(["area"], []).fit(df, df["price"])
        imputer = model.named_steps["prep"].named_transformers_["num"][0]
        self.assertEqual(imputer.statistics_.tolist(), [80.0])

    def test_unknown_category_is_zeros(self):
        df = homes()
        model = S.build_model(["area"], ["city"]).fit(df, df["price"])
        new = pd.DataFrame({"area": [70.0], "age": [3.0], "city": ["Chennai"]})
        encoded = model.named_steps["prep"].transform(new)
        self.assertEqual(encoded[0, 1:].tolist(), [0.0, 0.0])
        self.assertEqual(model.predict(new).shape, (1,))

    def test_no_missing_after_transform(self):
        df = homes()
        model = S.build_model(["area", "age"], ["city"]).fit(df, df["price"])
        self.assertFalse(np.isnan(model.named_steps["prep"].transform(df)).any())

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.build_model([], [])
        with self.assertRaises(ValueError):
            S.build_model(["city"], ["city"])


if __name__ == "__main__":
    unittest.main()
