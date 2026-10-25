# AG-02 · Parsing Model Tool Calls

**Topic:** Agentic AI · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** AG-01 Tool Registry and Dispatch, NL-01 Regular Expressions for Text

Read the lesson first: [article.md](article.md)

## Task

Write `parse_model_output(text)` returning one of:
* `{"type": "tool_call", "tool": str, "args": dict}` — exactly one `<tool_call>...</tool_call>` block
  containing a JSON object with string `"tool"` and (optional, default `{}`) dict `"args"`;
* `{"type": "final", "content": str}` — no tool-call tags and `text.lstrip()` starts with `FINAL:`
  (content = the rest, stripped);
* `{"type": "invalid", "error": str}` — anything else. Error messages: `"no tool call or final answer"`,
  `"multiple tool calls"`, `"invalid JSON"`, `"tool call must be an object with 'tool' and 'args'"`.

**Examples**
```python
parse_model_output('<tool_call>{"tool": "add", "args": {"a": 1}}</tool_call>')
# {'type': 'tool_call', 'tool': 'add', 'args': {'a': 1}}
parse_model_output("  FINAL: 42 ")      # {'type': 'final', 'content': '42'}
parse_model_output("<tool_call>{oops}</tool_call>")   # {'type': 'invalid', 'error': 'invalid JSON'}
```

## Hints

<details><summary>Hint 1</summary>

`blocks = re.findall(r'<tool_call>(.*?)</tool_call>', text, re.DOTALL)`.

</details>

<details><summary>Hint 2</summary>

If `len(blocks) > 1` → multiple; if 1 → `json.loads` in try/except `json.JSONDecodeError`.

</details>

<details><summary>Hint 3</summary>

Validate `isinstance(obj, dict)`, `isinstance(obj.get('tool'), str)`, `isinstance(obj.get('args', {}), dict)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_multiple` | Use a non-greedy pattern (.*?) and reject more than one block. |
| `test_multiline` | Pass re.DOTALL so '.' matches newlines. |
| `test_no_eval` | Only use json.loads; never eval model output. |
| `test_final` | Accept 'FINAL:' after leading whitespace and strip the content. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A non-greedy, DOTALL regex finds every tag pair. The parser enforces exactly one call, decodes it with
`json.loads` (never `eval`) and validates its shape. Without tags, only an explicit `FINAL:` prefix is
accepted; everything else becomes an error message for the agent loop.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Shunyu Yao et al. (`S036`)
