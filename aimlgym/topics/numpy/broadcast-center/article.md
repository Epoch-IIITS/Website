# Broadcasting

## Learning outcomes

After this lesson you can:

- Apply NumPy's broadcasting rules
- Centre and scale features without loops
- Use np.newaxis / reshape to align shapes

## Intuition
Subtracting a per-column mean from every row should not need a loop: NumPy "stretches" the
smaller array across the larger one. That stretching is **broadcasting**, done without copying
memory.

## Precise explanation
Compare shapes from the **right**. Two dimensions are compatible if they are equal or one of
them is 1 (a missing leading dimension counts as 1). The result takes the larger size.
| X shape | other | result |
|---|---|---|
| (4, 3) | (3,) | (4, 3) — row vector stretched down |
| (4, 3) | (4, 1) | (4, 3) — column stretched across |
| (4, 3) | (4,) | **error** (3 vs 4) |

To scale row *i* by `w[i]` with `w.shape == (4,)`, reshape it to a column: `w[:, np.newaxis]`
(or `w[:, None]`, `w.reshape(-1, 1)`).

## Worked example
```python
X = np.array([[1., 2.], [3., 6.]])
X - X.mean(axis=0)            # [[-1, -2], [1, 2]]
X * np.array([10, 0.5])[:, None]   # [[10, 20], [1.5, 3]]
```

## Common mistakes
* Multiplying `(4, 3)` by `(4,)` and getting a shape error — reshape to `(4, 1)`.
* Accidental broadcasting: `(n,)` minus `(n, 1)` produces an `(n, n)` matrix silently!
* Dividing by a zero standard deviation for a constant column.

## Why this matters
Standardization (ML-08), adding bias vectors in neural layers (DL-04), and pairwise distances
(NP-11) are all broadcasting.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
