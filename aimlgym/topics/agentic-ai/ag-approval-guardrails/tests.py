"""Tests for AG-18 Guardrails with Human Approval.

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


SENT = []


def send_email(to, text):
    SENT.append((to, text))
    return "sent"


TOOLS = {"read_calendar": lambda day="today": f"3 events {day}", "send_email": send_email}


class TestApproval(unittest.TestCase):
    def setUp(self):
        SENT.clear()
        self.app = S.build_guarded_graph(TOOLS, {"send_email"})

    def test_safe_action_runs_without_asking(self):
        asked = []
        outcome = S.run_with_approval(self.app, {"tool": "read_calendar", "args": {"day": "monday"}}, "t1",
                                      lambda payload: asked.append(payload) or "approve")
        self.assertEqual((outcome, asked), ("approved: 3 events monday", []))

    def test_sensitive_action_approved(self):
        seen = []
        action = {"tool": "send_email", "args": {"to": "club@example.org", "text": "Meeting at 5"}}
        outcome = S.run_with_approval(self.app, action, "t2", lambda payload: seen.append(payload) or "approve")
        self.assertEqual(outcome, "approved: sent")
        self.assertEqual(seen, [{"action": action}])
        self.assertEqual(SENT, [("club@example.org", "Meeting at 5")])

    def test_sensitive_action_rejected(self):
        action = {"tool": "send_email", "args": {"to": "all@example.org", "text": "Spam"}}
        self.assertEqual(S.run_with_approval(self.app, action, "t3", lambda payload: "reject"), "rejected")
        self.assertEqual(SENT, [])

    def test_only_exact_approve(self):
        action = {"tool": "send_email", "args": {"to": "a@example.org", "text": "x"}}
        self.assertEqual(S.run_with_approval(self.app, action, "t4", lambda payload: "yes please"), "rejected")

    def test_unknown_tool_blocked(self):
        self.assertEqual(S.run_with_approval(self.app, {"tool": "delete_all", "args": {}}, "t5", lambda p: "approve"), "blocked")

    def test_sent_once_after_resume(self):
        action = {"tool": "send_email", "args": {"to": "b@example.org", "text": "once"}}
        S.run_with_approval(self.app, action, "t6", lambda payload: "approve")
        self.assertEqual(len(SENT), 1)


if __name__ == "__main__":
    unittest.main()
