# PY-07 · Conditionals: Letter Grades

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-06 Strings: Indexing, Slicing and Methods

Read the lesson first: [article.md](article.md)

## Task

Read one integer score. Print two lines.

Line 1 — the grade:
| Score | Output |
|---|---|
| below 0 or above 100 | `Invalid score` |
| 90–100 | `A` |
| 80–89 | `B` |
| 70–79 | `C` |
| 60–69 | `D` |
| 0–59 | `F` |

Line 2 — `Pass` if the score is valid and at least 60, `Fail` if it is valid and below 60, and
`Check the input` if it is invalid.

## Hints

<details><summary>Hint 1</summary>

Test the invalid case first: `if score < 0 or score > 100:`.

</details>

<details><summary>Hint 2</summary>

Then go from the highest band down with `elif score >= 90:`, `elif score >= 80:` ...

</details>

<details><summary>Hint 3</summary>

For line 2 use a second if/elif/else; `0 <= score <= 100` checks validity.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_boundaries_top` | Use `>=` so that exactly 90 is an A and 89 is a B. |
| `test_middle_bands` | Check the bands from highest to lowest with elif. |
| `test_invalid_high` | Handle scores above 100 before the A band. |
| `test_invalid_low` | Negative scores are invalid, not F. |
| `test_pass_boundary` | 60 passes; 59 fails. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Invalid scores are handled first so that later branches only see 0–100. The bands are tested from
highest to lowest, so each `elif` implicitly knows the score is below the previous threshold.
The second decision reuses a chained comparison for validity.

## References

- [The Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html) — Python Software Foundation (`S042`)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — Python Software Foundation (`S049`)
