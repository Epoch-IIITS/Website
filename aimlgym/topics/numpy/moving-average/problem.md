# NP-14 · Moving Average with cumsum

**Topic:** NumPy · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** NP-08 Reshape and Stack

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `moving_average(x, w)` → float array of length `n - w + 1` with the mean of each full window,
  computed with `np.cumsum` (no Python loops). Raise `ValueError` unless `1 <= w <= len(x)`.
* `windows(x, w)` → `(n - w + 1, w)` array of all windows (use `sliding_window_view`).

**Examples**
```python
moving_average([1, 2, 3, 4, 5], 2)   # array([1.5, 2.5, 3.5, 4.5])
moving_average([4, 8], 2)            # array([6.])
windows(np.arange(4), 3)             # [[0, 1, 2], [1, 2, 3]]
```

## Hints

<details><summary>Hint 1</summary>

`c = np.concatenate([[0.0], np.cumsum(x)])`.

</details>

<details><summary>Hint 2</summary>

Window sums are `c[w:] - c[:-w]`.

</details>

<details><summary>Hint 3</summary>

`np.lib.stride_tricks.sliding_window_view(x, w)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Prepend 0 to the cumulative sum, then use c[w:] − c[:-w]. |
| `test_matches_convolve` | Return only full ('valid') windows: length n − w + 1. |
| `test_bad_w` | Validate 1 <= w <= len(x). |
| `test_windows` | Use np.lib.stride_tricks.sliding_window_view(x, w). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Prefix sums turn each window sum into one subtraction, so all n − w + 1 means come from two
vector slices. `sliding_window_view` exposes every window as a strided view without copying.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
