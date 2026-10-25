# AG-04 · Perceive-Act Loop

**Topic:** Agentic AI · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** AG-01 Tool Registry and Dispatch

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `reflex_vacuum_agent(percept)` with the rules above.
* `class VacuumWorld(dirt, location)` — `dirt` is a dict `{"A": bool, "B": bool}` (True = dirty),
  `location` "A" or "B"; methods `percept()` → `(location, "Dirty" | "Clean")` and `execute(action)`
  (unknown action → `ValueError`; Left at A / Right at B do nothing but still count as movement).
* `run(agent, env, steps)` → `(log, score)` where `log` is a list of `(percept, action)` and score
  follows the performance measure (after each action: +1 per clean square, −1 if the action was
  Left/Right).

**Example**
```python
log, score = run(reflex_vacuum_agent, VacuumWorld({"A": True, "B": True}, "A"), 4)
[a for _, a in log]   # ['Suck', 'Right', 'Suck', 'Left']
score                 # 1 + (−1 + 1) + 2 + (−1 + 2) = 4
```

## Hints

<details><summary>Hint 1</summary>

Agent: `loc, status = percept`.

</details>

<details><summary>Hint 2</summary>

`execute`: Suck sets `dirt[loc] = False`; Left → 'A'; Right → 'B'.

</details>

<details><summary>Hint 3</summary>

Score after each step: `sum(not d for d in env.dirt.values()) - (1 if action in ('Left', 'Right') else 0)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_run` | Score after each action: clean squares minus 1 for movement. |
| `test_percepts_logged` | Log the percept seen *before* the action. |
| `test_input_dict_not_mutated` | Copy the dirt dict inside VacuumWorld. |
| `test_clean_world_oscillates` | A simple reflex agent keeps moving even when everything is clean. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The agent sees only its percept and applies condition–action rules. The environment owns the state
and dynamics. The loop alternates perception, decision and execution, scoring cleanliness and
penalising movement after every step.

## References

- [Artificial Intelligence: A Modern Approach (4th ed.)](https://aima.cs.berkeley.edu/) — Stuart Russell, Peter Norvig (`S038`)
