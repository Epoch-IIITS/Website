r"""Reference solution for AG-20 Evaluating Agents.

Each task is isolated in its own `try`, so a crash becomes an `error:` result instead of stopping
the run. Every check appends a human-readable reason, which makes failures actionable, and a task
passes only when the list is empty. Comparing two reports by task id exposes regressions that an
unchanged pass rate would hide.
"""
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
