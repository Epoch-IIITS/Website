# RL-02 · Gridworld Transition Function

**Topic:** Reinforcement Learning · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** RL-01 Discounted Return

Read the lesson first: [article.md](article.md)

## Task

Implement `class GridWorld(rows)` (list of equal-length strings) with attributes `n_rows`, `n_cols`,
`n_states`, `start` (state id of `S`), methods:
* `step(state, action)` → `(next_state, reward, done)` per the rules; raise `ValueError` for invalid
  action/state, a wall state, or a terminal state.
* `build_P()` → dict `P[s][a] = [(1.0, s', r, done)]` for all states (terminal/wall states map to
  themselves with reward 0.0 and `done=True`).

**Example**
```python
g = GridWorld(["S..G", ".#.X"])
g.step(0, 1)   # (1, -1.0, False)
g.step(2, 1)   # (3, 10.0, True)
g.step(4, 1)   # (4, -1.0, False)  — blocked by wall
```

## Hints

<details><summary>Hint 1</summary>

Store `self.grid = rows`; `cell(s)` returns `rows[s // n_cols][s % n_cols]`.

</details>

<details><summary>Hint 2</summary>

Target `(r + dr, c + dc)`; if outside or a wall, stay.

</details>

<details><summary>Hint 3</summary>

Reward/done from the target cell: G → (10, True), X → (−10, True), else (−1, False).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_moves` | State id = row * n_cols + col; action 1 = right, 2 = down. |
| `test_walls_and_bounds` | Moves into walls or off-grid keep the agent in place with reward −1. |
| `test_goal_and_pit` | Goal gives +10 and pit −10, both terminal. |
| `test_P` | Terminal and wall states map to themselves with reward 0 and done=True. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

States are flattened grid coordinates. A move is applied unless it leaves the grid or hits a wall;
the destination cell determines reward and termination. The transition table enumerates `step` for
every state–action pair and makes walls and terminal states absorbing with zero reward.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Gymnasium Documentation](https://gymnasium.farama.org/) — Farama Foundation (`S035`)
