"""Tests for PY-24 Text Statistics from stdin.

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


import io
import subprocess
from contextlib import redirect_stdout
from unittest import mock


class TestTextStats(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.text_stats("to be\nor not\n"), (2, 4, 13))

    def test_empty(self):
        self.assertEqual(S.text_stats(""), (0, 0, 0))

    def test_no_trailing_newline(self):
        self.assertEqual(S.text_stats("one line no newline"), (1, 4, 19))

    def test_blank_lines(self):
        self.assertEqual(S.text_stats("a\n\n b \n"), (3, 2, 7))

    def test_main_output(self):
        buf = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO("to be\nor not\n")), redirect_stdout(buf):
            S.main()
        self.assertEqual(buf.getvalue(), "lines=2 words=4 chars=13\n")

    def test_main_empty(self):
        buf = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO("")), redirect_stdout(buf):
            S.main()
        self.assertEqual(buf.getvalue(), "lines=0 words=0 chars=0\n")

    def test_as_script(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), S.__name__ + ".py")
        r = subprocess.run([sys.executable, path], input="x y z\n", capture_output=True,
                           text=True, timeout=30)
        self.assertEqual(r.stdout, "lines=1 words=3 chars=6\n")


if __name__ == "__main__":
    unittest.main()
