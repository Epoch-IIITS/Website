r"""Reference solution for AG-13 Dependency-Ordered Plans.

Kahn's algorithm releases a task once all its dependencies are output; a min-heap picks the
alphabetically smallest ready task for a deterministic order, and leftover tasks reveal a cycle. Stages
peel off every currently-ready task at once, giving the maximum parallelism level by level.
"""
import heapq


def _check(deps):
    for t, ds in deps.items():
        for d in ds:
            if d not in deps:
                raise ValueError(f"unknown dependency {d!r} of {t!r}")


def topo_order(deps):
    _check(deps)
    indeg = {t: len(ds) for t, ds in deps.items()}
    dependents = {t: [] for t in deps}
    for t, ds in deps.items():
        for d in ds:
            dependents[d].append(t)
    ready = [t for t, k in indeg.items() if k == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        t = heapq.heappop(ready)
        order.append(t)
        for u in dependents[t]:
            indeg[u] -= 1
            if indeg[u] == 0:
                heapq.heappush(ready, u)
    if len(order) != len(deps):
        raise ValueError("cycle detected")
    return order


def stages(deps):
    topo_order(deps)  # validates and detects cycles
    done, out = set(), []
    remaining = set(deps)
    while remaining:
        stage = sorted(t for t in remaining if set(deps[t]) <= done)
        out.append(stage)
        done |= set(stage)
        remaining -= set(stage)
    return out
