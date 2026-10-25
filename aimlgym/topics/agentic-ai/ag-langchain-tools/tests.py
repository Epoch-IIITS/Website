"""Tests for AG-03 Tools and Tool Calling with LangChain.

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


from langchain_core.messages import AIMessage, ToolMessage


def calls(*items):
    return AIMessage(content="", tool_calls=[{"name": n, "args": a, "id": f"call_{i}"} for i, (n, a) in enumerate(items)])


class TestTools(unittest.TestCase):
    def test_tool_metadata(self):
        self.assertEqual(S.word_count.name, "word_count")
        self.assertEqual(S.word_count.description, "Count the words in a text.")
        self.assertEqual(set(S.to_fahrenheit.args), {"celsius"})

    def test_tools_compute(self):
        self.assertEqual(S.word_count.invoke({"text": "to be or not"}), 4)
        self.assertEqual(S.to_fahrenheit.invoke({"celsius": 100}), 212.0)

    def test_run_two_calls(self):
        out = S.run_tool_calls(calls(("word_count", {"text": "to be or not"}), ("to_fahrenheit", {"celsius": 100})),
                               [S.word_count, S.to_fahrenheit])
        self.assertEqual([(m.content, m.tool_call_id) for m in out], [("4", "call_0"), ("212.0", "call_1")])
        self.assertTrue(all(isinstance(m, ToolMessage) for m in out))

    def test_unknown_tool(self):
        [msg] = S.run_tool_calls(calls(("delete_files", {})), [S.word_count])
        self.assertEqual((msg.content, msg.status, msg.tool_call_id), ("Error: unknown tool delete_files", "error", "call_0"))

    def test_bad_arguments(self):
        [msg] = S.run_tool_calls(calls(("to_fahrenheit", {"celsius": "hot"})), [S.to_fahrenheit])
        self.assertEqual(msg.status, "error")
        self.assertTrue(msg.content.startswith("Error: "))

    def test_no_calls(self):
        self.assertEqual(S.run_tool_calls(AIMessage(content="done"), [S.word_count]), [])


if __name__ == "__main__":
    unittest.main()
