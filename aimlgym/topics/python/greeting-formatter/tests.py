"""Tests for PY-10 Greeting Formatter.

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


class TestGreet(unittest.TestCase):
    def test_default(self):
        self.assertEqual(S.greet(), "Hello, World!")

    def test_simple_name(self):
        self.assertEqual(S.greet("alice"), "Hello, Alice!")

    def test_strip_and_title(self):
        self.assertEqual(S.greet("  ada lovelace "), "Hello, Ada Lovelace!")

    def test_only_spaces(self):
        self.assertEqual(S.greet("   "), "Hello, World!")

    def test_empty_string(self):
        self.assertEqual(S.greet(""), "Hello, World!")

    def test_returns_str_not_none(self):
        self.assertIsInstance(S.greet("bob"), str)

    def test_already_capitalised(self):
        self.assertEqual(S.greet("GRACE HOPPER"), "Hello, Grace Hopper!")


if __name__ == "__main__":
    unittest.main()
