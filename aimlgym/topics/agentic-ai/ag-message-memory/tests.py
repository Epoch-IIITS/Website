"""Tests for AG-09 Conversation Memory with trim_messages.

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


from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


def chat():
    return [SystemMessage("be brief"), HumanMessage("a"), AIMessage("b"), HumanMessage("c"), AIMessage("d")]


class TestTrimming(unittest.TestCase):
    def test_budget_three(self):
        self.assertEqual([m.content for m in S.trim_history(chat(), 3)], ["be brief", "c", "d"])

    def test_starts_on_human(self):
        kept = S.trim_history(chat(), 4)
        self.assertEqual([m.content for m in kept], ["be brief", "c", "d"])
        self.assertEqual(kept[1].type, "human")

    def test_everything_fits(self):
        self.assertEqual(len(S.trim_history(chat(), 10)), 5)

    def test_count_words(self):
        self.assertEqual(S.count_words([HumanMessage("one two"), AIMessage("three")]), 3)
        self.assertEqual(S.count_words([]), 0)

    def test_trim_by_words(self):
        msgs = [SystemMessage("rules here"), HumanMessage("first long question here"), AIMessage("long answer"),
                HumanMessage("short"), AIMessage("ok")]
        kept = S.trim_by_words(msgs, 4)
        self.assertEqual([m.content for m in kept], ["rules here", "short", "ok"])
        self.assertLessEqual(S.count_words(kept), 4)

    def test_original_unchanged_and_invalid(self):
        msgs = chat()
        S.trim_history(msgs, 2)
        self.assertEqual(len(msgs), 5)
        with self.assertRaises(ValueError):
            S.trim_history(msgs, 0)


if __name__ == "__main__":
    unittest.main()
