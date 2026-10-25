"""Tests for PY-04 Reading Input.

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


class TestInputOutput(unittest.TestCase):
    def test_example(self):
        out, _ = run_program("Ada\n2006\n")
        self.assertEqual(out, "Hello, Ada!\nIn 2030 you will turn 24.\n")

    def test_strips_name(self):
        out, _ = run_program("   Grace  \n1990\n")
        self.assertEqual(out.splitlines()[0], "Hello, Grace!")

    def test_year_with_spaces(self):
        out, _ = run_program("Linus\n  1969 \n")
        self.assertEqual(out.splitlines()[1:], ["In 2030 you will turn 61."])

    def test_two_word_name(self):
        out, _ = run_program("Alan Turing\n1912\n")
        self.assertEqual(out, "Hello, Alan Turing!\nIn 2030 you will turn 118.\n")

    def test_future_year(self):
        out, _ = run_program("Kid\n2030\n")
        self.assertEqual(out.splitlines()[1], "In 2030 you will turn 0.")

    def test_no_prompt_text(self):
        out, _ = run_program("Ada\n2006\n")
        self.assertTrue(out.startswith("Hello, "))


if __name__ == "__main__":
    unittest.main()
