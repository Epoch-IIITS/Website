"""Tests for PY-05 Arithmetic Operators.

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


class TestDuration(unittest.TestCase):
    def test_example(self):
        out, _ = run_program("3725\n")
        self.assertEqual(out, "1:02:05\n62.08 minutes\n")

    def test_zero(self):
        out, _ = run_program("0\n")
        self.assertEqual(out, "0:00:00\n0.00 minutes\n")

    def test_padding(self):
        out, _ = run_program("59\n")
        self.assertEqual(out.splitlines()[0], "0:00:59")

    def test_exact_hour(self):
        out, _ = run_program("3600\n")
        self.assertEqual(out, "1:00:00\n60.00 minutes\n")

    def test_end_of_day(self):
        out, _ = run_program("86399\n")
        self.assertEqual(out, "23:59:59\n1439.98 minutes\n")

    def test_more_than_a_day(self):
        out, _ = run_program("90000\n")
        self.assertEqual(out.splitlines()[0], "25:00:00")

    def test_minutes_two_decimals(self):
        out, _ = run_program("61\n")
        self.assertEqual(out.splitlines()[1], "1.02 minutes")


if __name__ == "__main__":
    unittest.main()
