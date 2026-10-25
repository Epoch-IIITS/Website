r"""Reference solution for AG-08 A ReAct Agent in LangGraph.

The agent node asks the model for its next move; `tools_condition` sends tool calls to the ToolNode
and plain answers to the end, and the tool results flow back to the model. The checkpointer stores
each thread's messages, and the recursion limit turns a runaway loop into a clear message.
"""
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
