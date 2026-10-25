# PY-18 · Gradebook Aggregation

**Topic:** Python · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** PY-17 Functions as Values

Read the lesson first: [article.md](article.md)

## Task

Write `gradebook(records)` where `records` is a list of `(name, score)` tuples.

Return a list of `(name, average, count)` tuples:
* `average` = mean score rounded to 2 decimals (`round(x, 2)`), `count` = number of scores;
* sorted by average **descending**, ties broken by name **ascending**.

Ignore records whose score is not in `[0, 100]` (they do not count).

**Constraints:** ≤ 10⁵ records; names are non-empty strings; scores are ints/floats.

**Examples**
```python
gradebook([("ann", 90), ("bob", 70), ("ann", 80), ("cy", 85)])
# [('ann', 85.0, 2), ('cy', 85.0, 1), ('bob', 70.0, 1)]  — tie on 85 broken by name
gradebook([("x", 101), ("x", 50)])
# [('x', 50.0, 1)]  — 101 is out of range and ignored
```

## Hints

<details><summary>Hint 1</summary>

Skip a record unless `0 <= score <= 100`.

</details>

<details><summary>Hint 2</summary>

`groups.setdefault(name, []).append(score)` groups scores.

</details>

<details><summary>Hint 3</summary>

Sort with `key=lambda r: (-r[1], r[0])` after computing (name, avg, count).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Ties on average must be ordered by name ascending; reverse=True breaks this. |
| `test_rounding` | Average raw scores, then round once with round(x, 2). |
| `test_boundaries_included` | 0 and 100 are valid scores (inclusive range). |
| `test_only_invalid` | A name with no valid scores should not appear. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Invalid scores are filtered while grouping, so names that only have invalid scores never appear.
Averages are computed from raw scores and rounded once. The tuple sort key `(-average, name)`
gives descending averages with ascending-name tie-breaks in a single stable sort.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
