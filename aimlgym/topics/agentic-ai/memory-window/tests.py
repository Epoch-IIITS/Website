"""Tests for AG-10 Conversation Memory Window by Hand.

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


MSGS = [{"role": "system", "content": "be helpful"},
        {"role": "user", "content": "one two three four five six"},
        {"role": "assistant", "content": "a b c"},
        {"role": "user", "content": "ok"}]

class TestMemory(unittest.TestCase):
    def test_tokens(self):
        self.assertEqual(S.count_tokens("a  b\nc"), 3)

    def test_example(self):
        self.assertEqual([m["content"] for m in S.fit_context(MSGS, 20)],
                         ["be helpful", "[2 earlier messages omitted]", "ok"])

    def test_everything_fits(self):
        self.assertEqual(S.fit_context(MSGS, 100), MSGS)

    def test_marker_fits(self):
        out = S.fit_context(MSGS, 26)
        self.assertEqual([m["content"] for m in out], ["be helpful", "[1 earlier messages omitted]", "a b c", "ok"])

    def test_budget_respected(self):
        for b in range(6, 40):
            out = S.fit_context(MSGS, b)
            self.assertLessEqual(sum(len(m["content"].split()) + 4 for m in out), b)
            self.assertEqual(out[0]["content"], "be helpful")

    def test_no_system(self):
        out = S.fit_context(MSGS[1:], 9)
        self.assertEqual([m["content"] for m in out], ["ok"])

    def test_system_too_big(self):
        with self.assertRaises(ValueError):
            S.fit_context(MSGS, 3)

    def test_input_unchanged(self):
        before = [dict(m) for m in MSGS]
        S.fit_context(MSGS, 20)
        self.assertEqual(MSGS, before)


if __name__ == "__main__":
    unittest.main()
