# Simulation and the Law of Large Numbers

## Learning outcomes

After this lesson you can:

- Simulate a discrete random variable reproducibly
- Track a running mean
- Observe the law of large numbers

## Intuition
The expected sum of two fair dice is 7. Roll them 10 times and the average may be 6.2 or 8.1;
roll them 100 000 times and it will be very close to 7. The **law of large numbers** says sample
averages settle down to the expected value as the sample grows.

## Precise explanation
For i.i.d. $X_i$ with mean $\mu$, the running mean $\bar X_n = \frac1n\sum_{i\le n} X_i$
converges to $\mu$. Its typical error shrinks like $\sigma/\sqrt n$: 100× more rolls ≈ 10× less
error.

**Reproducible randomness.** `random.Random(seed)` creates an independent generator. Python only
guarantees the sequence of `rng.random()` (floats in $[0, 1)$) across versions, so we derive die
faces from it:
$$\text{face} = \lfloor 6u \rfloor + 1,\quad u = \text{rng.random()}.$$
Since $0 \le u < 1$, faces are 1..6 with equal probability.

## Worked example
If the first four `rng.random()` values were 0.10, 0.95, 0.50, 0.33, the faces are 1, 6, 4, 2;
the first two-dice roll sums to 7, the second to 6; running means 7.0, 6.5.

## Common mistakes
* Using the global `random.seed`, which other code can disturb.
* `int(u * 6)` without `+ 1` (faces 0..5) or `round(u * 6)` (faces 0..6 with uneven odds).
* Expecting the running mean to equal exactly 7.

## Why this matters
Monte Carlo simulation estimates quantities that are hard to compute exactly — expected returns
in RL (RL-11), bootstrap confidence intervals (ST-13), dropout's expected behaviour.

## References

- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html) — Python Software Foundation (`S004`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
