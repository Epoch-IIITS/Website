# TD(0): Learning from Every Step

## Learning outcomes

After this lesson you can:

- Update values from single transitions (bootstrapping)
- Implement the TD error
- Compare TD(0) with Monte Carlo on the same experience

## Intuition
Monte Carlo waits until the end of an episode. TD learning updates immediately after each step, using
its own current estimate of the next state's value as a stand-in for the rest of the return —
"learning a guess from a guess" (bootstrapping).

## Precise explanation (Sutton & Barto, §6.1)
For a transition $(s, r, s', d)$:
$$\delta = r + \gamma(1-d)V(s') - V(s),\qquad V(s) \leftarrow V(s) + \alpha\,\delta.$$
δ is the **TD error**. Transitions are processed in order, updating V in place. With a decaying (or
small) α and enough experience, TD(0) converges to $V^\pi$; on finite batches repeated many times
(batch TD) it converges to the certainty-equivalence estimate, which can differ from the MC average.

## Worked example
V = [0, 0], transition (0, r = 1, s' = 1, not done), then (1, r = 2, terminal), α = 0.5, γ = 1:
δ₁ = 1 + 0 − 0 = 1 → V(0) = 0.5; δ₂ = 2 − 0 = 2 → V(1) = 1.

## Common mistakes
* Bootstrapping from terminal states.
* Updating with the *new* V(s) inside the same δ computation (compute δ first).
* α too large → oscillations.

## Why this matters
TD learning underlies Q-learning, SARSA, actor–critic methods and value learning in modern deep RL.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
