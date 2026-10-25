# Upper Confidence Bound (UCB)

## Learning outcomes

After this lesson you can:

- Select actions by optimism in the face of uncertainty
- Implement UCB1 with initial exploration of every arm
- Measure cumulative regret

## Intuition
Prefer arms that are either good *or* poorly explored. UCB adds an exploration bonus that shrinks the
more often an arm is tried — "optimism in the face of uncertainty".

## Precise explanation (Sutton & Barto, §2.7)
At time t (1-based count of pulls so far + 1), choose
$$A_t = \arg\max_a \left[Q(a) + c\sqrt{\frac{\ln t}{N(a)}}\right],$$
with any arm having $N(a) = 0$ chosen first (lowest index). Ties → lowest index.
**Regret** after T steps: $T\mu^* - \sum_t \mu_{A_t}$ — reward lost compared with always pulling the
best arm. UCB's regret grows logarithmically; ε-greedy with constant ε grows linearly.

Simulation here: Bernoulli arms with success probabilities `means`; reward = 1 if
`rng.random() < means[a]` else 0 (one draw per step, after choosing the action).

## Worked example
Q = [0.5, 0.4], N = [10, 2], t = 13, c = 2: bonuses 2√(ln13/10) ≈ 1.01 and 2√(ln13/2) ≈ 2.26 →
scores 1.51 vs 2.66 → explore arm 1.

## Common mistakes
* Dividing by zero for untried arms.
* Using ln of the per-arm count instead of total time.
* Forgetting to update counts after pulling.

## Why this matters
UCB ideas power Monte Carlo tree search (AlphaGo) and many recommendation/A-B testing systems.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
