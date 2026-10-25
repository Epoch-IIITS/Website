"""Tests for ML-27 Capstone: an End-to-End Tabular Model.

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
from sklearn.model_selection import train_test_split


def churn(seed=0, n=400):
    rng = np.random.default_rng(seed)
    tenure = rng.integers(1, 60, n).astype(float)
    charges = rng.normal(70, 20, n)
    plan = rng.choice(["basic", "plus", "pro"], n)
    logit = 2.0 - 0.1 * tenure + 0.05 * (charges - 70) + np.where(plan == "basic", 1.5, 0.0)
    churned = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    tenure[rng.random(n) < 0.05] = np.nan
    return pd.DataFrame({"tenure": tenure, "charges": charges, "plan": plan, "churned": churned})


class TestEndToEnd(unittest.TestCase):
    def test_beats_baseline(self):
        r = S.end_to_end(churn(), "churned", ["tenure", "charges"], ["plan"])
        self.assertGreater(r["test_auc"], 0.75)
        self.assertGreater(r["test_accuracy"], r["baseline_accuracy"])

    def test_baseline_is_majority_share(self):
        df = churn(1)
        r = S.end_to_end(df, "churned", ["tenure", "charges"], ["plan"], seed=3)
        _, _, y_train, y_test = train_test_split(df.drop(columns=["churned"]), df["churned"],
                                                 test_size=0.25, stratify=df["churned"], random_state=3)
        majority = int(y_train.mean() >= 0.5)
        self.assertAlmostEqual(r["baseline_accuracy"], float((y_test == majority).mean()))

    def test_grid_choice(self):
        r = S.end_to_end(churn(2), "churned", ["tenure", "charges"], ["plan"])
        self.assertIn(r["best_C"], [0.01, 0.1, 1.0, 10.0])
        self.assertGreater(r["cv_auc"], 0.7)

    def test_model_handles_new_rows(self):
        r = S.end_to_end(churn(3), "churned", ["tenure", "charges"], ["plan"])
        new = pd.DataFrame({"tenure": [np.nan, 50.0], "charges": [95.0, 40.0], "plan": ["enterprise", "pro"]})
        proba = r["model"].predict_proba(new)[:, 1]
        self.assertEqual(proba.shape, (2,))
        self.assertGreater(proba[0], proba[1])

    def test_reproducible(self):
        a = S.end_to_end(churn(4), "churned", ["tenure", "charges"], ["plan"], seed=1)
        b = S.end_to_end(churn(4), "churned", ["tenure", "charges"], ["plan"], seed=1)
        self.assertEqual({k: v for k, v in a.items() if k != "model"}, {k: v for k, v in b.items() if k != "model"})

    def test_invalid_target(self):
        df = churn(5)
        with self.assertRaises(ValueError):
            S.end_to_end(df, "missing", ["tenure"], ["plan"])
        with self.assertRaises(ValueError):
            S.end_to_end(df.assign(churned=df["charges"]), "churned", ["tenure"], ["plan"])


if __name__ == "__main__":
    unittest.main()
