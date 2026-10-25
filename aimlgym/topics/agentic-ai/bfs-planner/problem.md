# AG-11 · BFS Planner

**Topic:** Agentic AI · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** AG-05 Goal Tests and Step Budgets

Read the lesson first: [article.md](article.md)

## Task

Write `bfs_plan(start, goal_test, successors)` returning `{"actions": list, "states": list,
"expanded": int}` for a shortest plan (states include start and goal; `expanded` = number of states
dequeued), or `None` if no plan exists. States are hashable.

**Example**
```python
G = {"hall": [("go kitchen", "kitchen"), ("go study", "study")], "kitchen": [("go garden", "garden")],
     "study": [("go garden", "garden")], "garden": []}
bfs_plan("hall", lambda s: s == "garden", lambda s: G[s])["actions"]   # ['go kitchen', 'go garden']
```

## Hints

<details><summary>Hint 1</summary>

`queue = deque([start]); parent = {start: None}`.

</details>

<details><summary>Hint 2</summary>

When enqueuing `nxt` not in parent: `parent[nxt] = (state, action)`.

</details>

<details><summary>Hint 3</summary>

Rebuild: walk parents from the goal to the start, then reverse both lists.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_rooms` | Expand successors in the given order and stop when a dequeued state is a goal. |
| `test_cycles` | Mark states as visited when enqueued so cycles don't loop forever. |
| `test_start_is_goal` | If the start is a goal, return an empty plan. |
| `test_unreachable` | Return None when the queue empties. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

BFS dequeues states in order of distance from the start, so the first goal dequeued is reached by a
shortest plan. Parent pointers recorded at enqueue time make each state's discovery unique and allow
plan reconstruction.

## References

- [Artificial Intelligence: A Modern Approach (4th ed.)](https://aima.cs.berkeley.edu/) — Stuart Russell, Peter Norvig (`S038`)
