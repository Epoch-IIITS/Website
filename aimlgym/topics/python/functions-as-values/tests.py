"""Tests for PY-17 Functions as Values.

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


class TestFunctionsAsValues(unittest.TestCase):
    def test_pipeline_order(self):
        self.assertEqual(S.pipeline(str.strip, str.upper)("  hi "), "HI")
        self.assertEqual(S.pipeline(lambda x: x + 1, lambda x: x * 10)(2), 30)

    def test_pipeline_empty(self):
        self.assertEqual(S.pipeline()(5), 5)

    def test_sort_words(self):
        self.assertEqual(S.sort_words(["pear", "fig", "apple", "kiwi"]), ["fig", "kiwi", "pear", "apple"])
        data = ["b", "a"]
        S.sort_words(data)
        self.assertEqual(data, ["b", "a"])

    def test_format_scores(self):
        self.assertEqual(S.format_record("ada", 90, 85), "ada: 90, 85")
        self.assertEqual(S.format_record("ada"), "ada: ")

    def test_format_extra_sorted(self):
        self.assertEqual(S.format_record("bob", 70, sep="/", year=2, club="ai"), "bob: 70 | club=ai, year=2")
        self.assertEqual(S.format_record("cy", 1, 2, sep="-"), "cy: 1-2")

    def test_count_calls(self):
        @S.count_calls
        def add(a, b=0):
            return a + b
        self.assertEqual(add.calls, 0)
        self.assertEqual(add(2, b=3), 5)
        add(1)
        self.assertEqual(add.calls, 2)

    def test_wraps_keeps_name(self):
        @S.count_calls
        def greet():
            """Say hi."""
            return "hi"
        self.assertEqual(greet.__name__, "greet")
        self.assertEqual(greet.__doc__, "Say hi.")


if __name__ == "__main__":
    unittest.main()
