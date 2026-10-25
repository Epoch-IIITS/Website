# Returns and Discounting

## Learning outcomes

After this lesson you can:

- Compute the discounted return of a reward sequence
- Compute returns for every time step in one backward pass
- Explain the role of the discount factor γ

## Intuition
An RL agent cares about the total reward it will collect, not just the next reward. Rewards far in
the future are usually worth a bit less — like money with interest — so we **discount** them.

## Precise explanation (Sutton & Barto, ch. 3)
For rewards $R_{t+1}, R_{t+2}, \dots, R_T$ and $0 \le \gamma \le 1$:
$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots = \sum_{k=0}^{T-t-1}\gamma^k R_{t+k+1}.$$
**Recursive form:** $G_t = R_{t+1} + \gamma G_{t+1}$ with $G_T = 0$. Scanning rewards backwards
computes all returns in O(T) — the same "carry state through a loop" pattern as Fibonacci (PY-14).
γ = 0: only the immediate reward matters; γ close to 1: far-sighted.

## Worked example
rewards [1, 0, 2], γ = 0.5: G₂ = 2; G₁ = 0 + 0.5·2 = 1; G₀ = 1 + 0.5·1 = 1.5.

## Common mistakes
* Discounting the first reward ($\gamma^1 R_1$ instead of $\gamma^0 R_1$).
* Forward loops recomputing sums (O(T²)).
* γ > 1 (returns may diverge).

## Why this matters
Every value function, policy-gradient method and RL loss is built on returns.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Dive into Deep Learning — Reinforcement Learning chapter](https://d2l.ai/chapter_reinforcement-learning/index.html) — Pratik Chaudhari, Rasool Fakoor, Kavosh Asadi (D2L) (`S034`)
