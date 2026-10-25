"""Tests for PY-03 Types and Conversion.

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


class TestTypes(unittest.TestCase):
    def test_price_float(self):
        _, m = run_program()
        self.assertIsInstance(m.price, float)
        self.assertAlmostEqual(m.price, 19.99)

    def test_quantity_int(self):
        _, m = run_program()
        self.assertIsInstance(m.quantity, int)
        self.assertEqual(m.quantity, 3)

    def test_discount_float(self):
        _, m = run_program()
        self.assertIsInstance(m.discount, float)
        self.assertAlmostEqual(m.discount, 0.1)

    def test_total(self):
        _, m = run_program()
        self.assertAlmostEqual(m.total, 19.99 * 3 * 0.9, places=9)
        self.assertEqual(m.total_rounded, 53.97)

    def test_label(self):
        _, m = run_program()
        self.assertEqual(m.label, "3 items")

    def test_output(self):
        out, _ = run_program()
        self.assertEqual(out, "Total: 53.97\nprice is float\nquantity is int\n3 items\n")


if __name__ == "__main__":
    unittest.main()
