# NP-01 · Create an Array and Inspect It

**Topic:** NumPy · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** PY-20 Matrix Transpose with Validation

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `to_array(rows, dtype=float)` → `np.ndarray` built from nested lists with the given dtype.
  Raise `ValueError` if `rows` is ragged (rows of different lengths).
* `describe(a)` → dict `{"shape": tuple, "ndim": int, "size": int, "dtype": str}` where
  `dtype` is `str(a.dtype)`.

**Examples**
```python
a = to_array([[1, 2, 3], [4, 5, 6]])
describe(a)   # {'shape': (2, 3), 'ndim': 2, 'size': 6, 'dtype': 'float64'}
describe(to_array([1, 2], dtype=int))['shape']   # (2,)
to_array([[1, 2], [3]])   # raises ValueError
```

## Hints

<details><summary>Hint 1</summary>

`np.array(rows, dtype=dtype)` raises ValueError for ragged numeric lists in NumPy ≥ 1.24.

</details>

<details><summary>Hint 2</summary>

You may also check row lengths yourself for clarity.

</details>

<details><summary>Hint 3</summary>

Use `tuple(a.shape)`, `int(a.ndim)`, `int(a.size)`, `str(a.dtype)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_2d` | Pass dtype to np.array and return shape as a tuple. |
| `test_ragged` | Raise ValueError for rows of different lengths. |
| `test_bool_dtype` | Return str(a.dtype), e.g. 'bool' or 'float64'. |
| `test_3d` | size is the product of the shape entries. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

An explicit row-length check gives a clear error message (NumPy would also raise). `describe`
converts NumPy's attributes into plain Python types so they compare cleanly in tests.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
