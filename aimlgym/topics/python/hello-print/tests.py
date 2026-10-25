"""Tests for PY-01 Hello, print().

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


EXPECTED = 'Hello, world!\nPython is fun\n2026-10-24\n\nLoading...done\nShe said "hi"\n'


class TestHelloPrint(unittest.TestCase):
    def test_exact_output(self):
        out, _ = run_program()
        self.assertEqual(out, EXPECTED)

    def test_first_line(self):
        out, _ = run_program()
        self.assertEqual(out.splitlines()[0], "Hello, world!")

    def test_words_line(self):
        out, _ = run_program()
        self.assertEqual(out.splitlines()[1:2], ["Python is fun"])

    def test_date_with_sep(self):
        out, _ = run_program()
        self.assertEqual(out.splitlines()[2:3], ["2026-10-24"])

    def test_blank_line(self):
        out, _ = run_program()
        self.assertEqual(out.splitlines()[3:4], [""])

    def test_end_joins_lines(self):
        out, _ = run_program()
        self.assertIn("Loading...done\n", out)

    def test_quotes(self):
        out, _ = run_program()
        self.assertTrue(out.endswith('She said "hi"\n'))

    def test_line_count(self):
        out, _ = run_program()
        self.assertEqual(len(out.splitlines()), 6)


if __name__ == "__main__":
    unittest.main()
