# AG-12 · A* Planner

**Topic:** Agentic AI · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** AG-11 BFS Planner

Read the lesson first: [article.md](article.md)

## Task

Write `astar(start, goal, neighbors, heuristic)` returning `{"path": list, "cost": float, "expanded": int}`
or `None`. `neighbors(s)` yields `(next_state, step_cost)` with non-negative costs; `heuristic(s)` is a
float. `expanded` counts states popped and processed (not stale entries). Heap entries:
`(f, h, counter, state)`.

**Example**
```python
r = astar((0, 0), (4, 4), grid_neighbors, lambda s: abs(s[0] - 4) + abs(s[1] - 4))
r["cost"], len(r["path"])     # (8.0, 9)
```

## Hints

<details><summary>Hint 1</summary>

`best_g = {start: 0}`, `parent = {start: None}`, `heap = [(h0, h0, next(counter), start)]`.

</details>

<details><summary>Hint 2</summary>

On pop: if `g_of_entry > best_g[state]` skip (compute g = f − h).

</details>

<details><summary>Hint 3</summary>

Rebuild the path from parents when the goal is popped.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_weighted_costs` | Stop when the goal is popped, not when it is generated. |
| `test_fewer_expansions_than_ucs` | Order the heap by f = g + h. |
| `test_walls` | Relax a neighbour only when the new g is strictly smaller; skip stale heap entries. |
| `test_start_is_goal` | Popping the start counts as one expansion. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Entries carry their g so stale ones (superseded by a cheaper path) are skipped on pop. Neighbours are
relaxed when a strictly cheaper path is found. Stopping only when the goal is popped guarantees
optimality with an admissible, consistent heuristic; the counter makes ordering deterministic without
comparing states.

## References

- [Artificial Intelligence: A Modern Approach (4th ed.)](https://aima.cs.berkeley.edu/) — Stuart Russell, Peter Norvig (`S038`)
