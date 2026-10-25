# The Binomial Distribution

## Learning outcomes

After this lesson you can:

- Apply the binomial PMF
- Compute cumulative and tail probabilities
- Check that probabilities sum to 1

## Intuition
Flip a biased coin $n$ times. The number of heads is random; the binomial distribution says how
likely each count is. Every count $k$ can happen in $\binom{n}{k}$ orders, each with the same
probability.

## Precise explanation
For $n$ independent trials with success probability $p$:
$$P(X=k) = \binom{n}{k} p^k (1-p)^{n-k},\qquad k = 0,\dots,n.$$
Cumulative: $P(X \le k) = \sum_{j=0}^{k} P(X=j)$. Tail: $P(X \ge k) = 1 - P(X \le k-1)$.
Mean $np$, variance $np(1-p)$. Values of $k$ outside $0..n$ have probability 0.

`math.comb(n, k)` gives the binomial coefficient (you implemented it in MA-07).
In Python `0 ** 0 == 1`, which correctly handles $p = 0$ or $p = 1$ at the boundaries.

## Worked example
$n = 4$, $p = 0.5$: $P(X=2) = 6 \cdot 0.5^4 = 0.375$.
$P(X \ge 3) = P(3) + P(4) = 4/16 + 1/16 = 0.3125$.

## Common mistakes
* Forgetting the $\binom{n}{k}$ factor (computing one specific sequence).
* Computing $P(X\ge k)$ as $1 - P(X \le k)$ (off by one).
* Not validating $0 \le p \le 1$.

## Why this matters
Accuracy on a test set of $n$ examples is a binomial proportion; A/B tests, dropout masks
(DL-21) and client participation (FL-08) are Bernoulli processes.

## Library implementation

`scipy.stats.binom(n, p)` provides `.pmf(k)`, `.cdf(k)` and `.sf(k - 1)` (the survival function,
$P(X \ge k)$), computed in a numerically careful way for large `n`. The comparison runs only when
SciPy is installed.

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
