"""Tests for AG-15 Validate-and-Retry Tool Calls.

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


SCHEMA = {"city": {"type": str}, "days": {"type": int, "min": 1, "max": 14},
          "mode": {"type": str, "enum": ["train", "bus"], "required": False}}

def scripted(replies):
    seen = []
    def model(msgs):
        seen.append(msgs); return replies[len(seen) - 1]
    model.seen = seen
    return model

class TestRetry(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(S.validate({"city": "Pune", "days": 3}, SCHEMA), [])

    def test_messages(self):
        self.assertEqual(S.validate({"city": "Pune", "days": "3"}, SCHEMA), ["days: expected int"])
        self.assertEqual(S.validate({"days": 30, "mode": "car", "x": 1}, SCHEMA),
                         ["city: missing", "days: must be <= 14", "mode: must be one of ['train', 'bus']", "x: unexpected field"])
        self.assertEqual(S.validate({"city": "A", "days": True}, SCHEMA), ["days: expected int"])
        self.assertEqual(S.validate([1], SCHEMA), ["expected a JSON object"])

    def test_retry_success(self):
        m = scripted(['{"city": "Pune", "days": "3"}', '{"city": "Pune", "days": 3}'])
        r = S.call_with_retries(m, "Plan a trip", SCHEMA)
        self.assertEqual((r["ok"], r["value"], r["attempts"]), (True, {"city": "Pune", "days": 3}, 2))
        self.assertEqual(r["errors"], [["days: expected int"]])

    def test_feedback_sent(self):
        m = scripted(["not json", '{"city": "X", "days": 1}'])
        S.call_with_retries(m, "p", SCHEMA)
        self.assertEqual(m.seen[1], ["p", "not json", "Your output was invalid: invalid JSON"])

    def test_exhausted(self):
        m = scripted(['{"days": 0}'] * 3)
        r = S.call_with_retries(m, "p", SCHEMA, max_attempts=3)
        self.assertEqual((r["ok"], r["attempts"], len(r["errors"])), (False, 3, 3))
        self.assertEqual(r["errors"][0], ["city: missing", "days: must be >= 1"])

    def test_first_try(self):
        r = S.call_with_retries(scripted(['{"city": "Goa", "days": 5, "mode": "bus"}']), "p", SCHEMA)
        self.assertEqual((r["attempts"], r["errors"]), (1, []))


if __name__ == "__main__":
    unittest.main()
