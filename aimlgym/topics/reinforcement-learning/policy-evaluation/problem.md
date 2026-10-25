# RL-08 · Iterative Policy Evaluation

**Topic:** Reinforcement Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** RL-02 Gridworld Transition Function, RL-01 Discounted Return

Read the lesson first: [article.md](article.md)

## Task

Write `policy_evaluation(P, policy, gamma=0.9, theta=1e-10, max_iter=10000)` returning
`(V, n_iter)` where `P` uses the topic's format, `policy` is an array `(n_states, n_actions)` of
probabilities, and `V` a float array. Synchronous sweeps; stop when the max change `< theta`.
Raise `ValueError` if a policy row does not sum to 1 (tolerance 1e-8) or `gamma` not in `[0, 1)`.

**Example**
```python
P = {0: {0: [(1.0, 1, -1.0, False)]}, 1: {0: [(1.0, 2, 10.0, True)]}, 2: {0: [(1.0, 2, 0.0, True)]}}
V, _ = policy_evaluation(P, np.ones((3, 1)), gamma=0.9)
V   # [8., 10., 0.]
```

## Hints

<details><summary>Hint 1</summary>

`V = np.zeros(n_states)`; each sweep build `new = np.zeros_like(V)`.

</details>

<details><summary>Hint 2</summary>

`new[s] += policy[s, a] * p * (r + gamma * (0 if done else V[s2]))`.

</details>

<details><summary>Hint 3</summary>

Stop when `np.max(np.abs(new - V)) < theta`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_corridor` | Don't bootstrap from transitions with done=True. |
| `test_stochastic_policy` | Weight each action's backup by π(a|s). |
| `test_stochastic_transitions` | Weight each outcome by its probability p. |
| `test_bellman_fixed_point` | Keep sweeping until the max change is below θ. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each sweep computes, for every state, the policy-weighted expected one-step reward plus discounted
next-state value, using the previous sweep's values. Terminal transitions contribute only their
reward. Iteration stops once values change by less than θ.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Dive into Deep Learning — Reinforcement Learning chapter](https://d2l.ai/chapter_reinforcement-learning/index.html) — Pratik Chaudhari, Rasool Fakoor, Kavosh Asadi (D2L) (`S034`)
