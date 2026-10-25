# NP-08 · Reshape and Stack

**Topic:** NumPy · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** NP-03 Slicing a Sub-grid

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `to_batches(x, batch_size)` → 1-D `x` reshaped to `(n // batch_size, batch_size)`, dropping the
  incomplete last batch. Raise `ValueError` if `batch_size < 1` or `> len(x)`.
* `add_bias_column(X)` → `X` (shape `(n, d)`) with a column of ones prepended → `(n, d+1)`.
* `flatten_images(imgs)` → `(N, H, W)` → `(N, H*W)`, row-major per image; raise `ValueError` if
  `imgs.ndim != 3`.

**Examples**
```python
to_batches(np.arange(10), 4)          # [[0, 1, 2, 3], [4, 5, 6, 7]]
add_bias_column(np.array([[3, 4], [5, 6]]))   # [[1., 3., 4.], [1., 5., 6.]]
flatten_images(np.arange(8).reshape(2, 2, 2)) # [[0, 1, 2, 3], [4, 5, 6, 7]]
```

## Hints

<details><summary>Hint 1</summary>

`m = len(x) // batch_size; x[: m * batch_size].reshape(m, batch_size)`.

</details>

<details><summary>Hint 2</summary>

`np.hstack([np.ones((n, 1)), X])`.

</details>

<details><summary>Hint 3</summary>

`imgs.reshape(imgs.shape[0], -1)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_batches` | Drop the remainder before reshaping to (-1, batch_size). |
| `test_bias` | The ones column comes first (prepended). |
| `test_flatten` | Keep axis 0 (the batch) and flatten the rest with reshape(N, -1). |
| `test_batches_bad` | Validate batch_size between 1 and len(x). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Truncating to a multiple of the batch size makes the reshape valid. The bias column is a
column of ones joined horizontally. Flattening keeps the batch axis and lets `-1` compute H·W.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
