"""Tests for PY-06 Strings: Indexing, Slicing and Methods.

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


def lines_for(word):
    out, _ = run_program(word + "\n")
    return out.splitlines()


class TestStrings(unittest.TestCase):
    def test_python(self):
        self.assertEqual(lines_for("Python"), [
            "Length: 6", "First: P", "Last: n", "First three: Pyt",
            "Reversed: nohtyP", "Upper: PYTHON", "Contains 'th': True"])

    def test_short_word(self):
        self.assertEqual(lines_for("ab")[3], "First three: ab")

    def test_single_character(self):
        lines = lines_for("x")
        self.assertEqual(lines[1:5], ["First: x", "Last: x", "First three: x", "Reversed: x"])

    def test_strip(self):
        self.assertEqual(lines_for("   data  ")[0], "Length: 4")

    def test_contains_false(self):
        self.assertEqual(lines_for("THEN")[6], "Contains 'th': False")

    def test_reverse_palindrome(self):
        self.assertEqual(lines_for("level")[4], "Reversed: level")

    def test_upper(self):
        self.assertEqual(lines_for("mathematics")[5], "Upper: MATHEMATICS")


if __name__ == "__main__":
    unittest.main()
