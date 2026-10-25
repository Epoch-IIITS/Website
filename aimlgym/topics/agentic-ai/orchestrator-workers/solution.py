r"""Reference solution for AG-17 Orchestrator-Workers Pipeline by Hand.

Each round plans, orders subtasks by dependencies, routes each to its worker with its dependencies'
outputs, and asks the evaluator to accept or give feedback. Worker failures are logged and end the
round without evaluation; the round cap prevents endless revision loops.
"""
import heapq


def _order(subtasks):
    deps = {s["id"]: set(s.get("deps", [])) for s in subtasks}
    for i, ds in deps.items():
        if not ds <= set(deps):
            raise ValueError(f"unknown dependency in {i!r}")
    indeg = {i: len(ds) for i, ds in deps.items()}
    dependents = {i: [] for i in deps}
    for i, ds in deps.items():
        for d in ds:
            dependents[d].append(i)
    ready = [i for i, k in indeg.items() if k == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        i = heapq.heappop(ready)
        order.append(i)
        for u in dependents[i]:
            indeg[u] -= 1
            if indeg[u] == 0:
                heapq.heappush(ready, u)
    if len(order) != len(deps):
        raise ValueError("cycle detected in plan")
    return order


def orchestrate(task, planner, workers, evaluator, max_rounds=2):
    feedback, log, outputs = None, [], {}
    for r in range(1, max_rounds + 1):
        subtasks = planner(task, feedback)
        by_id = {s["id"]: s for s in subtasks}
        order = _order(subtasks)
        log.append(f"round {r}: plan {order}")
        outputs, failed = {}, False
        for i in order:
            s = by_id[i]
            worker = workers.get(s["type"])
            if worker is None:
                log.append(f"round {r}: error {i}: unknown worker '{s['type']}'")
                failed = True
                break
            try:
                outputs[i] = worker(s["input"], {d: outputs[d] for d in s.get("deps", [])})
                log.append(f"round {r}: {i} -> {s['type']}")
            except Exception as e:
                log.append(f"round {r}: error {i}: {type(e).__name__}: {e}")
                failed = True
                break
        if failed:
            feedback = "a worker failed"
            continue
        accepted, feedback = evaluator(task, outputs)
        if accepted:
            log.append(f"round {r}: evaluator accepted")
            return {"accepted": True, "outputs": outputs, "rounds": r, "log": log}
        log.append(f"round {r}: evaluator rejected: {feedback}")
    return {"accepted": False, "outputs": outputs, "rounds": max_rounds, "log": log}
