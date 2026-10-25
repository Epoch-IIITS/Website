"""Tests for AG-14 Validating Tool Arguments and Retrying.

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


from langchain_core.messages import AIMessage, HumanMessage
from pydantic import ValidationError

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage


class Scripted(GenericFakeChatModel):
    """Replays the given AI messages in order; bind_tools returns the model unchanged."""
    def bind_tools(self, tools, **kwargs):
        return self


def call(name, args, call_id="call_1"):
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": call_id}])


SEEN = []


class Recording(Scripted):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        SEEN.append(list(messages))
        return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)


class TestValidatedCalls(unittest.TestCase):
    def test_schema(self):
        self.assertEqual(S.book_room.invoke({"room": "R101", "hour": 10}), "booked R101 at 10:00")
        with self.assertRaises(ValidationError):
            S.book_room.invoke({"room": "101", "hour": 10})
        with self.assertRaises(ValidationError):
            S.book_room.invoke({"room": "R101", "hour": 20})

    def test_success_first_try(self):
        model = Scripted(messages=iter([call("book_room", {"room": "R202", "hour": 9})]))
        self.assertEqual(S.call_with_validation(model, S.book_room, [HumanMessage("book")]), ("booked R202 at 9:00", 1))

    def test_retry_with_feedback(self):
        SEEN.clear()
        model = Recording(messages=iter([call("book_room", {"room": "101", "hour": 20}, "c1"),
                                         call("book_room", {"room": "R101", "hour": 16}, "c2")]))
        result = S.call_with_validation(model, S.book_room, [HumanMessage("book R101 at 4pm")])
        self.assertEqual(result, ("booked R101 at 16:00", 2))
        feedback = SEEN[1][-1]
        self.assertEqual((feedback.type, feedback.status, feedback.tool_call_id), ("tool", "error", "c1"))
        self.assertIn("room:", feedback.content)
        self.assertIn("hour:", feedback.content)

    def test_gives_up(self):
        model = Scripted(messages=iter([call("book_room", {"room": "x", "hour": 1}, f"c{i}") for i in range(5)]))
        self.assertEqual(S.call_with_validation(model, S.book_room, [HumanMessage("book")], max_attempts=3), (None, 3))

    def test_no_tool_call(self):
        model = Scripted(messages=iter([AIMessage("I cannot book that.")]))
        self.assertEqual(S.call_with_validation(model, S.book_room, [HumanMessage("book")]), (None, 1))

    def test_caller_messages_unchanged(self):
        msgs = [HumanMessage("book")]
        model = Scripted(messages=iter([call("book_room", {"room": "1", "hour": 9}), call("book_room", {"room": "R100", "hour": 9})]))
        S.call_with_validation(model, S.book_room, msgs)
        self.assertEqual(len(msgs), 1)


if __name__ == "__main__":
    unittest.main()
