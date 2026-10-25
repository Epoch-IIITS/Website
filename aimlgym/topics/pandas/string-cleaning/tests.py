"""Tests for PD-11 Cleaning Text Columns.

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

DF = pd.DataFrame({"name": ["  ann   LEE ", "BOB", None],
                   "phone": ["+91 98-765 43210", "(044) 1234", None],
                   "email": [" Ann.Lee@Example.COM ", "bob-at-mail", None]})

class TestClean(unittest.TestCase):
    def test_row0(self):
        self.assertEqual(S.clean_contacts(DF).iloc[0][["name", "phone", "email", "domain"]].tolist(),
                         ["Ann Lee", "919876543210", "ann.lee@example.com", "example.com"])

    def test_title(self):
        self.assertEqual(S.clean_contacts(DF)["name"].iloc[1], "Bob")

    def test_phone_digits(self):
        self.assertEqual(S.clean_contacts(DF)["phone"].iloc[1], "0441234")

    def test_no_at_domain_missing(self):
        self.assertTrue(pd.isna(S.clean_contacts(DF)["domain"].iloc[1]))

    def test_missing_stays_missing(self):
        row = S.clean_contacts(DF).iloc[2]
        self.assertTrue(all(pd.isna(row[c]) for c in ["name", "phone", "email", "domain"]))

    def test_not_string_nan(self):
        self.assertNotIn("nan", S.clean_contacts(DF)["name"].dropna().str.lower().tolist())

    def test_input_unchanged(self):
        d = DF.copy()
        S.clean_contacts(d)
        self.assertEqual(d["name"].iloc[0], "  ann   LEE ")


if __name__ == "__main__":
    unittest.main()
