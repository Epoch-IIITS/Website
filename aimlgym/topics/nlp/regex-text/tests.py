"""Tests for NL-01 Regular Expressions for Text.

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


import re


class TestRegex(unittest.TestCase):
    def test_collapse_manual_matches_regex(self):
        for text in ["a   b\t\nc", "  lead and trail  ", "", "one"]:
            self.assertEqual(S.collapse_spaces_manual(text), S.collapse_spaces(text))
        self.assertEqual(S.collapse_spaces("a   b\t\nc "), "a b c")

    def test_mask_digits(self):
        self.assertEqual(S.mask_digits("Call 555-0199 at 9am"), "Call ###-#### at #am")

    def test_find_numbers(self):
        self.assertEqual(S.find_numbers("x=-3.5, y=2, z=10.25 and 7."), [-3.5, 2.0, 10.25, 7.0])
        self.assertEqual(S.find_numbers("no numbers"), [])

    def test_hashtags(self):
        self.assertEqual(S.find_hashtags("#AI rocks #ml_2026! email#notatag (#NLP)"), ["ai", "ml_2026", "nlp"])

    def test_parse_log(self):
        self.assertEqual(S.parse_log("2026-10-24 12:00:01 ERROR Disk full"),
                         {"date": "2026-10-24", "time": "12:00:01", "level": "ERROR", "message": "Disk full"})

    def test_parse_log_rejects(self):
        self.assertIsNone(S.parse_log("2026-10-24 12:00:01 FATAL Disk full"))
        self.assertIsNone(S.parse_log("garbage 2026-10-24 12:00:01 INFO x"))
        self.assertIsNone(S.parse_log("2026-10-24 12:00 INFO short time"))

    def test_message_keeps_spaces(self):
        out = S.parse_log("2026-01-02 03:04:05 INFO user  ada   logged in")
        self.assertEqual(out["message"], "user  ada   logged in")


if __name__ == "__main__":
    unittest.main()
