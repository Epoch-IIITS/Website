# ST-01 · Mean and Variance (Population vs Sample)

**Topic:** Statistics · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** MA-01 Summation and Product Notation

Read the lesson first: [article.md](article.md)

## Task

Write `mean_variance(data, sample=False)` returning `(mean, variance)` as floats using the
two-pass method.

* `sample=False` → divide by `n`; `sample=True` → divide by `n - 1`.
* Raise `ValueError` if `data` is empty, or if `sample=True` and `len(data) < 2`.
* Do not use the `statistics` module.

**Examples**
```python
mean_variance([2, 4, 4, 4, 5, 5, 7, 9])               # (5.0, 4.0)
mean_variance([2, 4, 4, 4, 5, 5, 7, 9], sample=True)  # (5.0, 4.571428571428571)
mean_variance([3])                                    # (3.0, 0.0)
```

## Hints

<details><summary>Hint 1</summary>

Validate the length first, depending on `sample`.

</details>

<details><summary>Hint 2</summary>

Pass 1: `m = sum(data) / n`. Pass 2: `ss = sum((x - m) ** 2 for x in data)`.

</details>

<details><summary>Hint 3</summary>

Divide `ss` by `n - 1` if sample else `n`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_sample` | Sample variance divides by n − 1. |
| `test_large_offset_stable` | Use the two-pass method; E[x²] − E[x]² loses precision for large values. |
| `test_single_sample_error` | Sample variance of one value is undefined — raise ValueError. |
| `test_population` | Return the mean as a float and divide by n for population variance. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The mean is computed first, then the sum of squared deviations from it. The only difference
between population and sample variance is the denominator. Validation prevents division by zero.

## References

- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
