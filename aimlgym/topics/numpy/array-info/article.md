# The ndarray

## Learning outcomes

After this lesson you can:

- Create ndarrays from nested lists with a chosen dtype
- Read shape, ndim, size and dtype
- Explain why ragged lists cannot become numeric arrays

## Intuition
A NumPy array is a rectangular grid of numbers that all share one type. Because every element
has the same size and the grid is regular, NumPy can store the data in one contiguous block and
run fast compiled loops over it.

## Precise explanation
* `np.array(rows, dtype=float)` builds an array; `dtype` fixes the element type
  (`float64`, `int64`, `bool`, …).
* `a.shape` — tuple of lengths per axis; `a.ndim` — number of axes (`len(a.shape)`);
  `a.size` — total elements (product of the shape); `a.dtype` — element type.
* A 1-D array has shape `(n,)` (note the comma); a 2-D array `(rows, cols)`.
* Ragged nested lists (rows of different lengths) cannot form a numeric grid. Since NumPy 1.24
  `np.array([[1, 2], [3]])` raises `ValueError` unless you explicitly ask for `dtype=object`.

```python
>>> a = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)
>>> a.shape, a.ndim, a.size, a.dtype
((2, 3), 2, 6, dtype('float64'))
```

## Worked example
`np.array([7, 8, 9])` → shape `(3,)`, ndim 1, size 3, dtype int64 (on most 64-bit platforms).
`np.array([[7], [8], [9]])` → shape `(3, 1)` — a column, ndim 2.

## Common mistakes
* Confusing `(3,)` and `(3, 1)` — they broadcast differently (NP-07).
* Expecting `len(a)` to be the total size (it is the length of the first axis).
* Mixing ints and strings in one list → NumPy picks a string dtype.

## Why this matters
Every ML dataset is an array of shape `(n_samples, n_features)`; knowing its shape and dtype is
the first debugging step for almost every error message in later topics.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
