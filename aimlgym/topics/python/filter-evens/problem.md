# PY-12 · Filter Even Numbers

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-11 Sum and Mean of a List

Read the lesson first: [article.md](article.md)

## Task

Write `evens(nums)` that returns a new list containing only the even integers of `nums`, in
their original order.

**Constraints:** `nums` is a list of 0–10⁵ integers (may be negative). Do not modify `nums`.

**Examples**
```python
evens([5, -4, 0, 7, 12])   # [-4, 0, 12]  — 0 and negatives handled
evens([1, 3, 5])           # []           — nothing passes the test
```

## Hints

<details><summary>Hint 1</summary>

A number is even when `x % 2 == 0`.

</details>

<details><summary>Hint 2</summary>

A list comprehension can include `if` at the end.

</details>

<details><summary>Hint 3</summary>

`return [x for x in nums if x % 2 == 0]`

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_mixed` | Is 0 included? It is even. |
| `test_all_even_order` | Do not sort — keep the original order. |
| `test_not_modified` | Build a new list; don't call `.remove()` on the input. |
| `test_duplicates_kept` | Filtering keeps duplicates; don't convert to a set. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A conditional list comprehension iterates once, keeps elements whose remainder modulo 2 is zero,
and returns a new list, so the input is untouched and order is preserved. Python's `%` makes
the test correct for negative numbers.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
