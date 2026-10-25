# AG-03 · Tools and Tool Calling with LangChain

**Topic:** Agentic AI · **Difficulty:** beginner · **Allowed packages:** langchain-core

**Builds on:** AG-02 Parsing Model Tool Calls, LM-17 Chat Prompts and Messages with LangChain

Read the lesson first: [article.md](article.md)

## Task

1. Define two tools with `@tool`:
   * `word_count(text: str) -> int` with docstring `"Count the words in a text."` — the number of
     whitespace-separated words;
   * `to_fahrenheit(celsius: float) -> float` with docstring `"Convert Celsius to Fahrenheit."`.
2. `run_tool_calls(message, tools)` runs every call in `message.tool_calls` with the tool of that name
   from the list `tools` and returns a list of `ToolMessage`s with `tool_call_id` set:
   * success: `content=str(result)`;
   * unknown tool: `content=f"Error: unknown tool {name}"`, `status="error"`;
   * an exception while invoking: `content=f"Error: {type(error).__name__}"`, `status="error"`.

## Hints

<details><summary>Hint 1</summary>

Put `@tool` on a normal function with type hints and a one-line docstring.

</details>

<details><summary>Hint 2</summary>

Build `by_name = {t.name: t for t in tools}` and loop over `message.tool_calls`.

</details>

<details><summary>Hint 3</summary>

Wrap `by_name[name].invoke(call["args"])` in try/except Exception and always pass `tool_call_id=call["id"]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_tool_metadata` | Decorate the functions with @tool and give them the exact docstrings. |
| `test_run_two_calls` | Return one ToolMessage per call with content=str(result) and tool_call_id=call['id']. |
| `test_unknown_tool` | Unknown tools become error ToolMessages, not exceptions. |
| `test_bad_arguments` | Catch exceptions from tool.invoke and report them with status='error'. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`@tool` turns each function into a described, schema-checked tool. The runner looks tools up by name,
answers every call with a tool message carrying its id, and converts unknown tools and invalid
arguments into error messages that the model can react to.

## References

- [Tools (LangChain docs)](https://docs.langchain.com/oss/python/langchain/tools) — LangChain (`S134`)
- [Messages (LangChain docs)](https://docs.langchain.com/oss/python/langchain/messages) — LangChain (`S130`)
