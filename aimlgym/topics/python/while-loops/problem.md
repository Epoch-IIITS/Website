# PY-08 · While Loops: Read Until Done

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-07 Conditionals: Letter Grades

Read the lesson first: [article.md](article.md)

## Task

Read integers, one per line, until a line equal to `done` (ignore surrounding spaces). Then print
one line:

```
count=<how many numbers> total=<their sum> max=<the largest>
```
If `done` is the first line, print `count=0 total=0 max=None`. Numbers may be negative.

## Hints

<details><summary>Hint 1</summary>

Use `while True:` and read `line = input().strip()` at the top of the loop.

</details>

<details><summary>Hint 2</summary>

`if line == "done": break` must come before `int(line)`.

</details>

<details><summary>Hint 3</summary>

Update the maximum with `if largest is None or x > largest: largest = x`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_negatives` | Start `largest` at `None`, not 0, so negative maxima work. |
| `test_spaces_around_done` | Strip each line before comparing it with `done`. |
| `test_stops_at_done` | Break as soon as you see `done`; ignore anything after it. |
| `test_empty` | If `done` comes first, print the initial values: 0, 0 and None. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The loop has no natural end, so `while True` with a `break` on the sentinel is clearest. Three
accumulators are updated per number; starting the maximum at `None` makes the first number win
regardless of sign, and lets the empty case print `None`.

## References

- [The Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html) — Python Software Foundation (`S042`)
