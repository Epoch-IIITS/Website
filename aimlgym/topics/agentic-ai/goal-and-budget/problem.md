# AG-05 · Goal Tests and Step Budgets

**Topic:** Agentic AI · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** AG-04 Perceive-Act Loop

Read the lesson first: [article.md](article.md)

## Task

Write `run_with_budget(state, policy, transition, goal_test, max_steps, max_cost=None)` returning a dict
`{"status": "success" | "step_limit" | "cost_exceeded", "state": final_state, "actions": list,
"cost": total_cost}` following the pseudocode. Raise `ValueError` if `max_steps < 0`.

**Example**
```python
r = run_with_budget(0, lambda s: "inc", lambda s, a: (s + 1, 1.0), lambda s: s >= 3, max_steps=5)
r["status"], r["state"], r["cost"]    # ('success', 3, 3.0)
```

## Hints

<details><summary>Hint 1</summary>

Initialise `actions, total = [], 0.0`.

</details>

<details><summary>Hint 2</summary>

Inside the loop: goal test first, then act, then add cost and check `total > max_cost`.

</details>

<details><summary>Hint 3</summary>

After the loop, check the goal once more before returning step_limit.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_already_done` | Test the goal before taking the first action. |
| `test_success_on_last_step` | Check the goal once more after the loop. |
| `test_cost_exceeded` | Add the step's cost, then compare total > max_cost. |
| `test_exact_budget_ok` | Spending exactly max_cost is allowed. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The goal is tested before each action so solved tasks stop immediately. After every action the cost is
accumulated and compared with the budget. When the step limit is reached, a final goal test decides
between success and step_limit.

## References

- [Artificial Intelligence: A Modern Approach (4th ed.)](https://aima.cs.berkeley.edu/) — Stuart Russell, Peter Norvig (`S038`)
- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
