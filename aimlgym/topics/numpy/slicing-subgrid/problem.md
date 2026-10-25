# NP-03 · Slicing a Sub-grid

**Topic:** NumPy · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** NP-01 Create an Array and Inspect It

Read the lesson first: [article.md](article.md)

## Task

Implement for a 2-D array `a`:
* `crop(a, top, left, h, w)` → a **copy** of the `h × w` block starting at `(top, left)`;
  raise `ValueError` if the block does not fit inside `a` or `h`, `w` < 1 or top/left < 0.
* `every_other(a)` → `a[::2, ::2]` (a view is fine).
* `border_sum(a)` → sum of the elements on the outer border (for 1 or 2 rows/cols every element
  is on the border).

**Examples**
```python
a = np.arange(16).reshape(4, 4)
crop(a, 1, 1, 2, 2)   # array([[ 5,  6], [ 9, 10]])
every_other(a)        # array([[ 0,  2], [ 8, 10]])
border_sum(a)         # 90
```

## Hints

<details><summary>Hint 1</summary>

Check `top + h <= a.shape[0]` and `left + w <= a.shape[1]`.

</details>

<details><summary>Hint 2</summary>

`a[top:top+h, left:left+w].copy()`.

</details>

<details><summary>Hint 3</summary>

Border = total − interior `a[1:-1, 1:-1].sum()` (the interior is empty for small arrays).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_crop_is_copy` | Return `.copy()` of the slice so modifying the crop doesn't modify the input. |
| `test_crop_out_of_bounds` | Slicing silently clips; check the bounds yourself. |
| `test_border_small` | For 1×1 or 2×2 arrays the interior is empty, so the border is everything. |
| `test_crop` | Use a[top:top+h, left:left+w] (one bracket, comma between axes). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`crop` validates bounds (slicing would silently clip) and returns a copy so callers can modify it
safely. `every_other` uses steps. `border_sum` subtracts the interior from the total; for arrays
with fewer than three rows or columns the interior slice is empty and sums to 0.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
