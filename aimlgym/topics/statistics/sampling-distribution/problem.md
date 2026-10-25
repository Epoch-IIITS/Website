# ST-12 · Sampling Distributions and Standard Error

**Topic:** Statistics · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** ST-10 Dice Simulation and the Law of Large Numbers, ST-09 The Normal Distribution

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `sample_means(population, n, reps, seed)` → a list of `reps` sample means. Use one
   `rng = random.Random(seed)`; for each repetition draw `n` values with replacement, each as
   `population[int(rng.random() * len(population))]`, and record their mean.
2. `standard_error(sample)` → $s / \sqrt n$ with the $n-1$ sample standard deviation; raise
   `ValueError` if the sample has fewer than 2 values.
3. `mean_ci95(sample)` → `(low, high)` = mean ∓ z · SE with `z = NormalDist().inv_cdf(0.975)`.

**Example**
```python
means = sample_means([1, 2, 3, 4, 5, 6], 25, 2000, seed=0)
len(means)                 # 2000
# their standard deviation is close to 1.708 / 5 ≈ 0.342
standard_error([2, 4, 4, 4, 5, 5, 7, 9])   # ≈ 0.7559
```

## Hints

<details><summary>Hint 1</summary>

Create the generator once, outside the repetitions loop, so each repetition continues the stream.

</details>

<details><summary>Hint 2</summary>

Sample variance: `sum((x - m) ** 2 for x in sample) / (n - 1)`; SE is `sqrt(var) / sqrt(n)`.

</details>

<details><summary>Hint 3</summary>

`z = NormalDist().inv_cdf(0.975)`; return `(m - z * se, m + z * se)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_recipe_matches` | Create one `random.Random(seed)` and draw indices with `int(rng.random() * len(population))`, n per repetition. |
| `test_spread_shrinks_like_sqrt_n` | Each repetition must draw n values with replacement and record their mean. |
| `test_standard_error` | Use the n - 1 sample standard deviation divided by sqrt(n). |
| `test_ci95` | Use `NormalDist().inv_cdf(0.975)` (≈ 1.96) times the standard error on both sides of the mean. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A single seeded generator produces every draw, so the whole simulation is reproducible and
uses only `random()`, whose output Python guarantees across versions. The standard error uses the
unbiased $n-1$ variance, and the interval combines it with the exact 97.5% normal quantile.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html) — Python Software Foundation (`S004`)
