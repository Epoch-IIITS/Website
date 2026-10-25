# Slicing, Views and Copies

## Learning outcomes

After this lesson you can:

- Slice 2-D arrays with start:stop:step
- Distinguish views from copies
- Validate slice bounds

## Intuition
Slicing cuts a rectangle out of a grid. In NumPy that rectangle is usually a **view**: a window
onto the same memory. Changing the view changes the original — powerful, but surprising.

## Precise explanation
* `a[r0:r1, c0:c1]` selects rows `r0..r1-1` and columns `c0..c1-1`.
* Steps: `a[::2, ::2]` takes every other row and column.
* Basic slicing returns a **view** (`np.shares_memory(view, a)` is True). Use `.copy()` to get
  independent data.
* Out-of-range slice ends are silently clipped (`a[0:100]` on 5 rows gives 5 rows) — validate if
  you need exact sizes.
* Negative indices count from the end: `a[-1]` is the last row; `a[1:-1, 1:-1]` is the interior.

## Worked example
```python
a = np.arange(16).reshape(4, 4)
a[1:3, 1:3]     # [[ 5,  6], [ 9, 10]]
a[::2, ::2]     # [[ 0,  2], [ 8, 10]]
a.sum() - a[1:-1, 1:-1].sum()   # border sum = 120 - 30 = 90
```

## Common mistakes
* `a[1:3][1:3]` — slices rows twice instead of rows then columns.
* Modifying a crop and accidentally editing the source image.
* Off-by-one: stop indices are exclusive.

## Why this matters
Cropping image patches (CV), selecting time windows and mini-batches are all slicing; view
semantics explain many "my data changed by itself" bugs.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
