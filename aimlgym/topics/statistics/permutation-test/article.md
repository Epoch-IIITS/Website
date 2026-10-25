# Permutation Tests

## Learning outcomes

After this lesson you can:

- State a null hypothesis as exchangeability
- Implement a seeded Fisher–Yates shuffle
- Compute a two-sided permutation p-value with the +1 correction

## Intuition
If the group labels "A" and "B" don't matter (the null hypothesis), then shuffling the labels
should produce differences in means just as large as the one we observed, fairly often. If
almost no shuffle produces a difference as extreme as the real one, the labels probably *do*
matter.

## Precise explanation
1. Observed statistic $d_\text{obs} = \bar x - \bar y$.
2. Pool all values. For $b = 1..B$: shuffle the pool, call the first $n_x$ values "x" and the
   rest "y", compute $d_b$.
3. Two-sided p-value with the standard +1 correction (counts the observed arrangement, never 0):
$$p = \frac{1 + \#\{b: |d_b| \ge |d_\text{obs}|\}}{B + 1}.$$

**Fisher–Yates shuffle** (uniform over permutations) using only `rng.random()`:
```text
for i from n-1 down to 1:
    j = int(rng.random() * (i + 1))   # 0 <= j <= i
    swap items[i], items[j]
```
Floating-point noise can make $|d_b|$ differ from $|d_\text{obs}|$ in the last bits even for
identical arrangements; compare with a small tolerance (`>= abs_obs - 1e-12`).

## Worked example
x = [5, 6, 7], y = [1, 2, 3]: $d_\text{obs} = 4$. Only the 2 of the 20 equally likely splits
(x and y swapped) are as extreme, so the exact p-value is 2/20 = 0.1; a Monte Carlo estimate
with many shuffles is close to 0.1.

## Common mistakes
* Shuffling `x` and `y` separately (labels never move).
* Biased shuffles such as `j = int(rng.random() * n)` for every i.
* Reporting p = 0.

## Why this matters
Permutation tests make almost no distributional assumptions; they also underlie permutation
feature importance (XA-08), where shuffling a feature breaks its link with the target.

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html) — Python Software Foundation (`S004`)
