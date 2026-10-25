"""Tests for NL-16 Evaluating Text Classifiers.

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


from sklearn.metrics import f1_score, precision_score, recall_score


TEXTS = ["love it", "fine I guess", "awful", "it is ok", "great value", "not great"]
TRUE = ["pos", "neu", "neg", "neu", "pos", "neg"]
PRED = ["pos", "neg", "neg", "neu", "pos", "pos"]
LABELS = ["neg", "neu", "pos"]


class TestErrorReport(unittest.TestCase):
    def test_worked_example(self):
        r = S.error_report(["a", "b", "c", "d"], ["pos", "pos", "neg", "neu"], ["pos", "neg", "neg", "neg"], LABELS)
        self.assertEqual(r["confusion"], [[1, 0, 0], [1, 0, 0], [1, 0, 1]])
        self.assertEqual(r["per_class"]["neu"]["recall"], 0.0)
        self.assertEqual([e[0] for e in r["errors"]], ["b", "d"])

    def test_per_class_matches_metrics(self):
        r = S.error_report(TEXTS, TRUE, PRED, LABELS)
        p = precision_score(TRUE, PRED, labels=LABELS, average=None, zero_division=0)
        rc = recall_score(TRUE, PRED, labels=LABELS, average=None, zero_division=0)
        for i, label in enumerate(LABELS):
            self.assertAlmostEqual(r["per_class"][label]["precision"], p[i])
            self.assertAlmostEqual(r["per_class"][label]["recall"], rc[i])
            self.assertEqual(r["per_class"][label]["support"], TRUE.count(label))

    def test_macro_f1(self):
        r = S.error_report(TEXTS, TRUE, PRED, LABELS)
        self.assertAlmostEqual(r["macro_f1"], f1_score(TRUE, PRED, labels=LABELS, average="macro"))

    def test_errors_in_order(self):
        r = S.error_report(TEXTS, TRUE, PRED, LABELS)
        self.assertEqual(r["errors"], [("fine I guess", "neu", "neg"), ("not great", "neg", "pos")])

    def test_label_order_controls_matrix(self):
        r = S.error_report(TEXTS, TRUE, PRED, ["pos", "neu", "neg"])
        self.assertEqual(r["confusion"][0], [2, 0, 0])
        self.assertTrue(all(type(v) is int for row in r["confusion"] for v in row))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.error_report(["a"], ["pos", "neg"], ["pos", "neg"], LABELS)


if __name__ == "__main__":
    unittest.main()
