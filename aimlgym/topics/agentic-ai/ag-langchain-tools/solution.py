r"""Reference solution for AG-03 Tools and Tool Calling with LangChain.

`@tool` turns each function into a described, schema-checked tool. The runner looks tools up by name,
answers every call with a tool message carrying its id, and converts unknown tools and invalid
arguments into error messages that the model can react to.
"""
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool


@tool
def word_count(text: str) -> int:
    """Count the words in a text."""
    return len(text.split())


@tool
def to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def run_tool_calls(message, tools):
    by_name = {t.name: t for t in tools}
    results = []
    for call in message.tool_calls:
        name = call["name"]
        if name not in by_name:
            results.append(ToolMessage(content=f"Error: unknown tool {name}", tool_call_id=call["id"], status="error"))
            continue
        try:
            value = by_name[name].invoke(call["args"])
            results.append(ToolMessage(content=str(value), tool_call_id=call["id"]))
        except Exception as error:
            results.append(ToolMessage(content=f"Error: {type(error).__name__}", tool_call_id=call["id"], status="error"))
    return results
