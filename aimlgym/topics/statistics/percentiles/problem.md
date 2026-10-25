# ST-03 · Percentiles by Linear Interpolation

**Topic:** Statistics · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** ST-02 Median and Mode

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `percentile(data, q)` with the linear method above; `0 <= q <= 100` else `ValueError`;
  empty data → `ValueError`.
* `iqr(data)` → `percentile(data, 75) - percentile(data, 25)`.
* `tukey_outliers(data, k=1.5)` → sorted list of the **values** outside the fences.

**Examples**
```python
percentile([1, 2, 3, 4, 10], 40)   # 2.6
iqr([1, 2, 3, 4, 10])              # 2.0
tukey_outliers([1, 2, 3, 4, 10])   # [10]
```

## Hints

<details><summary>Hint 1</summary>

`s = sorted(data)`, `r = q / 100 * (len(s) - 1)`.

</details>

<details><summary>Hint 2</summary>

`i = math.floor(r)`, `f = r - i`; if `i + 1 < len(s)` interpolate, else return `s[i]`.

</details>

<details><summary>Hint 3</summary>

Fences: `lo = p25 - k * iqr`, `hi = p75 + k * iqr`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_interp` | Use rank r = q/100·(n−1) and interpolate between s[i] and s[i+1]. |
| `test_ends` | q = 100 gives the maximum; guard against indexing s[n]. |
| `test_known_values` | Make sure you sort the data first. |
| `test_tukey` | Return the outlying values (sorted), not their indices. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The fractional rank r locates the percentile between two neighbouring sorted values, and linear
interpolation blends them. The IQR and Tukey fences are built from the 25th and 75th percentiles.

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
