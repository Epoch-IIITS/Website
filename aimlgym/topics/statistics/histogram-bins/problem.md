# ST-04 · Histogram with Equal-Width Bins

**Topic:** Statistics · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** ST-01 Mean and Variance (Population vs Sample)

Read the lesson first: [article.md](article.md)

## Task

Write `histogram(data, bins, lo=None, hi=None)` returning `(edges, counts)`.

* `edges` has `bins + 1` floats; `counts` has `bins` ints.
* Default `lo = min(data)`, `hi = max(data)`; if `lo == hi`, use `lo - 0.5` and `hi + 0.5`.
* Bins are `[e_j, e_{j+1})` except the last, which includes `hi`. Ignore values outside `[lo, hi]`.
* Raise `ValueError` if `bins < 1`, if `data` is empty and `lo`/`hi` are not both given, or if
  `lo > hi`.

**Examples**
```python
histogram([1, 2, 2, 3, 4, 5], 2)
# ([1.0, 3.0, 5.0], [3, 3])
histogram([0, 10, 11], 2, lo=0, hi=10)
# ([0.0, 5.0, 10.0], [1, 1])   — 11 is outside and ignored; 10 lands in the last bin
```

## Hints

<details><summary>Hint 1</summary>

Resolve lo/hi defaults first, then `w = (hi - lo) / bins`.

</details>

<details><summary>Hint 2</summary>

`edges = [lo + j * w for j in range(bins + 1)]`.

</details>

<details><summary>Hint 3</summary>

For each x in range, `j = int((x - lo) / w)`; if `j == bins` set `j = bins - 1`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_max_in_last_bin` | The maximum value must go in the last (closed) bin — clamp index bins → bins−1. |
| `test_explicit_range_outside` | Skip values below lo or above hi. |
| `test_constant_data` | When lo == hi, widen to [lo−0.5, hi+0.5]. |
| `test_matches_numpy_convention` | A value exactly on an interior edge belongs to the bin on its right. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Defaults and degenerate ranges are resolved before computing the width. Edges are computed by
multiplication (and the last edge pinned to hi to avoid rounding drift). Each in-range value's
bin index is the floor of its scaled position; the value equal to hi would land in a non-existent
bin `bins`, so it is clamped into the last, closed bin.

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
