"""Tests for PY-07 Conditionals: Letter Grades.

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


def grade(score):
    out, _ = run_program(f"{score}\n")
    return out.splitlines()


class TestGrades(unittest.TestCase):
    def test_a_band(self):
        self.assertEqual(grade(95), ["A", "Pass"])

    def test_boundaries_top(self):
        self.assertEqual(grade(100), ["A", "Pass"])
        self.assertEqual(grade(90), ["A", "Pass"])
        self.assertEqual(grade(89), ["B", "Pass"])

    def test_middle_bands(self):
        self.assertEqual(grade(80)[0], "B")
        self.assertEqual(grade(79)[0], "C")
        self.assertEqual(grade(70)[0], "C")
        self.assertEqual(grade(69)[0], "D")

    def test_pass_boundary(self):
        self.assertEqual(grade(60), ["D", "Pass"])
        self.assertEqual(grade(59), ["F", "Fail"])

    def test_zero(self):
        self.assertEqual(grade(0), ["F", "Fail"])

    def test_invalid_low(self):
        self.assertEqual(grade(-1), ["Invalid score", "Check the input"])

    def test_invalid_high(self):
        self.assertEqual(grade(101), ["Invalid score", "Check the input"])


if __name__ == "__main__":
    unittest.main()
