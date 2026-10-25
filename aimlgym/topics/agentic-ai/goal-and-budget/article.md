# Goals, Budgets and Stopping Conditions

## Learning outcomes

After this lesson you can:

- Stop an agent when its goal is reached
- Enforce step and cost budgets
- Report why a run ended

## Intuition
An agent that never stops is a bug — and an expensive one when every step calls a paid model. Agents
need an explicit goal test and hard limits on steps and cost, plus a clear record of *why* they
stopped.

## Precise explanation
Loop:
```text
for step in 1..max_steps:
    if goal_test(state): return "success"
    action = policy(state)
    state, cost = transition(state, action)
    total += cost
    if max_cost is not None and total > max_cost: return "cost_exceeded"
check goal once more after the last step → "success" else "step_limit"
```
Return the status, final state, trajectory of actions and total cost. Checking the goal *before* acting
means an already-solved task costs nothing. Anthropic's agent guidance recommends stopping conditions
such as a maximum number of iterations to maintain control.

## Worked example
Counter from 0, goal ≥ 3, action +1 cost 1: max_steps 5 → success after 3 actions, cost 3;
max_steps 2 → step_limit with state 2; max_cost 1.5 → cost_exceeded after the second action.

## Common mistakes
* Off-by-one between steps and actions.
* Checking cost before applying it (overspend by one step).
* Returning only the final state with no reason.

## Why this matters
Budgets and termination reasons are essential for safe, debuggable agents (AG-06, AG-19).

## References

- [Artificial Intelligence: A Modern Approach (4th ed.)](https://aima.cs.berkeley.edu/) — Stuart Russell, Peter Norvig (`S038`)
- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
