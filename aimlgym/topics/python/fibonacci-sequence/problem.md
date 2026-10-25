# PY-14 · Fibonacci Sequence

**Topic:** Python · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** PY-13 Vowel Counter

Read the lesson first: [article.md](article.md)

## Task

Write `fibonacci(n)` returning a list of the first `n` Fibonacci numbers, starting `0, 1, ...`.

**Requirements:** iterative (O(n) time); `n = 0` returns `[]`; a negative `n` also returns `[]` (raising errors for bad input comes later, in PY-19).

**Constraints:** 0 ≤ n ≤ 10⁴.

**Examples**
```python
fibonacci(6)   # [0, 1, 1, 2, 3, 5]
fibonacci(1)   # [0]
fibonacci(0)   # []
```

## Hints

<details><summary>Hint 1</summary>

Keep two variables `a, b = 0, 1`.

</details>

<details><summary>Hint 2</summary>

Each iteration: append `a`, then `a, b = b, a + b`.

</details>

<details><summary>Hint 3</summary>

Loop exactly `n` times with `for _ in range(n)`; `range(n)` is empty when n ≤ 0, so no special case is needed.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_one` | The sequence starts with 0, so fibonacci(1) is [0]. |
| `test_recurrence_holds` | Check simultaneous assignment `a, b = b, a + b`. |
| `test_fast_large` | Avoid recursion; an O(n) loop finishes instantly. |
| `test_negative` | A negative n should give an empty list; `range(n)` already does this. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Two variables hold the current and next Fibonacci numbers. Simultaneous tuple assignment advances
the window by one step. Because the loop runs exactly n times, the n = 0 and n = 1 cases need no
special handling.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
