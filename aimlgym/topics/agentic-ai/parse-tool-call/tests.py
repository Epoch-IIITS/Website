"""Tests for AG-02 Parsing Model Tool Calls.

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


class TestParse(unittest.TestCase):
    def test_tool_call(self):
        self.assertEqual(S.parse_model_output('Thinking... <tool_call>{"tool": "add", "args": {"a": 1, "b": 2}}</tool_call>'),
                         {"type": "tool_call", "tool": "add", "args": {"a": 1, "b": 2}})

    def test_default_args(self):
        self.assertEqual(S.parse_model_output('<tool_call>{"tool": "time"}</tool_call>'),
                         {"type": "tool_call", "tool": "time", "args": {}})

    def test_multiline(self):
        r = S.parse_model_output('<tool_call>\n{"tool": "x",\n "args": {}}\n</tool_call>')
        self.assertEqual(r["type"], "tool_call")

    def test_final(self):
        self.assertEqual(S.parse_model_output("  FINAL: 42 "), {"type": "final", "content": "42"})

    def test_invalid_json(self):
        self.assertEqual(S.parse_model_output("<tool_call>{oops}</tool_call>"), {"type": "invalid", "error": "invalid JSON"})

    def test_multiple(self):
        t = '<tool_call>{"tool": "a"}</tool_call><tool_call>{"tool": "b"}</tool_call>'
        self.assertEqual(S.parse_model_output(t)["error"], "multiple tool calls")

    def test_bad_shape(self):
        self.assertEqual(S.parse_model_output('<tool_call>["add"]</tool_call>')["error"],
                         "tool call must be an object with 'tool' and 'args'")
        self.assertEqual(S.parse_model_output('<tool_call>{"tool": "a", "args": [1]}</tool_call>')["type"], "invalid")

    def test_plain_text(self):
        self.assertEqual(S.parse_model_output("The answer is 4."), {"type": "invalid", "error": "no tool call or final answer"})

    def test_no_eval(self):
        r = S.parse_model_output('<tool_call>__import__("os").system("echo hi")</tool_call>')
        self.assertEqual(r, {"type": "invalid", "error": "invalid JSON"})


if __name__ == "__main__":
    unittest.main()
