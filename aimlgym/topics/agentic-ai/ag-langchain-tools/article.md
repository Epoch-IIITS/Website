# Tools and Tool Calling with LangChain

## Learning outcomes

After this lesson you can:

- Define tools with the @tool decorator, a docstring and type hints
- Read tool calls from an AIMessage and answer them with ToolMessages
- Turn tool errors into messages the model can read instead of crashes

## Intuition
In AG-01 and AG-02 you kept a dict of functions and parsed a text format for
calling them. Modern chat models do the parsing for you: you describe each tool (name, purpose,
arguments) and the model replies with **structured tool calls**. Your code runs them and sends the
results back as tool messages.

## Precise explanation
```python
from langchain_core.tools import tool

@tool
def word_count(text: str) -> int:
    """Count the words in a text."""
    return len(text.split())

word_count.name, word_count.description, word_count.args   # 'word_count', the docstring, a JSON schema
word_count.invoke({"text": "hello there"})                  # 2
model_with_tools = model.bind_tools([word_count])           # the model now knows the tool
```

* The **docstring becomes the description** the model reads, and the type hints become the argument
  schema — both are part of the prompt, so write them carefully.
* A model reply asking for tools is an `AIMessage` whose `tool_calls` is a list of dicts
  `{"name": ..., "args": {...}, "id": ...}`; several calls can come at once.
* Each result goes back as `ToolMessage(content=str(result), tool_call_id=call["id"])`, so the model can
  match results to calls. Use `status="error"` for failures.
* `tool.invoke(args)` validates arguments against the schema and raises an error (a `ValueError`
  subclass from Pydantic) for missing or wrongly typed arguments.

## Worked example
The model replies with two calls: `word_count({"text": "to be or not"})` and
`to_fahrenheit({"celsius": 100})`. Running them gives tool messages "4" and "212.0". A call to
`delete_files` (not registered) gets the error message "Error: unknown tool delete_files" instead of
crashing the agent.

## What the library does inside
`@tool` wraps your function in an object with a name, description and Pydantic argument schema — a
richer version of your registry — and providers convert those into their function-calling format.

## Common mistakes
* No docstring: the model has no idea when to use the tool.
* Returning the result without the matching `tool_call_id`.
* Letting a bad argument or unknown tool raise and stop the whole agent.

## Why this matters
Tool calling turns a chat model into an agent; every LangGraph agent in this topic uses this exact
message protocol.

## References

- [Tools (LangChain docs)](https://docs.langchain.com/oss/python/langchain/tools) — LangChain (`S134`)
- [Messages (LangChain docs)](https://docs.langchain.com/oss/python/langchain/messages) — LangChain (`S130`)
