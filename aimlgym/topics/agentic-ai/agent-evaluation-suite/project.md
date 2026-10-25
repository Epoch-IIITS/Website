# AG-P3 · Project idea: Agent Evaluation Suite

**Topic:** Agentic AI · ungraded

## Brief

Build a reusable test suite for an agent: scripted scenarios with expected tool calls and answers,
metrics such as task success, tool accuracy and step count, and a report that shows what changed
between two versions of the agent.

## You will use

- AG-20 Evaluating Agents
- AG-08 A ReAct Agent in LangGraph
- AG-18 Guardrails with Human Approval
- NL-16 Evaluating Text Classifiers

## Milestones

1. Write 20 test cases: input, expected final answer (or a checker function) and expected tools.
2. Run an agent on every case and record the messages, tool calls, steps and time.
3. Compute task success, tool precision and recall, and average steps per task.
4. Add safety cases that must end in refusal or approval, and count violations.
5. Compare two agent versions in one table and highlight regressions.

## Stretch goals

- Use a second model as a grader for open-ended answers, and check its agreement with your own grades.
- Run each case several times to measure variability.
- Run the suite automatically on every change with a CI workflow.

## Data

Write the test cases yourself, for the study-planner or club-assistant agent. Scripted fake models make
the first version of the suite fully deterministic.

## Run it yourself

```bash
pip install langgraph langchain-core pandas
python evaluate.py --agent planner
```
