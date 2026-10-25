# PY-21 · Safe Division with Exceptions

**Topic:** Python · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** PY-20 Matrix Transpose with Validation

Read the lesson first: [article.md](article.md)

## Task

Implement two functions.

1. `safe_divide(a, b)` → `a / b` as a float, or `None` if `b` is zero. Catch **only**
   `ZeroDivisionError`; any other error (e.g. `TypeError` for strings) must propagate.
2. `divide_pairs(pairs)` → `(results, failed)` where `results[i] = safe_divide(*pairs[i])` and
   `failed` is the sorted list of indices whose result is `None`.

**Constraints:** numbers are ints or floats; `len(pairs)` ≤ 10⁵.

**Examples**
```python
safe_divide(7, 2)          # 3.5
safe_divide(1, 0)          # None
safe_divide("6", 3)        # raises TypeError (not caught)
divide_pairs([(6, 3), (1, 0), (5, 2)])   # ([2.0, None, 2.5], [1])
```

## Hints

<details><summary>Hint 1</summary>

Wrap only the division in `try:` and catch `except ZeroDivisionError:`.

</details>

<details><summary>Hint 2</summary>

Use `enumerate(pairs)` to get each index.

</details>

<details><summary>Hint 3</summary>

Append the index to `failed` when the result `is None`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_type_error_propagates` | Catch only ZeroDivisionError; a bare except hides TypeError. |
| `test_zero_numerator_ok` | 0 / 5 is 0.0, a valid result — only a None result counts as failed. Use `is None`, not `not r`. |
| `test_pairs` | Use enumerate to record indices of failures. |
| `test_float_zero` | Plain Python raises ZeroDivisionError for 1.0/0.0 too. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`safe_divide` catches exactly one exception type, so programming errors such as dividing a
string still raise `TypeError`. `divide_pairs` reuses it, records `None` for failures and the
index of each failure. Indices come out sorted automatically because the loop visits them in order.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
