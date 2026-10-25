"""Agentic AI step added in the 2026-10 revision: a deterministic evaluation harness."""

PROBLEMS = [
# ---------------------------------------------------------------- agent-evaluation
{
"slug": "agent-evaluation", "title": "Evaluating Agents",
"difficulty": "advanced", "prereqs": ["react-loop", "ag-approval-guardrails"], "packages": [],
"objectives": ["Define pass/fail criteria for an agent task: answer, budget and forbidden actions",
               "Normalise answers before comparing them",
               "Run a suite of tasks, isolating crashes so one failure does not stop the run",
               "Compare two agent versions and list regressions"],
"tags": ["evaluation", "agents", "regression-testing", "metrics", "safety"],
"sources": ["S037", "S102", "S002"], "entry": "normalize_answer(text); evaluate(agent, tasks); regressions(old_report, new_report)",
"article": r'''
# Evaluating Agents

## Intuition
An agent that worked once may fail tomorrow after a prompt change, a new tool or a different
model. An **evaluation harness** runs the agent on a fixed set of tasks with known expected
outcomes and reports what passed, what failed and why — the agent equivalent of unit tests
([[unit-testing]]).

## Precise explanation
An evaluation task here is a dict:
```python
{"id": "add-1", "input": "What is 2 + 3?", "expected": "5",
 "max_tool_calls": 2, "forbidden_tools": ["delete_file"]}
```
The agent is any function `agent(input)` returning
`{"status": "final" | ..., "answer": str | None, "tool_calls": int, "tools_used": [names]}`
(the shape of [[react-loop]]'s result plus a list of tools it used).

A task **passes** only if every check holds; each failed check adds a **reason**:
* `"not final"` — the agent did not finish (`status != "final"`);
* `"wrong answer"` — normalised answer differs from the normalised expected answer;
* `"over budget"` — more tool calls than `max_tool_calls` (when given);
* `"forbidden tool: <name>"` — for each forbidden tool it used (sorted by name);
* `"error: <ExceptionType>"` — the agent raised; this replaces all other reasons.

**Normalisation** prevents false failures: lowercase, strip, collapse whitespace, and remove
trailing `.`/`!` so `"Paris."` equals `"paris"`. Keep it minimal — over-normalising hides real
mistakes.

**Regressions**: tasks that passed with the old version and fail with the new one. Track the pass
rate *and* the list of regressions; a stable pass rate can hide one fixed task and one broken task.

## Worked example
Three tasks; the agent answers the first correctly with one tool call, answers the second
correctly but uses a forbidden tool, and crashes on the third: pass rate 1/3, reasons
`[]`, `["forbidden tool: rm"]`, `["error: KeyError"]`.

## Common mistakes
* Letting one exception abort the whole evaluation.
* Comparing raw strings, so trailing punctuation fails a correct answer.
* Measuring only final answers and ignoring unsafe or wasteful behaviour.
* Using a live model in tests, making results non-deterministic; use scripted agents for the
  harness itself.

## Why this matters
Evaluation is how teams decide whether an agent change is an improvement and whether it is safe
to deploy; guardrail checks ([[permission-guardrails]]) become evaluation criteria.
''',
"statement": r'''
Implement:

1. `normalize_answer(text)` — `None` → `""`; otherwise lowercase, strip, collapse internal
   whitespace to single spaces, then remove trailing `.` and `!` characters (and strip again).
2. `evaluate(agent, tasks)` → `{"results": [...], "pass_rate": float, "mean_tool_calls": float}`.
   Each result is `{"id": ..., "passed": bool, "reasons": [...]}` in task order, using the rules
   above. Call `agent(task["input"])` exactly once per task; catch any `Exception`.
   `mean_tool_calls` averages over tasks that did not error (0.0 if none). An empty task list
   gives pass rate 0.0.
3. `regressions(old_report, new_report)` → sorted list of task ids that passed in `old_report` and
   failed (or are missing) in `new_report`.
''',
"starter": r'''
def normalize_answer(text):
    # TODO
    return text


def evaluate(agent, tasks):
    results = []
    for task in tasks:
        out = agent(task["input"])
        results.append({"id": task["id"], "passed": out["answer"] == task["expected"], "reasons": []})
    # TODO: all checks, error handling, summary numbers
    return {"results": results, "pass_rate": 0.0, "mean_tool_calls": 0.0}


def regressions(old_report, new_report):
    # TODO
    return []
''',
"hints": [
    "`\" \".join(text.lower().split()).rstrip(\".!\").strip()` normalises.",
    "Wrap only the agent call in `try/except Exception as e:` and record `f\"error: {type(e).__name__}\"`.",
    "For regressions build `{r[\"id\"]: r[\"passed\"] for r in report[\"results\"]}` for both reports.",
],
"solution": r'''
def normalize_answer(text):
    if text is None:
        return ""
    return " ".join(text.lower().split()).rstrip(".!").strip()


def evaluate(agent, tasks):
    results, tool_counts = [], []
    for task in tasks:
        try:
            out = agent(task["input"])
        except Exception as e:
            results.append({"id": task["id"], "passed": False, "reasons": [f"error: {type(e).__name__}"]})
            continue
        reasons = []
        if out.get("status") != "final":
            reasons.append("not final")
        if normalize_answer(out.get("answer")) != normalize_answer(task["expected"]):
            reasons.append("wrong answer")
        calls = out.get("tool_calls", 0)
        tool_counts.append(calls)
        if "max_tool_calls" in task and calls > task["max_tool_calls"]:
            reasons.append("over budget")
        used = set(out.get("tools_used", []))
        for name in sorted(used & set(task.get("forbidden_tools", []))):
            reasons.append(f"forbidden tool: {name}")
        results.append({"id": task["id"], "passed": not reasons, "reasons": reasons})
    passed = sum(r["passed"] for r in results)
    return {
        "results": results,
        "pass_rate": passed / len(results) if results else 0.0,
        "mean_tool_calls": sum(tool_counts) / len(tool_counts) if tool_counts else 0.0,
    }


def regressions(old_report, new_report):
    old = {r["id"]: r["passed"] for r in old_report["results"]}
    new = {r["id"]: r["passed"] for r in new_report["results"]}
    return sorted(i for i, ok in old.items() if ok and not new.get(i, False))
''',
"explanation": r'''
Each task is isolated in its own `try`, so a crash becomes an `error:` result instead of stopping
the run. Every check appends a human-readable reason, which makes failures actionable, and a task
passes only when the list is empty. Comparing two reports by task id exposes regressions that an
unchanged pass rate would hide.
''',
"tests": r'''
TASKS = [
    {"id": "add", "input": "2+3", "expected": "5", "max_tool_calls": 1},
    {"id": "capital", "input": "capital of France", "expected": "Paris", "forbidden_tools": ["rm", "web"]},
    {"id": "crash", "input": "boom", "expected": "x"},
    {"id": "slow", "input": "think", "expected": "done", "max_tool_calls": 2},
]


def agent_v1(question):
    if question == "2+3":
        return {"status": "final", "answer": " 5. ", "tool_calls": 1, "tools_used": ["calculator"]}
    if question == "capital of France":
        return {"status": "final", "answer": "PARIS!", "tool_calls": 2, "tools_used": ["web", "rm", "search"]}
    if question == "boom":
        raise KeyError("missing")
    return {"status": "step_limit", "answer": None, "tool_calls": 5, "tools_used": []}


def agent_v2(question):
    if question == "2+3":
        return {"status": "final", "answer": "6", "tool_calls": 1, "tools_used": []}
    if question == "capital of France":
        return {"status": "final", "answer": "Paris", "tool_calls": 1, "tools_used": ["search"]}
    if question == "boom":
        return {"status": "final", "answer": "x", "tool_calls": 0, "tools_used": []}
    return {"status": "final", "answer": "Done", "tool_calls": 2, "tools_used": []}


class TestAgentEvaluation(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(S.normalize_answer("  The   Answer is 5.!  "), "the answer is 5")
        self.assertEqual(S.normalize_answer(None), "")
        self.assertEqual(S.normalize_answer("3.5"), "3.5")

    def test_reasons(self):
        report = S.evaluate(agent_v1, TASKS)
        reasons = {r["id"]: r["reasons"] for r in report["results"]}
        self.assertEqual(reasons["add"], [])
        self.assertEqual(reasons["capital"], ["forbidden tool: rm", "forbidden tool: web"])
        self.assertEqual(reasons["crash"], ["error: KeyError"])
        self.assertEqual(reasons["slow"], ["not final", "wrong answer", "over budget"])

    def test_summary(self):
        report = S.evaluate(agent_v1, TASKS)
        self.assertEqual([r["id"] for r in report["results"]], ["add", "capital", "crash", "slow"])
        self.assertEqual(report["pass_rate"], 0.25)
        self.assertAlmostEqual(report["mean_tool_calls"], (1 + 2 + 5) / 3)

    def test_calls_agent_once_per_task(self):
        calls = []
        def agent(q):
            calls.append(q)
            return agent_v2(q)
        S.evaluate(agent, TASKS)
        self.assertEqual(calls, [t["input"] for t in TASKS])

    def test_empty(self):
        self.assertEqual(S.evaluate(agent_v1, []), {"results": [], "pass_rate": 0.0, "mean_tool_calls": 0.0})

    def test_regressions(self):
        old, new = S.evaluate(agent_v1, TASKS), S.evaluate(agent_v2, TASKS)
        self.assertEqual(new["pass_rate"], 0.75)
        self.assertEqual(S.regressions(old, new), ["add"])
        self.assertEqual(S.regressions(new, old), ["capital", "crash", "slow"])
        self.assertEqual(S.regressions(new, {"results": []}), ["capital", "crash", "slow"])
''',
"feedback": [
    ("test_normalize", "Lowercase, collapse whitespace, then strip trailing '.' and '!'."),
    ("test_reasons", "Check status, answer, budget and forbidden tools in that order; an exception gives only an error reason."),
    ("test_summary", "Average tool calls only over tasks that returned a result."),
    ("test_calls_agent_once_per_task", "Call the agent exactly once per task, in order."),
    ("test_regressions", "A regression passed before and fails (or is missing) now; return ids sorted."),
],
},
]
