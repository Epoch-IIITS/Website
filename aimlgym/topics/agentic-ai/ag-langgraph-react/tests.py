"""Tests for AG-08 A ReAct Agent in LangGraph.

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


from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage


class Scripted(GenericFakeChatModel):
    """Replays the given AI messages in order; bind_tools returns the model unchanged."""
    def bind_tools(self, tools, **kwargs):
        return self


def call(name, args, call_id="call_1"):
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": call_id}])


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def two_step_model():
    return Scripted(messages=iter([call("multiply", {"a": 17, "b": 23}, "c1"), call("add", {"a": 391, "b": 5}, "c2"),
                                   AIMessage("The answer is 396.")]))


class TestReactGraph(unittest.TestCase):
    def test_answers_after_tools(self):
        app = S.build_agent(two_step_model(), [multiply, add])
        self.assertEqual(S.run_agent(app, "17 * 23 + 5?", "t1"), "The answer is 396.")

    def test_message_history(self):
        app = S.build_agent(two_step_model(), [multiply, add])
        S.run_agent(app, "17 * 23 + 5?", "t1")
        msgs = app.get_state({"configurable": {"thread_id": "t1"}}).values["messages"]
        self.assertEqual([m.type for m in msgs], ["human", "ai", "tool", "ai", "tool", "ai"])
        self.assertEqual([m.content for m in msgs if m.type == "tool"], ["391", "396"])

    def test_step_limit(self):
        looping = Scripted(messages=iter([call("add", {"a": 1, "b": 1}, f"c{i}") for i in range(50)]))
        app = S.build_agent(looping, [add])
        self.assertEqual(S.run_agent(app, "loop", "t2", max_steps=6), "Stopped: step limit reached")

    def test_threads_are_separate(self):
        model = Scripted(messages=iter([AIMessage("Hi Alice."), AIMessage("Hi Bob."), AIMessage("Again, Alice.")]))
        app = S.build_agent(model, [add])
        S.run_agent(app, "I am Alice", "alice")
        S.run_agent(app, "I am Bob", "bob")
        S.run_agent(app, "Remember me?", "alice")
        alice = app.get_state({"configurable": {"thread_id": "alice"}}).values["messages"]
        bob = app.get_state({"configurable": {"thread_id": "bob"}}).values["messages"]
        self.assertEqual((len(alice), len(bob)), (4, 2))

    def test_tool_error_reaches_model(self):
        model = Scripted(messages=iter([call("add", {"a": "x", "b": 1}), AIMessage("Sorry, that failed.")]))
        app = S.build_agent(model, [add])
        self.assertEqual(S.run_agent(app, "bad", "t3"), "Sorry, that failed.")
        tool_msg = app.get_state({"configurable": {"thread_id": "t3"}}).values["messages"][2]
        self.assertEqual(tool_msg.type, "tool")

    def test_direct_answer(self):
        app = S.build_agent(Scripted(messages=iter([AIMessage("No tools needed.")])), [add])
        self.assertEqual(S.run_agent(app, "hello", "t4"), "No tools needed.")


if __name__ == "__main__":
    unittest.main()
