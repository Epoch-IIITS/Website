"""Tests for PD-10 Merging Tables.

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

O = pd.DataFrame({"order_id": [1, 2, 3, 4], "customer_id": [1, 2, 9, 1], "amount": [50, 20, 5, 10]})
C = pd.DataFrame({"customer_id": [1, 2], "name": ["Ann", "Bob"]})

class TestMerge(unittest.TestCase):
    def test_names(self):
        self.assertEqual(S.orders_with_customers(O, C)["name"].tolist(), ["Ann", "Bob", "unknown", "Ann"])

    def test_row_count_kept(self):
        self.assertEqual(len(S.orders_with_customers(O, C)), 4)

    def test_order_ids(self):
        self.assertEqual(S.orders_with_customers(O, C)["order_id"].tolist(), [1, 2, 3, 4])

    def test_duplicate_customer(self):
        bad = pd.DataFrame({"customer_id": [1, 1], "name": ["Ann", "Ann2"]})
        with self.assertRaises(pd.errors.MergeError):
            S.orders_with_customers(O, bad)

    def test_spend(self):
        out = S.spend_per_customer(O, C)
        self.assertEqual(out["name"].tolist(), ["Ann", "Bob", "unknown"])
        self.assertEqual(out["total"].tolist(), [60, 20, 5])

    def test_spend_tie(self):
        o = pd.DataFrame({"order_id": [1, 2], "customer_id": [2, 1], "amount": [7, 7]})
        self.assertEqual(S.spend_per_customer(o, C)["name"].tolist(), ["Ann", "Bob"])

    def test_columns(self):
        self.assertEqual(list(S.spend_per_customer(O, C).columns), ["name", "total"])


import pandas as pd


class TestAgainstPlainPython(unittest.TestCase):
    def test_library_left_join_matches_dict_lookup(self):
        orders = pd.DataFrame({"order_id": [1, 2, 3, 4], "customer_id": [10, 11, 10, 99], "amount": [5.0, 7.5, 2.5, 1.0]})
        customers = pd.DataFrame({"customer_id": [10, 11], "name": ["ada", "bob"]})
        lookup = dict(zip(customers["customer_id"], customers["name"]))
        expected = [lookup.get(c, "unknown") for c in orders["customer_id"]]
        self.assertEqual(S.orders_with_customers(orders, customers)["name"].tolist(), expected)


if __name__ == "__main__":
    unittest.main()
