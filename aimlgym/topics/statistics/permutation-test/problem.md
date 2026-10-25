# ST-20 · Permutation Test for a Mean Difference by Hand

**Topic:** Statistics · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** ST-13 Bootstrap Confidence Interval, ST-18 Welch's t-statistic by Hand

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `fisher_yates(items, rng)` → a **new** shuffled list using exactly the recipe above
  (input unchanged).
* `permutation_test(x, y, n_perm=5000, seed=0)` → dict `{"observed": d_obs, "p_value": p}`.
  Use `rng = random.Random(seed)`; each permutation shuffles the pooled list `x + y` with
  `fisher_yates` (starting from the original pool each time). Count `abs(d_b) >= abs(d_obs) - 1e-12`.
  Raise `ValueError` if either group is empty or `n_perm < 1`.

**Examples**
```python
r = permutation_test([5, 6, 7], [1, 2, 3], n_perm=4000, seed=0)
r["observed"]                      # 4.0
abs(r["p_value"] - 0.1) < 0.02     # True
permutation_test([1, 2, 3], [1, 2, 3], n_perm=100)["p_value"]   # 1.0
```

## Hints

<details><summary>Hint 1</summary>

Copy first: `a = list(items)`, then loop `for i in range(len(a) - 1, 0, -1)`.

</details>

<details><summary>Hint 2</summary>

`j = int(rng.random() * (i + 1))`; `a[i], a[j] = a[j], a[i]`.

</details>

<details><summary>Hint 3</summary>

Split each shuffled pool into `p[:nx]` and `p[nx:]` and compare absolute differences.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_fy_recipe` | Loop i from n−1 down to 1 and use j = int(rng.random()*(i+1)). |
| `test_fy_uniform_first_position` | A biased shuffle (j over the whole list) fails this check. |
| `test_identical_groups` | Use abs(d) >= abs(d_obs) − 1e-12 so ties count. |
| `test_p_never_zero` | Use (hits + 1) / (n_perm + 1). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The Fisher–Yates loop picks each position's element uniformly from the not-yet-fixed prefix,
giving every permutation equal probability. Each permutation reassigns labels at random; the
fraction of shuffles at least as extreme as the observed difference (plus the observed
arrangement itself) is the p-value.

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html) — Python Software Foundation (`S004`)
