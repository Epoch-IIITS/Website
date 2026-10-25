r"""Reference solution for AG-06 ReAct Loop with a Scripted Model.

Each iteration asks the model for its next message, parses it, and either finishes, executes a tool,
or reports a parse error — always appending an observation so the model sees the consequence of its
action. The step limit guarantees termination.
"""
import json
import re

TAG = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)


def parse_model_output(text):
    blocks = TAG.findall(text)
    if len(blocks) > 1:
        return {"type": "invalid", "error": "multiple tool calls"}
    if len(blocks) == 1:
        try:
            obj = json.loads(blocks[0])
        except json.JSONDecodeError:
            return {"type": "invalid", "error": "invalid JSON"}
        if (not isinstance(obj, dict) or not isinstance(obj.get("tool"), str)
                or not isinstance(obj.get("args", {}), dict)):
            return {"type": "invalid", "error": "tool call must be an object with 'tool' and 'args'"}
        return {"type": "tool_call", "tool": obj["tool"], "args": obj.get("args", {})}
    stripped = text.lstrip()
    if stripped.startswith("FINAL:"):
        return {"type": "final", "content": stripped[len("FINAL:"):].strip()}
    return {"type": "invalid", "error": "no tool call or final answer"}


def react_agent(model, registry, question, max_steps=5):
    transcript = [{"role": "user", "content": question}]
    tool_calls = 0
    for _ in range(max_steps):
        text = model(list(transcript))
        transcript.append({"role": "assistant", "content": text})
        p = parse_model_output(text)
        if p["type"] == "final":
            return {"status": "final", "answer": p["content"], "transcript": transcript, "tool_calls": tool_calls}
        if p["type"] == "tool_call":
            res = registry.dispatch({"tool": p["tool"], "args": p["args"]})
            tool_calls += 1
        else:
            res = {"ok": False, "error": p["error"]}
        transcript.append({"role": "tool", "content": json.dumps(res)})
    return {"status": "step_limit", "answer": None, "transcript": transcript, "tool_calls": tool_calls}
