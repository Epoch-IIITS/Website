# Incremental Estimates for Bandits

## Learning outcomes

After this lesson you can:

- Update sample-average estimates incrementally
- Use a constant step size for non-stationary rewards
- Track action counts

## Intuition
A slot machine's average payout can be tracked without storing every result: nudge the estimate
towards each new reward by a fraction of the error.

## Precise explanation (Sutton & Barto, §2.4–2.5)
Sample average after n rewards: $Q_{n+1} = Q_n + \frac{1}{n}(R_n - Q_n)$ — exactly the mean, using
O(1) memory. General form "NewEstimate ← OldEstimate + StepSize · (Target − OldEstimate)".
With a **constant** step size α, recent rewards weigh more (exponential recency-weighted average),
which tracks changing (non-stationary) reward distributions:
$Q_{n+1} = Q_n + \alpha(R_n - Q_n)$.

## Worked example
Rewards for one arm: 2, 4, 6. Sample average: 0 → 2 → 3 → 4. α = 0.5 from 0: 1 → 2.5 → 4.25.

## Common mistakes
* Incrementing the count after computing 1/n (off by one).
* Sharing one count across all arms.
* Using 1/n on non-stationary problems (adapts too slowly).

## Why this matters
This update pattern is the seed of TD learning and Q-learning (RL-12, RL-13).

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
