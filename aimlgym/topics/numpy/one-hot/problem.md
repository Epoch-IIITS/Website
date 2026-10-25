# NP-13 · One-Hot Encoding

**Topic:** NumPy · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** NP-09 Fancy Indexing and Gather

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `one_hot(labels, num_classes=None)` → float array `(n, K)`. Default `K = max(labels) + 1`.
  Raise `ValueError` for empty labels, negative labels, non-integer labels, or labels `>= K`.
* `from_one_hot(Y)` → integer label array via argmax; raise `ValueError` unless every row has
  exactly one 1 and the rest zeros.

**Examples**
```python
one_hot([2, 0, 1])               # [[0,0,1],[1,0,0],[0,1,0]]
one_hot([1], num_classes=4)      # [[0,1,0,0]]
from_one_hot(one_hot([3, 1, 3])) # array([3, 1, 3])
```

## Hints

<details><summary>Hint 1</summary>

`labels = np.asarray(labels)`; check `np.issubdtype(labels.dtype, np.integer)`.

</details>

<details><summary>Hint 2</summary>

`Y = np.zeros((n, K)); Y[np.arange(n), labels] = 1.0`.

</details>

<details><summary>Hint 3</summary>

Valid one-hot rows: all entries in {0, 1} and each row sums to 1.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_basic` | Use Y[np.arange(n), labels] = 1, not Y[:, labels] = 1. |
| `test_negative` | Negative indices silently wrap around in NumPy — validate labels >= 0. |
| `test_bad_decode` | Check each row has exactly one 1 and only 0/1 entries. |
| `test_float_labels` | Reject non-integer label dtypes. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

After validating type and range, paired fancy indexing writes exactly one 1 per row. Decoding
checks the matrix really is one-hot (only zeros/ones, one 1 per row) and returns the argmax.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
