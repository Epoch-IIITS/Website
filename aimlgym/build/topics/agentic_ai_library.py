"""Agents with LangChain and LangGraph (library revision, Phase 5).

Library steps are followed by the from-scratch versions they replace on the required path, kept as
optional deep dives: [[memory-window]], [[validate-and-retry]], [[orchestrator-workers]],
[[permission-guardrails]].
"""

AGENT_PACKAGES = ["langchain-core", "langgraph"]

# A scripted chat model for tests: GenericFakeChatModel replays messages but cannot bind tools.
SCRIPTED = r'''
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage


class Scripted(GenericFakeChatModel):
    """Replays the given AI messages in order; bind_tools returns the model unchanged."""
    def bind_tools(self, tools, **kwargs):
        return self


def call(name, args, call_id="call_1"):
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": call_id}])
'''

PROBLEMS = [
# ---------------------------------------------------------------- ag-langchain-tools
{
"slug": "ag-langchain-tools", "title": "Tools and Tool Calling with LangChain",
"difficulty": "beginner", "prereqs": ["parse-tool-call", "lm-chat-prompt-langchain"], "packages": ["langchain-core"],
"objectives": ["Define tools with the @tool decorator, a docstring and type hints",
               "Read tool calls from an AIMessage and answer them with ToolMessages",
               "Turn tool errors into messages the model can read instead of crashes"],
"tags": ["langchain", "tools", "tool-calling", "function-calling"],
"sources": ["S134", "S130"], "entry": "word_count; to_fahrenheit; run_tool_calls(message, tools)",
"article": r'''
# Tools and Tool Calling with LangChain

## Intuition
In [[tool-registry]] and [[parse-tool-call]] you kept a dict of functions and parsed a text format for
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
''',
"statement": r'''
1. Define two tools with `@tool`:
   * `word_count(text: str) -> int` with docstring `"Count the words in a text."` — the number of
     whitespace-separated words;
   * `to_fahrenheit(celsius: float) -> float` with docstring `"Convert Celsius to Fahrenheit."`.
2. `run_tool_calls(message, tools)` runs every call in `message.tool_calls` with the tool of that name
   from the list `tools` and returns a list of `ToolMessage`s with `tool_call_id` set:
   * success: `content=str(result)`;
   * unknown tool: `content=f"Error: unknown tool {name}"`, `status="error"`;
   * an exception while invoking: `content=f"Error: {type(error).__name__}"`, `status="error"`.
''',
"starter": r'''
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool


# TODO: word_count and to_fahrenheit tools


def run_tool_calls(message, tools):
    # TODO
    pass
''',
"hints": [
    "Put `@tool` on a normal function with type hints and a one-line docstring.",
    "Build `by_name = {t.name: t for t in tools}` and loop over `message.tool_calls`.",
    "Wrap `by_name[name].invoke(call[\"args\"])` in try/except Exception and always pass `tool_call_id=call[\"id\"]`.",
],
"solution": r'''
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
''',
"explanation": r'''
`@tool` turns each function into a described, schema-checked tool. The runner looks tools up by name,
answers every call with a tool message carrying its id, and converts unknown tools and invalid
arguments into error messages that the model can react to.
''',
"tests": r'''
from langchain_core.messages import AIMessage, ToolMessage


def calls(*items):
    return AIMessage(content="", tool_calls=[{"name": n, "args": a, "id": f"call_{i}"} for i, (n, a) in enumerate(items)])


class TestTools(unittest.TestCase):
    def test_tool_metadata(self):
        self.assertEqual(S.word_count.name, "word_count")
        self.assertEqual(S.word_count.description, "Count the words in a text.")
        self.assertEqual(set(S.to_fahrenheit.args), {"celsius"})

    def test_tools_compute(self):
        self.assertEqual(S.word_count.invoke({"text": "to be or not"}), 4)
        self.assertEqual(S.to_fahrenheit.invoke({"celsius": 100}), 212.0)

    def test_run_two_calls(self):
        out = S.run_tool_calls(calls(("word_count", {"text": "to be or not"}), ("to_fahrenheit", {"celsius": 100})),
                               [S.word_count, S.to_fahrenheit])
        self.assertEqual([(m.content, m.tool_call_id) for m in out], [("4", "call_0"), ("212.0", "call_1")])
        self.assertTrue(all(isinstance(m, ToolMessage) for m in out))

    def test_unknown_tool(self):
        [msg] = S.run_tool_calls(calls(("delete_files", {})), [S.word_count])
        self.assertEqual((msg.content, msg.status, msg.tool_call_id), ("Error: unknown tool delete_files", "error", "call_0"))

    def test_bad_arguments(self):
        [msg] = S.run_tool_calls(calls(("to_fahrenheit", {"celsius": "hot"})), [S.to_fahrenheit])
        self.assertEqual(msg.status, "error")
        self.assertTrue(msg.content.startswith("Error: "))

    def test_no_calls(self):
        self.assertEqual(S.run_tool_calls(AIMessage(content="done"), [S.word_count]), [])
''',
"feedback": [
    ("test_tool_metadata", "Decorate the functions with @tool and give them the exact docstrings."),
    ("test_run_two_calls", "Return one ToolMessage per call with content=str(result) and tool_call_id=call['id']."),
    ("test_unknown_tool", "Unknown tools become error ToolMessages, not exceptions."),
    ("test_bad_arguments", "Catch exceptions from tool.invoke and report them with status='error'."),
],
},
# ---------------------------------------------------------------- ag-langgraph-basics
{
"slug": "ag-langgraph-basics", "title": "LangGraph Basics: State, Nodes and Edges",
"difficulty": "intermediate", "prereqs": ["react-loop", "ag-langchain-tools"], "packages": ["langgraph"],
"objectives": ["Describe a workflow as a StateGraph with a typed state",
               "Write nodes that return partial state updates and use a reducer to accumulate lists",
               "Route between nodes with conditional edges, including loops"],
"tags": ["langgraph", "state-machines", "workflows", "graphs"],
"sources": ["S136", "S139"], "entry": "build_cleaner(max_words)",
"article": r'''
# LangGraph Basics: State, Nodes and Edges

## Intuition
Your agent loops so far were `while` loops with `if`s inside. As workflows grow — retries,
approvals, several workers — that control flow becomes hard to read and test. LangGraph makes it
explicit: a **state** dict, **nodes** that read the state and return updates, and **edges** that
decide which node runs next.

## Precise explanation
```python
import operator
from typing import Annotated, TypedDict
from langgraph.graph import END, START, StateGraph

class State(TypedDict):
    text: str
    steps: Annotated[list[str], operator.add]      # reducer: updates are appended, not replaced

def strip(state):
    return {"text": state["text"].strip(), "steps": ["strip"]}    # return only what changes

graph = StateGraph(State)
graph.add_node("strip", strip)
graph.add_edge(START, "strip")
graph.add_conditional_edges("check", route)        # route(state) returns a node name or END
app = graph.compile()
app.invoke({"text": "  Hello ", "steps": []})      # the final state
```

* A node returns a **partial update**. Keys without a reducer are overwritten; a key annotated with a
  reducer such as `operator.add` combines the old and new values. (`operator.add(a, b)` is `a + b` as a
  function, from the standard-library `operator` module; for lists it concatenates.)
* `add_conditional_edges(node, route)` calls `route(state)` after the node and follows the returned
  name, which may point back to an earlier node to form a loop.
* `compile()` checks the graph (unknown nodes, unreachable nodes) and returns a runnable with
  `invoke`. `app.get_graph().nodes` lists the nodes; LangGraph can also draw the graph.
* A loop that never ends stops with `GraphRecursionError` after `recursion_limit` steps (default 25).

## Worked example
For "  The Quick Brown Fox Jumps  " and `max_words=3`: strip, lower, check (5 words, too long),
shorten, check (4), shorten, check (3, done). The final text is "the quick brown" and `steps` is
["strip", "lower", "shorten", "shorten"].

## Common mistakes
* Mutating `state` inside a node instead of returning an update.
* Forgetting the reducer, so each node's list replaces the previous one.
* A routing function that returns a name that is not a node.

## Why this matters
The ReAct agent, orchestrator and guardrail steps that follow are LangGraph graphs; reading and
drawing them is how you debug agents.
''',
"statement": r'''
Write `build_cleaner(max_words)` returning a compiled graph over the state
`{"text": str, "steps": Annotated[list[str], operator.add]}` with nodes:

* `"strip"`: strips surrounding whitespace, step `"strip"`;
* `"lower"`: lowercases, step `"lower"`;
* `"check"`: no change (return `{}`);
* `"shorten"`: removes the last word, step `"shorten"`.

Edges: START → strip → lower → check; after `check`, go to `"shorten"` if the text has more than
`max_words` words, otherwise END; shorten → check. Raise `ValueError` if `max_words < 1`.
''',
"starter": r'''
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class CleanerState(TypedDict):
    text: str
    steps: Annotated[list[str], operator.add]


def build_cleaner(max_words):
    # TODO
    pass
''',
"hints": [
    "Each node is a small function returning a dict, e.g. `lambda s: {\"text\": s[\"text\"].lower(), \"steps\": [\"lower\"]}`.",
    "`route = lambda s: \"shorten\" if len(s[\"text\"].split()) > max_words else END`.",
    "Add the nodes, the fixed edges, `add_conditional_edges(\"check\", route)` and `add_edge(\"shorten\", \"check\")`, then `compile()`.",
],
"solution": r'''
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class CleanerState(TypedDict):
    text: str
    steps: Annotated[list[str], operator.add]


def build_cleaner(max_words):
    if max_words < 1:
        raise ValueError("max_words must be at least 1")

    def route(state):
        return "shorten" if len(state["text"].split()) > max_words else END

    graph = StateGraph(CleanerState)
    graph.add_node("strip", lambda s: {"text": s["text"].strip(), "steps": ["strip"]})
    graph.add_node("lower", lambda s: {"text": s["text"].lower(), "steps": ["lower"]})
    graph.add_node("check", lambda s: {})
    graph.add_node("shorten", lambda s: {"text": " ".join(s["text"].split()[:-1]), "steps": ["shorten"]})
    graph.add_edge(START, "strip")
    graph.add_edge("strip", "lower")
    graph.add_edge("lower", "check")
    graph.add_conditional_edges("check", route)
    graph.add_edge("shorten", "check")
    return graph.compile()
''',
"explanation": r'''
Each node returns only the keys it changes; the `operator.add` reducer appends step names. The
conditional edge after `check` either loops through `shorten` or ends, so the loop's condition lives
in one routing function rather than inside the nodes.
''',
"tests": r'''
from langgraph.errors import GraphRecursionError


class TestCleanerGraph(unittest.TestCase):
    def test_worked_example(self):
        out = S.build_cleaner(3).invoke({"text": "  The Quick Brown Fox Jumps  ", "steps": []})
        self.assertEqual(out["text"], "the quick brown")
        self.assertEqual(out["steps"], ["strip", "lower", "shorten", "shorten"])

    def test_short_text_skips_loop(self):
        out = S.build_cleaner(5).invoke({"text": " Hi There ", "steps": []})
        self.assertEqual((out["text"], out["steps"]), ("hi there", ["strip", "lower"]))

    def test_reducer_keeps_existing_steps(self):
        out = S.build_cleaner(5).invoke({"text": "a", "steps": ["start"]})
        self.assertEqual(out["steps"], ["start", "strip", "lower"])

    def test_nodes(self):
        nodes = set(S.build_cleaner(2).get_graph().nodes)
        self.assertTrue({"strip", "lower", "check", "shorten"} <= nodes)

    def test_recursion_limit(self):
        app = S.build_cleaner(1)
        with self.assertRaises(GraphRecursionError):
            app.invoke({"text": " ".join(["w"] * 40), "steps": []}, {"recursion_limit": 10})

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.build_cleaner(0)
''',
"feedback": [
    ("test_worked_example", "Route from check to shorten while there are more than max_words words; shorten loops back to check."),
    ("test_reducer_keeps_existing_steps", "Annotate steps with operator.add and return only new steps from each node."),
    ("test_nodes", "Name the nodes strip, lower, check and shorten."),
    ("test_invalid", "Raise ValueError when max_words < 1."),
],
},
# ---------------------------------------------------------------- ag-langgraph-react
{
"slug": "ag-langgraph-react", "title": "A ReAct Agent in LangGraph",
"difficulty": "intermediate", "prereqs": ["ag-langgraph-basics"], "packages": AGENT_PACKAGES,
"objectives": ["Build an agent graph from a model node, a ToolNode and tools_condition",
               "Limit the number of steps with recursion_limit",
               "Keep conversations per thread with an InMemorySaver checkpointer"],
"tags": ["langgraph", "react", "agents", "tool-calling", "checkpoints"],
"sources": ["S139", "S137"], "entry": "build_agent(model, tools); run_agent(app, question, thread_id, max_steps=8)",
"article": r'''
# A ReAct Agent in LangGraph

## Intuition
The ReAct loop of [[react-loop]] alternates thinking and acting: the model decides on a tool, the
tool runs, the model reads the result, and so on until it answers. In LangGraph that loop is two nodes
and a conditional edge — plus, for free, a step limit and saved conversation history.

## Precise explanation
```python
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

bound = model.bind_tools(tools)
def agent(state):
    return {"messages": [bound.invoke(state["messages"])]}

graph = StateGraph(MessagesState)                    # {"messages": [...]} with an add_messages reducer
graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))            # runs the tool calls of the last AI message
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)   # "tools" if there are tool calls, else END
graph.add_edge("tools", "agent")
app = graph.compile(checkpointer=InMemorySaver())
app.invoke({"messages": [HumanMessage("...")]}, {"configurable": {"thread_id": "alice"}, "recursion_limit": 8})
```

* `MessagesState`'s reducer appends new messages, so the history grows: human, ai (tool calls), tool,
  ai, …
* `ToolNode` executes the calls and returns `ToolMessage`s, turning tool errors into messages.
* `recursion_limit` caps the total number of node executions; reaching it raises
  `GraphRecursionError` — the budget of [[goal-and-budget]].
* With a **checkpointer**, each `thread_id` keeps its own state between calls; the next `invoke` on
  the same thread continues the conversation. `app.get_state(config).values` shows it.

## Worked example
"What is 17 × 23 + 5?" The model calls `multiply(17, 23)`, reads 391, calls `add(391, 5)`, reads 396
and answers "396". The thread then holds six messages: human, ai, tool, ai, tool, ai.

## Common mistakes
* Forgetting the edge from tools back to the agent, so the model never sees the result.
* No step limit, so a confused model loops until the default limit (or your bill) stops it.
* Reusing one thread id for different users.

## Why this matters
This graph is the core of most tool-using assistants; the study-planner project idea after this step
adds real tools to it.
''',
"statement": r'''
1. `build_agent(model, tools)` returns the compiled graph from the lesson: nodes `"agent"` (calls
   `model.bind_tools(tools)` on the messages) and `"tools"` (`ToolNode(tools)`), `tools_condition`
   routing, and an `InMemorySaver` checkpointer.
2. `run_agent(app, question, thread_id, max_steps=8)` invokes the graph with a `HumanMessage(question)`,
   `thread_id` and `recursion_limit=max_steps`, and returns the content of the last message. If the
   limit is reached (`GraphRecursionError`), return `"Stopped: step limit reached"`.
''',
"starter": r'''
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.errors import GraphRecursionError
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


def build_agent(model, tools):
    # TODO
    pass


def run_agent(app, question, thread_id, max_steps=8):
    # TODO
    pass
''',
"hints": [
    "Bind the tools once outside the node function: `bound = model.bind_tools(tools)`.",
    "Edges: START → agent, conditional edges with tools_condition, tools → agent; compile with `checkpointer=InMemorySaver()`.",
    "The config is `{\"configurable\": {\"thread_id\": thread_id}, \"recursion_limit\": max_steps}`; read `result[\"messages\"][-1].content`.",
],
"solution": r'''
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.errors import GraphRecursionError
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


def build_agent(model, tools):
    bound = model.bind_tools(tools)

    def agent(state):
        return {"messages": [bound.invoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    return graph.compile(checkpointer=InMemorySaver())


def run_agent(app, question, thread_id, max_steps=8):
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": max_steps}
    try:
        result = app.invoke({"messages": [HumanMessage(question)]}, config)
    except GraphRecursionError:
        return "Stopped: step limit reached"
    return result["messages"][-1].content
''',
"explanation": r'''
The agent node asks the model for its next move; `tools_condition` sends tool calls to the ToolNode
and plain answers to the end, and the tool results flow back to the model. The checkpointer stores
each thread's messages, and the recursion limit turns a runaway loop into a clear message.
''',
"tests": r'''
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
''' + SCRIPTED + r'''

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
''',
"feedback": [
    ("test_answers_after_tools", "Route with tools_condition and add an edge from tools back to agent."),
    ("test_step_limit", "Pass recursion_limit=max_steps and catch GraphRecursionError."),
    ("test_threads_are_separate", "Compile with InMemorySaver() and pass the thread_id in the config."),
    ("test_tool_error_reaches_model", "Use ToolNode(tools), which reports tool errors as messages."),
],
},
# ---------------------------------------------------------------- ag-message-memory
{
"slug": "ag-message-memory", "title": "Conversation Memory with trim_messages",
"difficulty": "intermediate", "prereqs": ["ag-langgraph-react"], "packages": ["langchain-core"],
"objectives": ["Keep a conversation within a budget with trim_messages",
               "Keep the system message and start the kept history on a human turn",
               "Write a custom token counter"],
"tags": ["langchain", "memory", "context-window", "messages"],
"sources": ["S135", "S130"], "entry": "trim_history(messages, max_messages); count_words(messages); trim_by_words(messages, max_words)",
"article": r'''
# Conversation Memory with trim_messages

## Intuition
A model can only read a limited context, and every token costs time and money. Long conversations must
be cut down: keep the system instructions, keep the most recent turns, drop the oldest — without
leaving a reply whose question was dropped.

## Precise explanation
```python
from langchain_core.messages import trim_messages

trim_messages(messages, max_tokens=4, token_counter=len,       # len counts messages
              strategy="last", include_system=True, start_on="human")
```

* `strategy="last"` keeps the end of the conversation; `include_system=True` always keeps a leading
  system message (it counts towards the budget).
* `start_on="human"` drops messages from the front of the kept window until it starts with a human
  message, so the history never opens with an orphaned AI reply or tool result.
* `token_counter` is either a model (to count real tokens) or a function that receives a **list of
  messages** and returns a number. `len` counts messages; a word counter approximates tokens.
* Trimming returns a new list; the stored history is unchanged.

## Worked example
[system, human "a", ai "b", human "c", ai "d"] with a budget of 3 messages keeps system, human "c" and
ai "d". With a budget of 4, the window [ai "b", human "c", ai "d"] would start with an AI message, so
"b" is dropped too.

## What the library does inside
The sliding window of [[memory-window]] (the optional deep dive after this step), measured in the
units you choose and aware of message roles.

## Common mistakes
* Dropping the system message and losing the instructions.
* Cutting a tool result away from the AI message that requested it.
* Counting characters when the limit is in tokens; use the model's own counter in production.

## Why this matters
Every long-running assistant needs a memory policy; trimming is the simplest, and summarising old turns
is the next step.
''',
"statement": r'''
1. `trim_history(messages, max_messages)` returns `trim_messages(messages, max_tokens=max_messages,
   token_counter=len, strategy="last", include_system=True, start_on="human")`.
2. `count_words(messages)` returns the total number of whitespace-separated words in the messages'
   `content`.
3. `trim_by_words(messages, max_words)` trims the same way but with `count_words` as the counter.

Raise `ValueError` in the trimming functions for a budget below 1.
''',
"starter": r'''
from langchain_core.messages import trim_messages


def trim_history(messages, max_messages):
    # TODO
    pass


def count_words(messages):
    # TODO
    pass


def trim_by_words(messages, max_words):
    # TODO
    pass
''',
"hints": [
    "Both trimming functions call `trim_messages` with `strategy=\"last\"`, `include_system=True`, `start_on=\"human\"`.",
    "A token counter receives a list of messages: `sum(len(str(m.content).split()) for m in messages)`.",
    "Pass the function itself (`token_counter=count_words`), not its result.",
],
"solution": r'''
from langchain_core.messages import trim_messages


def _trim(messages, budget, counter):
    if budget < 1:
        raise ValueError("budget must be at least 1")
    return trim_messages(messages, max_tokens=budget, token_counter=counter,
                         strategy="last", include_system=True, start_on="human")


def trim_history(messages, max_messages):
    return _trim(messages, max_messages, len)


def count_words(messages):
    return sum(len(str(m.content).split()) for m in messages)


def trim_by_words(messages, max_words):
    return _trim(messages, max_words, count_words)
''',
"explanation": r'''
One helper holds the policy — keep the latest turns, the system message, and start on a human turn —
and the two public functions differ only in how size is measured: number of messages or number of
words.
''',
"tests": r'''
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


def chat():
    return [SystemMessage("be brief"), HumanMessage("a"), AIMessage("b"), HumanMessage("c"), AIMessage("d")]


class TestTrimming(unittest.TestCase):
    def test_budget_three(self):
        self.assertEqual([m.content for m in S.trim_history(chat(), 3)], ["be brief", "c", "d"])

    def test_starts_on_human(self):
        kept = S.trim_history(chat(), 4)
        self.assertEqual([m.content for m in kept], ["be brief", "c", "d"])
        self.assertEqual(kept[1].type, "human")

    def test_everything_fits(self):
        self.assertEqual(len(S.trim_history(chat(), 10)), 5)

    def test_count_words(self):
        self.assertEqual(S.count_words([HumanMessage("one two"), AIMessage("three")]), 3)
        self.assertEqual(S.count_words([]), 0)

    def test_trim_by_words(self):
        msgs = [SystemMessage("rules here"), HumanMessage("first long question here"), AIMessage("long answer"),
                HumanMessage("short"), AIMessage("ok")]
        kept = S.trim_by_words(msgs, 4)
        self.assertEqual([m.content for m in kept], ["rules here", "short", "ok"])
        self.assertLessEqual(S.count_words(kept), 4)

    def test_original_unchanged_and_invalid(self):
        msgs = chat()
        S.trim_history(msgs, 2)
        self.assertEqual(len(msgs), 5)
        with self.assertRaises(ValueError):
            S.trim_history(msgs, 0)
''',
"feedback": [
    ("test_budget_three", "Use strategy='last' and include_system=True."),
    ("test_starts_on_human", "start_on='human' drops a leading AI message from the kept window."),
    ("test_trim_by_words", "Pass count_words itself as token_counter."),
    ("test_original_unchanged_and_invalid", "Return a trimmed copy and reject budgets below 1."),
],
},
# ---------------------------------------------------------------- ag-validate-retry
{
"slug": "ag-validate-retry", "title": "Validating Tool Arguments and Retrying",
"difficulty": "advanced", "prereqs": ["task-dag-plan", "ag-message-memory", "lm-structured-output"],
"packages": ["langchain-core"],
"objectives": ["Give a tool a Pydantic argument schema with constraints",
               "Return validation errors to the model as tool messages",
               "Retry a fixed number of times and stop cleanly"],
"tags": ["langchain", "validation", "pydantic", "tool-calling", "retries"],
"sources": ["S134", "S140"], "entry": "class BookingArgs(BaseModel); book_room; call_with_validation(model, tool, messages, max_attempts=3)",
"article": r'''
# Validating Tool Arguments and Retrying

## Intuition
Models make plausible mistakes: a room "101" where the format is "R101", a meeting at 8 pm when the
building closes at 5. If the tool simply runs, it does damage; if it crashes, the agent stops. The
middle way: validate the arguments, tell the model exactly what was wrong, and let it try again.

## Precise explanation
```python
class BookingArgs(BaseModel):
    room: str = Field(pattern=r"^R\d{3}$", description="Room id such as R101")
    hour: int = Field(ge=9, le=17, description="Start hour, 9 to 17")

@tool(args_schema=BookingArgs)
def book_room(room: str, hour: int) -> str:
    """Book a meeting room for one hour."""
```

* `args_schema` makes the schema (including the descriptions) visible to the model and enforces it:
  `book_room.invoke(bad_args)` raises `pydantic.ValidationError`.
* `error.errors()` lists each problem with its field (`loc`) and message (`msg`); a compact summary such
  as `room: String should match pattern '^R\d{3}$'` is what the model needs.
* Loop: invoke the model → take its first tool call → validate and run. On failure append the AI message
  and a `ToolMessage(content="Invalid arguments: ...", tool_call_id=..., status="error")`, then ask again.
  Stop after `max_attempts` and report failure instead of looping.

## Worked example
Attempt 1: `{"room": "101", "hour": 20}` → "Invalid arguments: room: String should match pattern
'^R\d{3}$'; hour: Input should be less than or equal to 17". Attempt 2: `{"room": "R101", "hour": 16}`
→ "booked R101 at 16:00".

## What the library does inside
Pydantic validation replaces the hand-written checks in [[validate-and-retry]] (the optional deep dive
after this step); the retry loop is the same idea with real messages.

## Common mistakes
* Retrying without the error, so the model repeats the same mistake.
* Catching all exceptions, including bugs inside the tool, as if they were bad arguments.
* Unlimited retries.

## Why this matters
Validated tools are the first line of defence for agents that act in the world — booking, paying,
editing files.
''',
"statement": r'''
1. `class BookingArgs(BaseModel)` with `room: str = Field(pattern=r"^R\d{3}$")` and
   `hour: int = Field(ge=9, le=17)`.
2. `book_room` — a `@tool(args_schema=BookingArgs)` with docstring `"Book a meeting room for one hour."`
   returning `f"booked {room} at {hour}:00"`.
3. `call_with_validation(model, tool, messages, max_attempts=3)` repeats up to `max_attempts` times:
   `reply = model.invoke(messages)`; if the reply has no tool calls, return `(None, attempt)`; otherwise
   invoke `tool` with the first call's args. On success return `(result, attempt)`. On
   `ValidationError`, append the reply and a `ToolMessage` with
   `content="Invalid arguments: " + "; ".join(f"{err['loc'][0]}: {err['msg']}" for err in error.errors())`,
   `status="error"` and the call's id, and continue. After the last failed attempt return
   `(None, max_attempts)`. Attempts are counted from 1; the caller's `messages` list must not be modified.
''',
"starter": r'''
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field, ValidationError


class BookingArgs(BaseModel):
    # TODO
    pass


# TODO: book_room tool


def call_with_validation(model, tool, messages, max_attempts=3):
    # TODO
    pass
''',
"hints": [
    "Copy the conversation first: `history = list(messages)`.",
    "Inside the loop: `call = reply.tool_calls[0]`, then `tool.invoke(call[\"args\"])` in a try block.",
    "On ValidationError: `history += [reply, ToolMessage(content=..., tool_call_id=call[\"id\"], status=\"error\")]`.",
],
"solution": r'''
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field, ValidationError


class BookingArgs(BaseModel):
    room: str = Field(pattern=r"^R\d{3}$")
    hour: int = Field(ge=9, le=17)


@tool(args_schema=BookingArgs)
def book_room(room: str, hour: int) -> str:
    """Book a meeting room for one hour."""
    return f"booked {room} at {hour}:00"


def call_with_validation(model, tool, messages, max_attempts=3):
    history = list(messages)
    for attempt in range(1, max_attempts + 1):
        reply = model.invoke(history)
        if not reply.tool_calls:
            return None, attempt
        call = reply.tool_calls[0]
        try:
            return tool.invoke(call["args"]), attempt
        except ValidationError as error:
            summary = "; ".join(f"{err['loc'][0]}: {err['msg']}" for err in error.errors())
            history = history + [reply, ToolMessage(content="Invalid arguments: " + summary,
                                                    tool_call_id=call["id"], status="error")]
    return None, max_attempts
''',
"explanation": r'''
The Pydantic schema states the constraints once; the tool enforces them on every call. Each failure is
summarised field by field and sent back as an error tool message tied to the call, so the model can
correct itself; the attempt counter bounds the loop.
''',
"tests": r'''
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import ValidationError
''' + SCRIPTED + r'''

SEEN = []


class Recording(Scripted):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        SEEN.append(list(messages))
        return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)


class TestValidatedCalls(unittest.TestCase):
    def test_schema(self):
        self.assertEqual(S.book_room.invoke({"room": "R101", "hour": 10}), "booked R101 at 10:00")
        with self.assertRaises(ValidationError):
            S.book_room.invoke({"room": "101", "hour": 10})
        with self.assertRaises(ValidationError):
            S.book_room.invoke({"room": "R101", "hour": 20})

    def test_success_first_try(self):
        model = Scripted(messages=iter([call("book_room", {"room": "R202", "hour": 9})]))
        self.assertEqual(S.call_with_validation(model, S.book_room, [HumanMessage("book")]), ("booked R202 at 9:00", 1))

    def test_retry_with_feedback(self):
        SEEN.clear()
        model = Recording(messages=iter([call("book_room", {"room": "101", "hour": 20}, "c1"),
                                         call("book_room", {"room": "R101", "hour": 16}, "c2")]))
        result = S.call_with_validation(model, S.book_room, [HumanMessage("book R101 at 4pm")])
        self.assertEqual(result, ("booked R101 at 16:00", 2))
        feedback = SEEN[1][-1]
        self.assertEqual((feedback.type, feedback.status, feedback.tool_call_id), ("tool", "error", "c1"))
        self.assertIn("room:", feedback.content)
        self.assertIn("hour:", feedback.content)

    def test_gives_up(self):
        model = Scripted(messages=iter([call("book_room", {"room": "x", "hour": 1}, f"c{i}") for i in range(5)]))
        self.assertEqual(S.call_with_validation(model, S.book_room, [HumanMessage("book")], max_attempts=3), (None, 3))

    def test_no_tool_call(self):
        model = Scripted(messages=iter([AIMessage("I cannot book that.")]))
        self.assertEqual(S.call_with_validation(model, S.book_room, [HumanMessage("book")]), (None, 1))

    def test_caller_messages_unchanged(self):
        msgs = [HumanMessage("book")]
        model = Scripted(messages=iter([call("book_room", {"room": "1", "hour": 9}), call("book_room", {"room": "R100", "hour": 9})]))
        S.call_with_validation(model, S.book_room, msgs)
        self.assertEqual(len(msgs), 1)
''',
"feedback": [
    ("test_schema", "Use Field(pattern=r'^R\\d{3}$') for room and Field(ge=9, le=17) for hour, and @tool(args_schema=BookingArgs)."),
    ("test_retry_with_feedback", "Append the reply and an error ToolMessage listing each invalid field."),
    ("test_gives_up", "Stop after max_attempts and return (None, max_attempts)."),
    ("test_caller_messages_unchanged", "Work on a copy of messages."),
],
},
# ---------------------------------------------------------------- ag-orchestrator-graph
{
"slug": "ag-orchestrator-graph", "title": "Orchestrator and Workers in LangGraph",
"difficulty": "advanced", "prereqs": ["ag-validate-retry"], "packages": ["langgraph"],
"objectives": ["Fan out work to parallel workers with Send",
               "Collect worker results with a reducer and restore their order",
               "Combine results in a synthesiser node"],
"tags": ["langgraph", "orchestration", "map-reduce", "parallelism"],
"sources": ["S139", "S136"], "entry": "build_report_graph(worker_fn)",
"article": r'''
# Orchestrator and Workers in LangGraph

## Intuition
Some tasks split naturally: summarise each section of a report, check each file, answer each
sub-question. An **orchestrator** decides the pieces, **workers** handle one piece each (in parallel
when possible), and a **synthesiser** combines their results. How many workers are needed is known
only at run time.

## Precise explanation
```python
from langgraph.types import Send

def assign(state):                                   # a conditional edge that fans out
    return [Send("worker", {"index": i, "section": s}) for i, s in enumerate(state["sections"])]

graph.add_conditional_edges("orchestrator", assign, ["worker"])
graph.add_edge("worker", "synthesise")
```

* `Send(node, payload)` runs `node` with its own payload instead of the shared state; returning a list
  of `Send`s starts one worker per item.
* Workers write to a key with a reducer (`Annotated[list, operator.add]`), so their results are
  collected rather than overwritten. Parallel results arrive in no guaranteed order — include an index
  and sort in the synthesiser.
* The synthesiser runs once, after all workers of that step have finished.
* With zero items no worker runs, and nothing after them runs either; handle that case where it matters.

## Worked example
A document with sections "intro text", "methods text" and "results text" becomes three worker calls.
With a worker that returns the section's word count, the synthesiser writes
"1: 2 words | 2: 2 words | 3: 2 words".

## What the library does inside
The task splitting and merging of [[orchestrator-workers]] (the optional deep dive after this step),
with LangGraph scheduling the workers and merging their state updates.

## Common mistakes
* Workers returning plain values for a key without a reducer, so only one result survives.
* Assuming results arrive in order.
* Passing the whole state to each worker when it needs only its piece.

## Why this matters
Research assistants, code reviewers and report writers use this pattern to split large jobs across
many model calls.
''',
"statement": r'''
Write `build_report_graph(worker_fn)` returning a compiled graph over the state
`{"document": str, "sections": list, "results": Annotated[list, operator.add], "report": str}`:

* `"orchestrator"` splits the document on blank lines (`"\n\n"`), keeping non-empty, stripped sections;
* a conditional edge sends each section to `"worker"` with `Send("worker", {"index": i, "section": s})`;
* `"worker"` returns `{"results": [(index, worker_fn(section))]}`;
* `"synthesise"` sorts the results by index and sets `report` to
  `" | ".join(f"{i + 1}: {summary}" for i, summary in sorted_results)`.

Edges: START → orchestrator → (Send) worker → synthesise → END.
''',
"starter": r'''
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class ReportState(TypedDict):
    document: str
    sections: list
    results: Annotated[list, operator.add]
    report: str


def build_report_graph(worker_fn):
    # TODO
    pass
''',
"hints": [
    "`orchestrator` returns `{\"sections\": [s.strip() for s in state[\"document\"].split(\"\\n\\n\") if s.strip()]}`.",
    "The fan-out function returns a list of `Send(\"worker\", {...})`; register it with `add_conditional_edges(\"orchestrator\", assign, [\"worker\"])`.",
    "The worker receives the Send payload (with `index` and `section`), not the whole state.",
],
"solution": r'''
import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class ReportState(TypedDict):
    document: str
    sections: list
    results: Annotated[list, operator.add]
    report: str


def build_report_graph(worker_fn):
    def orchestrator(state):
        return {"sections": [s.strip() for s in state["document"].split("\n\n") if s.strip()]}

    def assign(state):
        return [Send("worker", {"index": i, "section": s}) for i, s in enumerate(state["sections"])]

    def worker(payload):
        return {"results": [(payload["index"], worker_fn(payload["section"]))]}

    def synthesise(state):
        ordered = sorted(state["results"])
        return {"report": " | ".join(f"{i + 1}: {summary}" for i, summary in ordered)}

    graph = StateGraph(ReportState)
    graph.add_node("orchestrator", orchestrator)
    graph.add_node("worker", worker)
    graph.add_node("synthesise", synthesise)
    graph.add_edge(START, "orchestrator")
    graph.add_conditional_edges("orchestrator", assign, ["worker"])
    graph.add_edge("worker", "synthesise")
    graph.add_edge("synthesise", END)
    return graph.compile()
''',
"explanation": r'''
The orchestrator decides the work; `Send` starts one worker per section with only that section; the
reducer collects the indexed results; the synthesiser restores the order and writes one report.
''',
"tests": r'''
def words(section):
    return f"{len(section.split())} words"


def state(document):
    return {"document": document, "sections": [], "results": [], "report": ""}


class TestOrchestrator(unittest.TestCase):
    def test_worked_example(self):
        app = S.build_report_graph(words)
        out = app.invoke(state("intro text\n\nmethods text\n\nresults text"))
        self.assertEqual(out["report"], "1: 2 words | 2: 2 words | 3: 2 words")

    def test_order_restored(self):
        app = S.build_report_graph(lambda s: s.upper())
        out = app.invoke(state("c\n\nb b\n\na a a"))
        self.assertEqual(out["report"], "1: C | 2: B B | 3: A A A")

    def test_one_worker_per_section(self):
        calls = []
        app = S.build_report_graph(lambda s: calls.append(s) or "ok")
        out = app.invoke(state("one\n\n\n\ntwo\n\n   \n\nthree"))
        self.assertEqual(sorted(calls), ["one", "three", "two"])
        self.assertEqual(out["sections"], ["one", "two", "three"])

    def test_results_collected(self):
        out = S.build_report_graph(len).invoke(state("ab\n\ncde"))
        self.assertEqual(sorted(out["results"]), [(0, 2), (1, 3)])

    def test_single_section(self):
        out = S.build_report_graph(words).invoke(state("just one section here"))
        self.assertEqual(out["report"], "1: 4 words")

    def test_nodes(self):
        nodes = set(S.build_report_graph(words).get_graph().nodes)
        self.assertTrue({"orchestrator", "worker", "synthesise"} <= nodes)
''',
"feedback": [
    ("test_worked_example", "Fan out with Send('worker', {'index': i, 'section': s}) and join results in synthesise."),
    ("test_order_restored", "Sort the collected (index, summary) pairs before joining."),
    ("test_one_worker_per_section", "Split on blank lines and drop empty sections."),
    ("test_results_collected", "Annotate results with operator.add so every worker's update is kept."),
],
},
# ---------------------------------------------------------------- ag-approval-guardrails
{
"slug": "ag-approval-guardrails", "title": "Guardrails with Human Approval",
"difficulty": "advanced", "prereqs": ["ag-orchestrator-graph"], "packages": ["langgraph"],
"objectives": ["Pause a graph with interrupt() to ask a person for approval",
               "Resume it with Command(resume=...) on the same thread",
               "Allow safe actions, require approval for sensitive ones and block unknown ones"],
"tags": ["langgraph", "guardrails", "human-in-the-loop", "interrupts", "safety"],
"sources": ["S138", "S137"], "entry": "build_guarded_graph(tools, sensitive); run_with_approval(app, action, thread_id, decide)",
"article": r'''
# Guardrails with Human Approval

## Intuition
An agent that can send emails or delete records should not do so on its own judgement. A guardrail
checks each proposed action: harmless ones run, unknown ones are refused, and sensitive ones **pause**
until a person approves. The pause must survive while the person thinks — so the graph's state is
saved, and the run resumes exactly where it stopped.

## Precise explanation
```python
from langgraph.types import Command, interrupt

def guard(state):
    action = state["action"]
    if action["tool"] not in tools:
        return {"outcome": "blocked"}
    if action["tool"] in sensitive:
        decision = interrupt({"action": action})        # pauses here
        if decision != "approve":
            return {"outcome": "rejected"}
    return {"outcome": "approved"}

app = graph.compile(checkpointer=InMemorySaver())       # interrupts need a checkpointer
first = app.invoke({"action": action}, config)          # stops: first["__interrupt__"][0].value
final = app.invoke(Command(resume="approve"), config)   # continues; interrupt() returns "approve"
```

* `interrupt(payload)` saves the state and ends the current `invoke`; the result contains
  `"__interrupt__"`, whose `.value` is the payload shown to the person.
* `Command(resume=value)` on the **same thread** restarts the interrupted node; this time `interrupt`
  returns `value`. Code before the `interrupt` call runs again, so keep side effects after it.
* The decision is data from outside the program: compare it with an exact value and treat anything else
  as a rejection.

## Worked example
Tools: `read_calendar` (safe), `send_email` (sensitive). `read_calendar` runs at once.
`send_email` pauses with the payload `{"action": {...}}`; with "approve" it runs and the outcome is
"approved: sent"; with "reject" nothing is sent. `delete_all` is blocked.

## What the library does inside
The permission checks of [[permission-guardrails]] (the optional deep dive after this step), with a
checkpointed pause in place of a blocking `input()` call.

## Common mistakes
* No checkpointer: `interrupt` cannot pause.
* Resuming with a different `thread_id`, which starts a new run.
* Performing the side effect before the interrupt, so it happens twice on resume.
* Treating any non-empty reply as approval.

## Why this matters
Human approval is required by many organisations for agents that act on real systems; the
club-event-assistant project idea after this step uses it before sending announcements.
''',
"statement": r'''
1. `build_guarded_graph(tools, sensitive)` (`tools` is a dict from name to a function taking `**args`;
   `sensitive` a set of names) returns a graph compiled with `InMemorySaver` over the state
   `{"action": dict, "outcome": str}` with nodes:
   * `"guard"`: unknown tool → `{"outcome": "blocked"}`; sensitive tool → `decision = interrupt({"action": action})`,
     and anything other than `"approve"` → `{"outcome": "rejected"}`; otherwise continue to execute;
   * `"execute"`: runs `tools[name](**args)` and sets `outcome` to `f"approved: {result}"`.
   Edges: START → guard; from guard to `"execute"` unless the outcome is already `"blocked"` or
   `"rejected"` (then END); execute → END.
2. `run_with_approval(app, action, thread_id, decide)` invokes the graph with
   `{"action": action, "outcome": ""}`; if the result contains `"__interrupt__"`, calls
   `decide(payload)` with the interrupt's value and resumes with `Command(resume=decision)`.
   Return the final `outcome`.
''',
"starter": r'''
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class GuardState(TypedDict):
    action: dict
    outcome: str


def build_guarded_graph(tools, sensitive):
    # TODO
    pass


def run_with_approval(app, action, thread_id, decide):
    # TODO
    pass
''',
"hints": [
    "The guard node returns `{}` when the action may run, so the router can send it to execute.",
    "`route = lambda s: END if s[\"outcome\"] in (\"blocked\", \"rejected\") else \"execute\"`.",
    "`result = app.invoke(...)`; `if \"__interrupt__\" in result: result = app.invoke(Command(resume=decide(result[\"__interrupt__\"][0].value)), config)`.",
],
"solution": r'''
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class GuardState(TypedDict):
    action: dict
    outcome: str


def build_guarded_graph(tools, sensitive):
    def guard(state):
        name = state["action"]["tool"]
        if name not in tools:
            return {"outcome": "blocked"}
        if name in sensitive:
            decision = interrupt({"action": state["action"]})
            if decision != "approve":
                return {"outcome": "rejected"}
        return {}

    def execute(state):
        action = state["action"]
        result = tools[action["tool"]](**action.get("args", {}))
        return {"outcome": f"approved: {result}"}

    def route(state):
        return END if state["outcome"] in ("blocked", "rejected") else "execute"

    graph = StateGraph(GuardState)
    graph.add_node("guard", guard)
    graph.add_node("execute", execute)
    graph.add_edge(START, "guard")
    graph.add_conditional_edges("guard", route)
    graph.add_edge("execute", END)
    return graph.compile(checkpointer=InMemorySaver())


def run_with_approval(app, action, thread_id, decide):
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"action": action, "outcome": ""}, config)
    if "__interrupt__" in result:
        decision = decide(result["__interrupt__"][0].value)
        result = app.invoke(Command(resume=decision), config)
    return result["outcome"]
''',
"explanation": r'''
The guard classifies every action. For sensitive ones `interrupt` saves the state and returns control
to the caller with the action to review; resuming on the same thread feeds the decision back into the
guard. Only an exact "approve" lets the action reach the execute node, where the side effect happens.
''',
"tests": r'''
SENT = []


def send_email(to, text):
    SENT.append((to, text))
    return "sent"


TOOLS = {"read_calendar": lambda day="today": f"3 events {day}", "send_email": send_email}


class TestApproval(unittest.TestCase):
    def setUp(self):
        SENT.clear()
        self.app = S.build_guarded_graph(TOOLS, {"send_email"})

    def test_safe_action_runs_without_asking(self):
        asked = []
        outcome = S.run_with_approval(self.app, {"tool": "read_calendar", "args": {"day": "monday"}}, "t1",
                                      lambda payload: asked.append(payload) or "approve")
        self.assertEqual((outcome, asked), ("approved: 3 events monday", []))

    def test_sensitive_action_approved(self):
        seen = []
        action = {"tool": "send_email", "args": {"to": "club@example.org", "text": "Meeting at 5"}}
        outcome = S.run_with_approval(self.app, action, "t2", lambda payload: seen.append(payload) or "approve")
        self.assertEqual(outcome, "approved: sent")
        self.assertEqual(seen, [{"action": action}])
        self.assertEqual(SENT, [("club@example.org", "Meeting at 5")])

    def test_sensitive_action_rejected(self):
        action = {"tool": "send_email", "args": {"to": "all@example.org", "text": "Spam"}}
        self.assertEqual(S.run_with_approval(self.app, action, "t3", lambda payload: "reject"), "rejected")
        self.assertEqual(SENT, [])

    def test_only_exact_approve(self):
        action = {"tool": "send_email", "args": {"to": "a@example.org", "text": "x"}}
        self.assertEqual(S.run_with_approval(self.app, action, "t4", lambda payload: "yes please"), "rejected")

    def test_unknown_tool_blocked(self):
        self.assertEqual(S.run_with_approval(self.app, {"tool": "delete_all", "args": {}}, "t5", lambda p: "approve"), "blocked")

    def test_sent_once_after_resume(self):
        action = {"tool": "send_email", "args": {"to": "b@example.org", "text": "once"}}
        S.run_with_approval(self.app, action, "t6", lambda payload: "approve")
        self.assertEqual(len(SENT), 1)
''',
"feedback": [
    ("test_safe_action_runs_without_asking", "Only sensitive tools call interrupt()."),
    ("test_sensitive_action_approved", "Resume with Command(resume=decision) on the same thread_id."),
    ("test_only_exact_approve", "Treat anything except 'approve' as a rejection."),
    ("test_sent_once_after_resume", "Run the tool in the execute node, after the approval, not inside guard."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "study-planner-agent", "title": "Study-Planner Agent",
"tags": ["agents", "langgraph", "tools"],
"brief": r'''
Build an assistant that plans your study week: it reads your deadlines and free time from files, uses
tools to look them up and update a plan, and answers questions such as "what should I do tonight?" —
without ever running more than a fixed number of steps.
''',
"uses": ["ag-langchain-tools", "ag-langgraph-basics", "ag-langgraph-react", "task-dag-plan"],
"milestones": [
    "Store deadlines and free time slots in JSON files and write tools to read and update them.",
    "Build the ReAct graph with those tools and a scripted model; test it with a few fixed conversations.",
    "Connect a real chat model and write a system prompt that explains the tools and your preferences.",
    "Add a step limit and a checkpointer so each day's conversation continues where it stopped.",
    "Add a tool that schedules tasks in dependency order (prerequisites first) and test it on a sample week.",
],
"stretch": [
    "Export the plan to an .ics calendar file.",
    "Add a reflection node that checks the plan against deadlines before answering.",
    "Measure how often the agent uses the right tool on 20 test requests.",
],
"data": r'''
Write your own deadline and timetable files. No dataset is needed; for a local model install
[Ollama](https://ollama.com/).
''',
"setup": r'''
```bash
pip install langgraph langchain-core langchain-ollama
python planner.py
```
''',
},
{
"kind": "project", "slug": "club-event-assistant", "title": "Club Event Assistant",
"tags": ["agents", "guardrails", "human-in-the-loop"],
"brief": r'''
Build an assistant for a student club that answers questions about upcoming events, drafts
announcements and registration reminders — and never sends anything without a committee member's
approval.
''',
"uses": ["lm-langchain-rag", "ag-langgraph-react", "ag-validate-retry", "ag-approval-guardrails"],
"milestones": [
    "Put event details in a small JSON or CSV file and answer FAQ-style questions about them with retrieval.",
    "Add a draft_announcement tool that returns text but sends nothing.",
    "Add a send_message tool behind an approval interrupt; show the draft and ask approve or reject.",
    "Validate tool arguments (dates in the future, known channels, length limits) and retry on errors.",
    "Log every proposed and approved action with a timestamp for review.",
],
"stretch": [
    "Support edits: the reviewer can change the draft before approving.",
    "Connect a real channel (email or a chat webhook) only after everything else is tested.",
    "Write evaluation cases for refusals: requests the assistant must not act on.",
],
"data": r'''
Use a sample events file you create (titles, dates, venues, registration links). Keep real contact lists
out of the project until the approval flow is reliable.
''',
"setup": r'''
```bash
pip install langgraph langchain-core
python assistant.py
```
''',
},
{
"kind": "project", "slug": "agent-evaluation-suite", "title": "Agent Evaluation Suite",
"tags": ["evaluation", "testing", "agents"],
"brief": r'''
Build a reusable test suite for an agent: scripted scenarios with expected tool calls and answers,
metrics such as task success, tool accuracy and step count, and a report that shows what changed
between two versions of the agent.
''',
"uses": ["agent-evaluation", "ag-langgraph-react", "ag-approval-guardrails", "nlp-error-analysis"],
"milestones": [
    "Write 20 test cases: input, expected final answer (or a checker function) and expected tools.",
    "Run an agent on every case and record the messages, tool calls, steps and time.",
    "Compute task success, tool precision and recall, and average steps per task.",
    "Add safety cases that must end in refusal or approval, and count violations.",
    "Compare two agent versions in one table and highlight regressions.",
],
"stretch": [
    "Use a second model as a grader for open-ended answers, and check its agreement with your own grades.",
    "Run each case several times to measure variability.",
    "Run the suite automatically on every change with a CI workflow.",
],
"data": r'''
Write the test cases yourself, for the study-planner or club-assistant agent. Scripted fake models make
the first version of the suite fully deterministic.
''',
"setup": r'''
```bash
pip install langgraph langchain-core pandas
python evaluate.py --agent planner
```
''',
},
]
