# PY-05 · Arithmetic Operators

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-04 Reading Input

Read the lesson first: [article.md](article.md)

## Task

Read one non-negative integer: a number of seconds. Print two lines:

1. The duration as `H:MM:SS` — hours without padding, minutes and seconds with two digits.
2. The duration in minutes with exactly two decimals, followed by ` minutes`.

**Example**
```
input:  3725
output: 1:02:05
        62.08 minutes
```
Hours may exceed 24 (`90000` → `25:00:00`).

## Hints

<details><summary>Hint 1</summary>

`hours = total // 3600` and `rest = total % 3600`.

</details>

<details><summary>Hint 2</summary>

`minutes = rest // 60`, `seconds = rest % 60`.

</details>

<details><summary>Hint 3</summary>

`print(f"{hours}:{minutes:02d}:{seconds:02d}")` and `print(f"{total / 60:.2f} minutes")`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_padding` | Pad minutes and seconds with `:02d`. |
| `test_zero` | Use `:.2f` so zero is printed as `0.00`. |
| `test_end_of_day` | Take the remainder after removing hours before computing minutes. |
| `test_more_than_a_day` | Do not wrap hours at 24; just use `total // 3600`. |
| `test_minutes_two_decimals` | Minutes use true division `/`, then `:.2f` formatting. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Floor division gives the number of whole hours; the remainder holds what is left, which is split
again into minutes and seconds. `:02d` pads minutes and seconds to two digits and `:.2f` shows
the true-division result with two decimals.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — Python Software Foundation (`S049`)
