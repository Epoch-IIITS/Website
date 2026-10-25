# ST-05 · Standardize to z-scores

**Topic:** Statistics · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** ST-01 Mean and Variance (Population vs Sample)

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `z_scores(data, sample=False)` → list of floats; use the population sd unless `sample=True`.
  Raise `ValueError` for empty data or zero standard deviation.
* `outliers(data, threshold=3.0)` → sorted list of **indices** whose population z-score has
  `abs(z) > threshold`.

**Examples**
```python
z_scores([2, 4, 4, 4, 5, 5, 7, 9])   # [-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]
outliers([10, 11, 9, 10, 50], threshold=1.5)   # [4]
```

## Hints

<details><summary>Hint 1</summary>

Compute mean and variance (n or n−1), then `sd = math.sqrt(var)`.

</details>

<details><summary>Hint 2</summary>

Raise ValueError if `sd == 0`.

</details>

<details><summary>Hint 3</summary>

`[i for i, z in enumerate(z_scores(data)) if abs(z) > threshold]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Divide by the standard deviation (sqrt of variance), not the variance. |
| `test_sample_variant` | With sample=True use n − 1 in the variance. |
| `test_constant` | Raise ValueError when sd == 0. |
| `test_outliers` | Return indices, not values, and compare abs(z) > threshold. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The mean and standard deviation are computed once and every value is shifted and scaled. A zero
spread makes standardization meaningless, so it is rejected. `outliers` reuses `z_scores` and
returns indices so the caller can locate the original records.

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
