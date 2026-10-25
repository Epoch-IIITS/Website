# NP-09 · Fancy Indexing and Gather

**Topic:** NumPy · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** NP-04 Boolean Masks, NP-05 Aggregations Along Axes

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `gather_rows(X, idx)` → rows of `X` at integer indices `idx` (order and repeats preserved).
* `pick_per_row(P, cols)` → 1-D array with `P[i, cols[i]]`; raise `ValueError` if
  `len(cols) != P.shape[0]`.
* `top_k(v, k)` → indices of the `k` largest values of 1-D `v`, largest first, ties broken by
  lower index; raise `ValueError` unless `1 <= k <= len(v)`.

**Examples**
```python
P = np.array([[0.1, 0.7, 0.2], [0.5, 0.3, 0.2]])
pick_per_row(P, [1, 0])           # array([0.7, 0.5])
top_k(np.array([3, 9, 9, 1]), 2)  # array([1, 2])
```

## Hints

<details><summary>Hint 1</summary>

`X[np.asarray(idx)]`.

</details>

<details><summary>Hint 2</summary>

`P[np.arange(P.shape[0]), cols]`.

</details>

<details><summary>Hint 3</summary>

`np.argsort(-v, kind='stable')[:k]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_pick` | Use P[np.arange(n), cols], not P[:, cols]. |
| `test_topk_ties` | argsort(-v, kind='stable') keeps lower indices first on ties; reversing argsort(v) does not. |
| `test_gather` | Integer-array indexing keeps order and repeats. |
| `test_pick_bad` | Validate one column index per row. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Integer-array indexing gathers rows directly. Pairing `arange(n)` with the column indices picks
one element per row. Sorting the negated values with a stable algorithm yields descending order
with ties resolved by original position.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
