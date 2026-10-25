# NP-04 · Boolean Masks

**Topic:** NumPy · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** NP-03 Slicing a Sub-grid

Read the lesson first: [article.md](article.md)

## Task

Implement without Python loops:
* `in_range(a, lo, hi)` → 1-D array of the elements with `lo <= x <= hi` (in original order,
  row-major for 2-D).
* `count_above(a, t)` → number (Python `int`) of elements strictly greater than `t`.
* `cap(a, t)` → new array equal to `a` but with every element `> t` replaced by `t`; `a` must not
  change.

**Examples**
```python
a = np.array([4, -1, 9, 3, 12])
in_range(a, 0, 9)   # array([4, 9, 3])
count_above(a, 5)   # 2
cap(a, 5)           # array([ 4, -1,  5,  3,  5])
```

## Hints

<details><summary>Hint 1</summary>

`mask = (a >= lo) & (a <= hi)` then `a[mask]`.

</details>

<details><summary>Hint 2</summary>

`int((a > t).sum())`.

</details>

<details><summary>Hint 3</summary>

`np.where(a > t, t, a)` returns a new array.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_in_range` | Use & with parentheses: (a >= lo) & (a <= hi). |
| `test_count_strict` | Strictly greater: a > t. |
| `test_cap_no_mutation` | Don't assign into a; use np.where or np.minimum to build a new array. |
| `test_count` | Convert the result to a Python int. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Comparisons produce masks; `&` combines them element-wise and boolean indexing extracts the
selected elements. Summing a mask counts Trues. `np.where` constructs a fresh array, leaving the
input untouched.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
