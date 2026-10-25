"""Tests for PY-08 While Loops: Read Until Done.

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


class TestReadUntilDone(unittest.TestCase):
    def test_example(self):
        out, _ = run_program("4\n9\n2\ndone\n")
        self.assertEqual(out, "count=3 total=15 max=9\n")

    def test_empty(self):
        out, _ = run_program("done\n")
        self.assertEqual(out, "count=0 total=0 max=None\n")

    def test_negatives(self):
        out, _ = run_program("-5\n-2\n-9\ndone\n")
        self.assertEqual(out, "count=3 total=-16 max=-2\n")

    def test_single(self):
        out, _ = run_program("7\ndone\n")
        self.assertEqual(out, "count=1 total=7 max=7\n")

    def test_spaces_around_done(self):
        out, _ = run_program("1\n2\n  done  \n")
        self.assertEqual(out, "count=2 total=3 max=2\n")

    def test_stops_at_done(self):
        out, _ = run_program("1\ndone\n100\n")
        self.assertEqual(out, "count=1 total=1 max=1\n")


if __name__ == "__main__":
    unittest.main()
