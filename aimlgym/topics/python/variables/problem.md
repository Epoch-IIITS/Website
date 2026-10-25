# PY-02 · Variables and f-strings

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-01 Hello, print()

Read the lesson first: [article.md](article.md)

## Task

Write a program that creates these variables with exactly these values and types:

| Variable | Value |
|---|---|
| `name` | `"Ada"` |
| `age` | `19` |
| `height_m` | `1.68` |
| `is_student` | `True` |
| `next_age` | `age + 1` (compute it; do not type 20) |

Then print exactly four lines using f-strings:

```
Name: Ada
Age next year: 20
Height: 1.68 m
Student: True
```

The tests read your variables after the program runs and compare its output.

## Hints

<details><summary>Hint 1</summary>

Numbers are written without quotes: `age = 19`, `height_m = 1.68`.

</details>

<details><summary>Hint 2</summary>

`True` has a capital T and no quotes; `next_age = age + 1`.

</details>

<details><summary>Hint 3</summary>

`print(f"Age next year: {next_age}")` inserts the value into the text.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_age_is_int` | Write `age = 19` without quotes; `"19"` is a string. |
| `test_height_is_float` | Use `1.68` (a float), not `"1.68"`. |
| `test_is_student_bool` | Use the keyword `True` (capital T, no quotes). |
| `test_next_age` | Compute `next_age = age + 1` after creating `age`. |
| `test_output` | Your printed lines must match the expected output exactly: check each label, the ` m` after the height, and that you used f-strings with braces around the variable names. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Four assignments create the variables with the requested types; `next_age` is computed from
`age`, so changing `age` and re-running the program would update it. Each f-string inserts one
variable into a fixed label.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [The Python Tutorial: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html) — Python Software Foundation (`S041`)
