# Agentic AI

**You will be able to:** Build agent loops, parsing, budgets, ReAct, planners and evaluation by hand, then LangChain tools and LangGraph graphs with tool nodes, checkpointed memory, validated retries, orchestrator–workers and human-approval guardrails.

**Topic prerequisites:** Large Language Models

Agents are programs that repeatedly decide on an action, act through tools and observe the
result. You first build each part with ordinary Python and a **scripted model** — tool registries,
parsing model output, perceive–act loops, goals and budgets, the ReAct loop, BFS and A* planners,
dependency-ordered plans and an evaluation harness. Then you use the libraries: LangChain tools and
tool calling, LangGraph state graphs, a ReAct agent with a tool node and checkpointed threads,
message trimming, validated tool arguments with retries, orchestrator–workers with `Send`, and
human approval with interrupts.

**Packages:** standard library, `langchain-core` and `langgraph`. Fake chat models keep every test
deterministic; no paid API or network is used. The hand-written memory window, validate-and-retry,
orchestrator and guardrail steps are **optional deep dives**. **Project ideas:** a study-planner
agent, a club event assistant and an agent evaluation suite.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | AG-01 | [Tool Registry and Dispatch](tool-registry/problem.md) | beginner | PY-17 |
| 2 | AG-02 | [Parsing Model Tool Calls](parse-tool-call/problem.md) | beginner | AG-01, NL-01 |
| 3 | AG-03 | [Tools and Tool Calling with LangChain](ag-langchain-tools/problem.md) | beginner | AG-02, LM-17 |
| 4 | AG-04 | [Perceive-Act Loop](reflex-agent-loop/problem.md) | beginner | AG-01 |
| 5 | AG-05 | [Goal Tests and Step Budgets](goal-and-budget/problem.md) | beginner | AG-04 |
| 6 | AG-06 | [ReAct Loop with a Scripted Model](react-loop/problem.md) | intermediate | AG-02, AG-05 |
| 7 | AG-07 | [LangGraph Basics: State, Nodes and Edges](ag-langgraph-basics/problem.md) | intermediate | AG-06, AG-03 |
| 8 | AG-08 | [A ReAct Agent in LangGraph](ag-langgraph-react/problem.md) | intermediate | AG-07 |
| 9 | AG-09 | [Conversation Memory with trim_messages](ag-message-memory/problem.md) | intermediate | AG-08 |
| 10 | AG-10 | [Conversation Memory Window by Hand (optional deep dive)](memory-window/problem.md) | intermediate | AG-06 |
| 11 | AG-11 | [BFS Planner](bfs-planner/problem.md) | intermediate | AG-05 |
| 12 | AG-12 | [A* Planner](a-star-planner/problem.md) | intermediate | AG-11 |
| 13 | AG-13 | [Dependency-Ordered Plans](task-dag-plan/problem.md) | advanced | AG-11 |
| 14 | AG-P1 | [Project idea: Study-Planner Agent](study-planner-agent/project.md) | ungraded | AG-03, AG-07, AG-08, AG-13 |
| 15 | AG-14 | [Validating Tool Arguments and Retrying](ag-validate-retry/problem.md) | advanced | AG-13, AG-09, LM-19 |
| 16 | AG-15 | [Validate-and-Retry Tool Calls (optional deep dive)](validate-and-retry/problem.md) | advanced | AG-02, AG-06 |
| 17 | AG-16 | [Orchestrator and Workers in LangGraph](ag-orchestrator-graph/problem.md) | advanced | AG-14 |
| 18 | AG-17 | [Orchestrator-Workers Pipeline by Hand (optional deep dive)](orchestrator-workers/problem.md) | advanced | AG-13, AG-15 |
| 19 | AG-18 | [Guardrails with Human Approval](ag-approval-guardrails/problem.md) | advanced | AG-16 |
| 20 | AG-19 | [Permission Guardrails (optional deep dive)](permission-guardrails/problem.md) | advanced | AG-01, AG-06 |
| 21 | AG-P2 | [Project idea: Club Event Assistant](club-event-assistant/project.md) | ungraded | LM-20, AG-08, AG-14, AG-18 |
| 22 | AG-20 | [Evaluating Agents](agent-evaluation/problem.md) | advanced | AG-06, AG-18 |
| 23 | AG-P3 | [Project idea: Agent Evaluation Suite](agent-evaluation-suite/project.md) | ungraded | AG-20, AG-08, AG-18, NL-16 |
