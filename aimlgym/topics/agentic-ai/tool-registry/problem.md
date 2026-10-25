# AG-01 · Tool Registry and Dispatch

**Topic:** Agentic AI · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-17 Functions as Values

Read the lesson first: [article.md](article.md)

## Task

Implement `class ToolRegistry` with:
* `register(name, fn, schema, description="")` — raise `ValueError` if the name is already registered.
* `dispatch(call)` — `call` is a dict with keys `"tool"` and `"args"` (dict). Return
  `{"ok": True, "result": value}` or `{"ok": False, "error": message}` for: unknown tool
  (`"unknown tool '<name>'"`), missing argument (`"missing argument '<arg>'"`), unexpected argument
  (`"unexpected argument '<arg>'"`), wrong type (`"argument '<arg>' must be <type>"`, using
  `type.__name__`; bools are not ints), or an exception raised by the tool
  (`"tool error: <ExceptionType>: <message>"`). Check in that order (args in sorted order).
* `describe()` → list of `{"name", "description", "args": {arg: type_name}}` sorted by name.

**Example**
```python
reg = ToolRegistry(); reg.register("add", lambda a, b: a + b, {"a": int, "b": int}, "Add two ints")
reg.dispatch({"tool": "add", "args": {"a": 2, "b": 3}})     # {'ok': True, 'result': 5}
reg.dispatch({"tool": "add", "args": {"a": 2}})             # {'ok': False, 'error': "missing argument 'b'"}
```

## Hints

<details><summary>Hint 1</summary>

Store `self._tools[name] = (fn, schema, description)`.

</details>

<details><summary>Hint 2</summary>

Check missing = sorted(schema − args), unexpected = sorted(args − schema), then types.

</details>

<details><summary>Hint 3</summary>

Wrap `fn(**args)` in `try/except Exception as e` and format `type(e).__name__`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_tool_exception` | Catch exceptions from the tool and return them as an error dict. |
| `test_types` | Reject bools for int/float parameters; floats accept ints. |
| `test_missing_and_unexpected` | Check missing args before unexpected args, each in sorted order. |
| `test_describe` | Return tools sorted by name with argument type names. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Dispatch validates in a fixed order — tool exists, required args present, no extras, correct types —
and only then runs the tool inside a try/except so that any failure is reported as a structured error
the model can read. Floats accept ints; bools are rejected for numeric types.

## References

- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
