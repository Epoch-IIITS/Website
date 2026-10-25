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
