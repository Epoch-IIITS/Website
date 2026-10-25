r"""Reference solution for AG-12 A* Planner.

Entries carry their g so stale ones (superseded by a cheaper path) are skipped on pop. Neighbours are
relaxed when a strictly cheaper path is found. Stopping only when the goal is popped guarantees
optimality with an admissible, consistent heuristic; the counter makes ordering deterministic without
comparing states.
"""
import heapq
import itertools


def astar(start, goal, neighbors, heuristic):
    counter = itertools.count()
    h0 = float(heuristic(start))
    heap = [(h0, h0, next(counter), start, 0.0)]
    best_g = {start: 0.0}
    parent = {start: None}
    expanded = 0
    while heap:
        f, h, _, s, g = heapq.heappop(heap)
        if g > best_g.get(s, float("inf")):
            continue
        expanded += 1
        if s == goal:
            path = [s]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            return {"path": path[::-1], "cost": float(g), "expanded": expanded}
        for nxt, cost in neighbors(s):
            ng = g + cost
            if ng < best_g.get(nxt, float("inf")):
                best_g[nxt] = ng
                parent[nxt] = s
                nh = float(heuristic(nxt))
                heapq.heappush(heap, (ng + nh, nh, next(counter), nxt, ng))
    return None
