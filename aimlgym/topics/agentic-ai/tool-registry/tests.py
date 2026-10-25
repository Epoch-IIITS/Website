"""Tests for AG-01 Tool Registry and Dispatch.

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


def make():
    reg = S.ToolRegistry()
    reg.register("add", lambda a, b: a + b, {"a": int, "b": int}, "Add two ints")
    reg.register("div", lambda x, y: x / y, {"x": float, "y": float}, "Divide")
    return reg

class TestRegistry(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(make().dispatch({"tool": "add", "args": {"a": 2, "b": 3}}), {"ok": True, "result": 5})

    def test_unknown(self):
        self.assertEqual(make().dispatch({"tool": "rm", "args": {}}), {"ok": False, "error": "unknown tool 'rm'"})

    def test_missing_and_unexpected(self):
        r = make()
        self.assertEqual(r.dispatch({"tool": "add", "args": {"a": 2}})["error"], "missing argument 'b'")
        self.assertEqual(r.dispatch({"tool": "add", "args": {"a": 1, "b": 2, "c": 3}})["error"], "unexpected argument 'c'")

    def test_types(self):
        r = make()
        self.assertEqual(r.dispatch({"tool": "add", "args": {"a": 2, "b": "3"}})["error"], "argument 'b' must be int")
        self.assertEqual(r.dispatch({"tool": "add", "args": {"a": True, "b": 1}})["error"], "argument 'a' must be int")
        self.assertTrue(r.dispatch({"tool": "div", "args": {"x": 1, "y": 2}})["ok"])

    def test_tool_exception(self):
        self.assertEqual(make().dispatch({"tool": "div", "args": {"x": 1.0, "y": 0.0}}),
                         {"ok": False, "error": "tool error: ZeroDivisionError: float division by zero"})

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            make().register("add", print, {})

    def test_describe(self):
        self.assertEqual(make().describe(), [
            {"name": "add", "description": "Add two ints", "args": {"a": "int", "b": "int"}},
            {"name": "div", "description": "Divide", "args": {"x": "float", "y": "float"}}])


if __name__ == "__main__":
    unittest.main()
