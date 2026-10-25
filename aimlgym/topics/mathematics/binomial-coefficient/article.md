# Counting Combinations

## Learning outcomes

After this lesson you can:

- Count combinations
- Use the multiplicative formula to avoid huge factorials
- Exploit symmetry C(n,k) = C(n,n-k)

## Intuition
"How many different 3-person teams can be chosen from 5 students?" Order does not matter, so
{Ann, Bob, Cy} is the same team as {Cy, Ann, Bob}. The answer is the **binomial coefficient**
$\binom{5}{3} = 10$.

## Precise explanation
$$\binom{n}{k} = \frac{n!}{k!\,(n-k)!}\quad (0\le k\le n),\qquad \binom{n}{k}=0 \text{ if } k>n.$$
Computing three factorials is wasteful. The **multiplicative formula** builds the result step by
step and stays an integer at every step:
$$\binom{n}{k} = \prod_{i=1}^{k} \frac{n-k+i}{i}.$$
```python
r = 1
for i in range(1, k + 1):
    r = r * (n - k + i) // i      # exact: r*(n-k+i) is always divisible by i
```
Because $\binom{n}{k} = \binom{n}{n-k}$, use `k = min(k, n - k)` to do fewer steps.

Pascal's rule $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$ gives Pascal's triangle.

## Worked example
$\binom{5}{2}$: r = 1 → 1·4//1 = 4 → 4·5//2 = 10.

## Common mistakes
* Using `/` (float division) → large values lose precision (e.g. `comb(60, 30)`).
* Writing `r = r // i * (n-k+i)` — dividing first may not be exact.
* Forgetting $\binom{n}{0} = 1$ and $\binom{n}{k} = 0$ for $k > n$.

## Why this matters
Binomial coefficients give the binomial distribution (ST-08), count subsets for exact Shapley
values (XA-11), and count n-gram / feature combinations.

## Library implementation

`math.comb(n, k)` is the standard-library binomial coefficient (exact integers, returns 0 when
`k > n`). ST-08 uses it directly once you have seen how it works.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
