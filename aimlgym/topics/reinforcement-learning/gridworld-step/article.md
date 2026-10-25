# A Gridworld Environment

## Learning outcomes

After this lesson you can:

- Encode an environment as states, actions, rewards and terminal flags
- Implement deterministic transitions with walls and boundaries
- Build the full transition table P

## Intuition
An RL environment answers one question: "If I'm here and do this, where do I end up, what reward do I
get, and is the episode over?" A gridworld answers it with a map.

## Precise explanation
Map as strings: `.` empty, `#` wall, `S` start, `G` goal (+10, terminal), `X` pit (−10, terminal).
Every other move costs −1. States are indices `r * n_cols + c`. Actions: 0 = up, 1 = right,
2 = down, 3 = left. Moving into a wall or off the grid leaves the agent in place (still −1).
Stepping from a terminal state is not allowed (episodes end there).

**Transition table:** `P[s][a] = [(1.0, s', r, done)]` for this deterministic world (Sutton & Barto's
four-argument dynamics $p(s', r \mid s, a)$ written as a list). Terminal and wall states map every action
to themselves with reward 0 and `done=True` so that algorithms can iterate over all states safely.

```text
S . . G        state ids:  0  1  2  3
. # . X                    4  5  6  7
```

## Worked example
From state 0, action right → state 1, reward −1, not done. From 2, right → 3 (goal), +10, done.
From 4, right → wall at 5 → stays 4, −1.

## Common mistakes
* Row/column confusion in state ids.
* Treating the goal reward as +10 −1 (choose one convention and document it; here +10).
* Allowing movement through walls.

## Why this matters
RL-08 … RL-10 all run on environments built this way; Gymnasium environments expose the same
`step` interface idea.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Gymnasium Documentation](https://gymnasium.farama.org/) — Farama Foundation (`S035`)
