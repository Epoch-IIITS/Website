"""Tests for PY-02 Variables and f-strings.

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


class TestVariables(unittest.TestCase):
    def test_name(self):
        _, m = run_program()
        self.assertEqual(m.name, "Ada")

    def test_age_is_int(self):
        _, m = run_program()
        self.assertEqual(m.age, 19)
        self.assertIsInstance(m.age, int)

    def test_height_is_float(self):
        _, m = run_program()
        self.assertIsInstance(m.height_m, float)
        self.assertAlmostEqual(m.height_m, 1.68)

    def test_is_student_bool(self):
        _, m = run_program()
        self.assertIs(m.is_student, True)

    def test_next_age(self):
        _, m = run_program()
        self.assertEqual(m.next_age, 20)

    def test_output(self):
        out, _ = run_program()
        self.assertEqual(out, "Name: Ada\nAge next year: 20\nHeight: 1.68 m\nStudent: True\n")


if __name__ == "__main__":
    unittest.main()
