# Parsing What the Model Said

## Learning outcomes

After this lesson you can:

- Extract structured tool calls from free text
- Distinguish tool calls, final answers and malformed output
- Never execute anything during parsing

## Intuition
Model output is text, and text can be malformed: missing braces, extra prose, two calls at once. The
agent needs a strict parser that turns text into one of a few well-defined cases — and treats
anything else as an error to report back, not something to guess at.

## Precise explanation
Protocol used in this course (a common pattern; real APIs often return structured tool calls natively):
* A tool call is wrapped in tags: `<tool_call>{"tool": "...", "args": {...}}</tool_call>`. Exactly one
  call per message.
* A final answer starts with `FINAL:` (after optional leading whitespace).
* Anything else is invalid.
Parse with `re` to find tag contents (non-greedy, `re.DOTALL`), then `json.loads`. Validate the
structure: a JSON object with a string `"tool"` and a dict `"args"` (default `{}`).
Parsing must be **side-effect free** — never call tools here.

## Worked example
`'I will add. <tool_call>{"tool": "add", "args": {"a": 1, "b": 2}}</tool_call>'` →
`{"type": "tool_call", "tool": "add", "args": {"a": 1, "b": 2}}`.
`'FINAL: 3'` → `{"type": "final", "content": "3"}`.

## Common mistakes
* Greedy regex swallowing two calls.
* `eval` on model output (arbitrary code execution!).
* Accepting both a final answer and a tool call in the same message without a rule.

## Why this matters
Robust parsing turns model unreliability into recoverable errors (AG-15) and is a security boundary.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Shunyu Yao et al. (`S036`)
