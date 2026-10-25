# Fancy (Integer-Array) Indexing

## Learning outcomes

After this lesson you can:

- Index with integer arrays
- Pick one element per row with paired index arrays
- Find top-k indices with argsort

## Intuition
Sometimes you know exactly *which* positions you want — rows 3, 0 and 3 again, or "the
probability of the correct class in each row". Passing integer arrays as indices fetches exactly
those elements in that order.

## Precise explanation
* `X[[3, 0, 3]]` returns rows 3, 0, 3 (copies, repeats allowed).
* Paired index arrays select individual elements:
  `P[np.arange(n), cols]` returns `[P[0, cols[0]], P[1, cols[1]], …]`.
  This is **not** the same as `P[:, cols]`, which returns whole columns (an n × n block).
* `np.argsort(v)` returns indices that would sort `v` ascending. For top-k largest use
  `np.argsort(-v, kind="stable")[:k]`; the stable sort keeps the lower index first on ties.

## Worked example
```python
P = np.array([[0.1, 0.7, 0.2],
              [0.5, 0.3, 0.2]])
P[np.arange(2), [1, 0]]     # [0.7, 0.5]
np.argsort(-np.array([3, 9, 9, 1]), kind="stable")[:2]   # [1, 2]
```

## Common mistakes
* `P[:, cols]` instead of `P[np.arange(n), cols]`.
* Using `argsort(v)[::-1]` for top-k — reverses tie order too.
* Indices out of range raise `IndexError`.

## Why this matters
Cross-entropy picks the predicted probability of the true class per row (DL-03); k-NN and
retrieval pick top-k neighbours; embedding lookup in NLP/LLMs is `E[token_ids]`.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
