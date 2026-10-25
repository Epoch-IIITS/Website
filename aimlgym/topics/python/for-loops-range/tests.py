"""Tests for PY-09 For Loops and range: FizzBuzz.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import contextlib
import importlib
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
TARGET = os.environ.get("AIMLGYM_TARGET", "solution")


def run_program(stdin_text=""):
    """Run the program from the top with stdin_text as its input; return (output, module)."""
    sys.modules.pop(TARGET, None)
    saved_stdin = sys.stdin
    sys.stdin = io.StringIO(stdin_text)
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            module = importlib.import_module(TARGET)
    finally:
        sys.stdin = saved_stdin
    return buffer.getvalue(), module


class TestFizzBuzz(unittest.TestCase):
    def test_five(self):
        out, _ = run_program("5\n")
        self.assertEqual(out, "1\n2\nFizz\n4\nBuzz\nsum=8\n")

    def test_fifteen_line(self):
        out, _ = run_program("15\n")
        self.assertEqual(out.splitlines()[14], "FizzBuzz")

    def test_fifteen_sum(self):
        out, _ = run_program("15\n")
        self.assertEqual(out.splitlines()[-1], "sum=60")

    def test_zero(self):
        out, _ = run_program("0\n")
        self.assertEqual(out, "sum=0\n")

    def test_one(self):
        out, _ = run_program("1\n")
        self.assertEqual(out, "1\nsum=0\n")

    def test_line_count(self):
        out, _ = run_program("100\n")
        lines = out.splitlines()
        self.assertEqual(len(lines), 101)
        self.assertEqual(lines[-1], "sum=2418")


if __name__ == "__main__":
    unittest.main()
