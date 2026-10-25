r"""Reference solution for AG-02 Parsing Model Tool Calls.

A non-greedy, DOTALL regex finds every tag pair. The parser enforces exactly one call, decodes it with
`json.loads` (never `eval`) and validates its shape. Without tags, only an explicit `FINAL:` prefix is
accepted; everything else becomes an error message for the agent loop.
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
