"""Tests for PY-19 Validated Factorial.

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


class TestFactorial(unittest.TestCase):
    def test_five(self):
        self.assertEqual(S.factorial(5), 120)

    def test_zero_and_one(self):
        self.assertEqual(S.factorial(0), 1)
        self.assertEqual(S.factorial(1), 1)

    def test_large_exact(self):
        self.assertEqual(S.factorial(25), 15511210043330985984000000)

    def test_negative(self):
        with self.assertRaises(ValueError):
            S.factorial(-2)

    def test_float(self):
        with self.assertRaises(TypeError):
            S.factorial(3.0)

    def test_string(self):
        with self.assertRaises(TypeError):
            S.factorial("4")

    def test_bool(self):
        with self.assertRaises(TypeError):
            S.factorial(True)


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_math_factorial(self):
        for n in (0, 1, 5, 20, 100):
            self.assertEqual(S.factorial(n), math.factorial(n))


if __name__ == "__main__":
    unittest.main()
