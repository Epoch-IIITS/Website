# AG-P1 · Project idea: Study-Planner Agent

**Topic:** Agentic AI · ungraded

## Brief

Build an assistant that plans your study week: it reads your deadlines and free time from files, uses
tools to look them up and update a plan, and answers questions such as "what should I do tonight?" —
without ever running more than a fixed number of steps.

## You will use

- AG-03 Tools and Tool Calling with LangChain
- AG-07 LangGraph Basics: State, Nodes and Edges
- AG-08 A ReAct Agent in LangGraph
- AG-13 Dependency-Ordered Plans

## Milestones

1. Store deadlines and free time slots in JSON files and write tools to read and update them.
2. Build the ReAct graph with those tools and a scripted model; test it with a few fixed conversations.
3. Connect a real chat model and write a system prompt that explains the tools and your preferences.
4. Add a step limit and a checkpointer so each day's conversation continues where it stopped.
5. Add a tool that schedules tasks in dependency order (prerequisites first) and test it on a sample week.

## Stretch goals

- Export the plan to an .ics calendar file.
- Add a reflection node that checks the plan against deadlines before answering.
- Measure how often the agent uses the right tool on 20 test requests.

## Data

Write your own deadline and timetable files. No dataset is needed; for a local model install
[Ollama](https://ollama.com/).

## Run it yourself

```bash
pip install langgraph langchain-core langchain-ollama
python planner.py
```
