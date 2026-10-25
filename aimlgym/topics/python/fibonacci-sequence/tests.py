"""Tests for PY-14 Fibonacci Sequence.

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


class TestFibonacci(unittest.TestCase):
    def test_six(self):
        self.assertEqual(S.fibonacci(6), [0, 1, 1, 2, 3, 5])

    def test_zero(self):
        self.assertEqual(S.fibonacci(0), [])

    def test_one(self):
        self.assertEqual(S.fibonacci(1), [0])

    def test_two(self):
        self.assertEqual(S.fibonacci(2), [0, 1])

    def test_negative(self):
        self.assertEqual(S.fibonacci(-1), [])

    def test_recurrence_holds(self):
        f = S.fibonacci(50)
        self.assertEqual(len(f), 50)
        for k in range(2, 50):
            self.assertEqual(f[k], f[k - 1] + f[k - 2])

    def test_fast_large(self):
        f = S.fibonacci(5000)
        self.assertEqual(len(f), 5000)


if __name__ == "__main__":
    unittest.main()
