"""Tests for AG-06 ReAct Loop with a Scripted Model.

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


import json

class Reg:
    def __init__(self):
        self.calls = []
    def dispatch(self, call):
        self.calls.append(call)
        if call["tool"] == "add":
            return {"ok": True, "result": call["args"]["a"] + call["args"]["b"]}
        return {"ok": False, "error": f"unknown tool '{call['tool']}'"}

def scripted(replies):
    seen = []
    def model(transcript):
        seen.append(transcript)
        return replies[min(len(seen) - 1, len(replies) - 1)]
    model.seen = seen
    return model

ADD = '<tool_call>{"tool": "add", "args": {"a": 2, "b": 3}}</tool_call>'

class TestReAct(unittest.TestCase):
    def test_final_after_tool(self):
        r = S.react_agent(scripted([ADD, "FINAL: 5"]), Reg(), "What is 2 + 3?")
        self.assertEqual((r["status"], r["answer"], r["tool_calls"]), ("final", "5", 1))

    def test_transcript_shape(self):
        r = S.react_agent(scripted([ADD, "FINAL: 5"]), Reg(), "q")
        self.assertEqual([m["role"] for m in r["transcript"]], ["user", "assistant", "tool", "assistant"])
        self.assertEqual(json.loads(r["transcript"][2]["content"]), {"ok": True, "result": 5})

    def test_model_sees_observation(self):
        m = scripted([ADD, "FINAL: 5"])
        S.react_agent(m, Reg(), "q")
        self.assertEqual(m.seen[1][-1]["role"], "tool")

    def test_invalid_reported(self):
        r = S.react_agent(scripted(["hmm", "FINAL: ok"]), Reg(), "q")
        self.assertEqual(json.loads(r["transcript"][2]["content"]), {"ok": False, "error": "no tool call or final answer"})
        self.assertEqual(r["tool_calls"], 0)

    def test_step_limit(self):
        reg = Reg()
        r = S.react_agent(scripted([ADD]), reg, "q", max_steps=3)
        self.assertEqual((r["status"], r["answer"], r["tool_calls"], len(reg.calls)), ("step_limit", None, 3, 3))

    def test_tool_error_observed(self):
        r = S.react_agent(scripted(['<tool_call>{"tool": "web"}</tool_call>', "FINAL: sorry"]), Reg(), "q")
        self.assertIn("unknown tool", r["transcript"][2]["content"])

    def test_immediate_final(self):
        r = S.react_agent(scripted(["FINAL: hi"]), Reg(), "q")
        self.assertEqual((r["answer"], len(r["transcript"])), ("hi", 2))


if __name__ == "__main__":
    unittest.main()
