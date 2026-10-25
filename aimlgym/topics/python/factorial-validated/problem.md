# PY-19 · Validated Factorial

**Topic:** Python · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** PY-18 Gradebook Aggregation

Read the lesson first: [article.md](article.md)

## Task

Write `factorial(n)`.

**Requirements**
* Return $n!$ as an `int` for integers $n \ge 0$ (with $0! = 1$). Use a loop, not `math.factorial`.
* Raise `TypeError` if `n` is not an `int`, or is a `bool`.
* Raise `ValueError` if `n < 0`.

**Constraints:** 0 ≤ n ≤ 1000 for valid input.

**Examples**
```python
factorial(5)     # 120
factorial(0)     # 1      — empty product
factorial(-2)    # raises ValueError
factorial(3.0)   # raises TypeError — floats are rejected even if whole
```

## Hints

<details><summary>Hint 1</summary>

Check the type first: `isinstance(n, bool) or not isinstance(n, int)`.

</details>

<details><summary>Hint 2</summary>

Then check `n < 0` and raise `ValueError`.

</details>

<details><summary>Hint 3</summary>

Start `result = 1` and multiply by `k` for `k in range(2, n + 1)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_zero_and_one` | 0! is defined as 1; make sure your loop handles n = 0. |
| `test_float` | Use isinstance(n, int); 3.0 is a float even though it equals 3. |
| `test_bool` | bool is a subclass of int — check for it explicitly. |
| `test_negative` | Raise ValueError (not return) when n < 0. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Type validation comes before value validation so that comparing `n < 0` is never attempted on,
say, a string. `bool` is rejected explicitly because it is a subclass of `int`. The loop starts
at 2 because multiplying by 1 changes nothing; for n = 0 or 1 the loop body never runs and the
empty product 1 is returned.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
