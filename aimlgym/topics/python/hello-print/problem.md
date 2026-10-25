# PY-01 · Hello, print()

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** none

Read the lesson first: [article.md](article.md)

## Task

Write a program that prints **exactly** these six lines (no extra spaces):

```
Hello, world!
Python is fun
2026-10-24
                         <- this line is empty
Loading...done
She said "hi"
```

**Requirements**
* Line 2 must come from one `print` call with three arguments: `"Python"`, `"is"`, `"fun"`.
* Line 3 must come from one `print` call with the arguments `"2026"`, `"10"`, `"24"` and `sep`.
* Line 5 must come from two `print` calls, the first using `end`.
* Line 6 contains double quotes, so write it with single quotes around it.

The tests run your file and compare everything it prints.

## Hints

<details><summary>Hint 1</summary>

`print("Python", "is", "fun")` already puts one space between the words.

</details>

<details><summary>Hint 2</summary>

`print()` with no arguments prints an empty line; `sep="-"` changes the separator.

</details>

<details><summary>Hint 3</summary>

`print("Loading", end="...")` then `print("done")`; finally `print('She said "hi"')`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_exact_output` | Compare your output with the six expected lines; look for extra spaces or missing lines. |
| `test_words_line` | Use one print with three arguments; print adds the spaces for you. |
| `test_date_with_sep` | Pass `sep="-"` so the parts are joined by dashes, not spaces. |
| `test_blank_line` | Line 4 must be empty: call `print()` with no arguments. |
| `test_end_joins_lines` | The first call needs `end="..."` so `done` continues the same line. |
| `test_quotes` | Wrap the last string in single quotes so it can contain double quotes. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each `print` call writes its arguments joined by `sep` and then writes `end`. Changing `sep`
produces the date, an empty call produces the blank line, and `end="..."` replaces the newline
so that `done` continues the fifth line. Single quotes let the last string contain double quotes.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [The Python Tutorial: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html) — Python Software Foundation (`S041`)
