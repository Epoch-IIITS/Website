# AG-13 · Dependency-Ordered Plans

**Topic:** Agentic AI · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** AG-11 BFS Planner

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `topo_order(deps)` → list of tasks (Kahn's algorithm, smallest ready task first using `heapq`). Raise
  `ValueError("cycle detected")` on cycles and `ValueError` if a dependency is not a key.
* `stages(deps)` → list of sorted lists of tasks that can run in parallel.

**Example**
```python
deps = {"data": set(), "outline": set(), "charts": {"data"}, "report": {"data", "charts", "outline"}}
topo_order(deps)   # ['data', 'charts', 'outline', 'report']
stages(deps)       # [['data', 'outline'], ['charts'], ['report']]
```

## Hints

<details><summary>Hint 1</summary>

Build `dependents[d].append(t)` for each t and each d in deps[t]; `indeg[t] = len(deps[t])`.

</details>

<details><summary>Hint 2</summary>

`ready = [t for t in deps if indeg[t] == 0]; heapq.heapify(ready)`.

</details>

<details><summary>Hint 3</summary>

Stages: loop taking `sorted(t for t in remaining if all deps done)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_order` | Use a min-heap of ready tasks so the smallest ready task goes first. |
| `test_cycle` | If not all tasks were output, raise ValueError('cycle detected'). |
| `test_stages` | A stage is every task whose dependencies are all in earlier stages. |
| `test_unknown_dep` | Every dependency must be a key of deps. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Kahn's algorithm releases a task once all its dependencies are output; a min-heap picks the
alphabetically smallest ready task for a deterministic order, and leftover tasks reveal a cycle. Stages
peel off every currently-ready task at once, giving the maximum parallelism level by level.

## References

- [Artificial Intelligence: A Modern Approach (4th ed.)](https://aima.cs.berkeley.edu/) — Stuart Russell, Peter Norvig (`S038`)
- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
