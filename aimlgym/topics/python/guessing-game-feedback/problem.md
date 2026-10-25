# PY-22 · Guessing Game Feedback

**Topic:** Python · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** PY-21 Safe Division with Exceptions

Read the lesson first: [article.md](article.md)

## Task

Write `guess_feedback(target, guesses, max_attempts=7)` returning a dict
`{"feedback": list[str], "attempts": int, "won": bool}`.

**Rules**
* Process guesses in order, at most `max_attempts` of them.
* For each processed guess append `"too low"`, `"too high"` or `"correct"`.
* Stop immediately after `"correct"`.
* `attempts` = number of guesses processed; `won` = whether `"correct"` occurred.
* Raise `ValueError` if `max_attempts < 1`.

**Constraints:** ints; `len(guesses)` ≤ 1000.

**Examples**
```python
guess_feedback(42, [50, 25, 42, 10])
# {'feedback': ['too high', 'too low', 'correct'], 'attempts': 3, 'won': True}
guess_feedback(5, [1, 2, 3], max_attempts=2)
# {'feedback': ['too low', 'too low'], 'attempts': 2, 'won': False}   — limit reached
```

## Hints

<details><summary>Hint 1</summary>

Loop over `guesses[:max_attempts]`.

</details>

<details><summary>Hint 2</summary>

Compare with `<`, `>`, `==` and append the right string.

</details>

<details><summary>Hint 3</summary>

Set `won = True` and `break` on a correct guess; attempts = len(feedback).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_win` | Stop the loop with `break` after a correct guess. |
| `test_win_on_last_allowed` | Check your attempt-limit comparison: max_attempts guesses are allowed, not max_attempts-1. |
| `test_correct_after_limit_ignored` | Only the first max_attempts guesses may be processed. |
| `test_bad_limit` | Validate max_attempts before looping. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Slicing `guesses[:max_attempts]` enforces the attempt budget up front. Each guess produces one
feedback string; on a correct guess the flag is set and the loop breaks, so later guesses are
never processed. Because exactly one string is appended per processed guess, `attempts` is just
the length of the feedback list.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
