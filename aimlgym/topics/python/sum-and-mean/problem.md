# PY-11 · Sum and Mean of a List

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-10 Greeting Formatter

Read the lesson first: [article.md](article.md)

## Task

Write `sum_and_mean(nums)` returning a tuple `(total, mean)`.

**Requirements**
* `total` is the sum of the numbers (an `int` if all inputs are ints).
* `mean` is `total / len(nums)` as a `float`.
* For an empty list return `(0, None)`.
* Use a loop (do not call `sum` or `statistics`). Do not modify the input list.

**Constraints:** 0 ≤ `len(nums)` ≤ 10⁵; elements are ints or floats.

**Examples**
```python
sum_and_mean([2, 4, 9])     # (15, 5.0)
sum_and_mean([])            # (0, None)   — mean undefined for empty data
sum_and_mean([-1.5, 1.5])   # (0.0, 0.0)
```

## Hints

<details><summary>Hint 1</summary>

Loop with `for x in nums:` and update `total += x`.

</details>

<details><summary>Hint 2</summary>

Check `if len(nums) == 0:` (or `if not nums:`) before dividing.

</details>

<details><summary>Hint 3</summary>

Use true division `/` so the mean is a float.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_empty` | Return `(0, None)` before dividing; dividing by zero raises an error. |
| `test_mean_is_true_division` | Use `/` not `//`. |
| `test_floats_tolerance` | Floats are compared with a tolerance of 1e-9; make sure you return numbers, not strings. |
| `test_single` | With one element the mean equals that element as a float. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

One pass over the data maintains two accumulators: the running total and the count. Counting
inside the loop means the function would also work for any iterable (not only lists). The empty
case is detected via `count == 0` before division, avoiding `ZeroDivisionError`.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
