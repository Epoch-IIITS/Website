# PY-04 · Reading Input

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-03 Types and Conversion

Read the lesson first: [article.md](article.md)

## Task

Read two lines from standard input:
1. a name (it may have spaces around it — remove them with `strip()`),
2. a birth year (an integer).

Print exactly two lines:
```
Hello, <name>!
In 2030 you will turn <2030 - year>.
```

Call `input()` **without** a prompt.

**Example**
```
input:  Ada
        2006
output: Hello, Ada!
        In 2030 you will turn 24.
```

## Hints

<details><summary>Hint 1</summary>

`name = input().strip()` removes surrounding spaces.

</details>

<details><summary>Hint 2</summary>

`year = int(input())` reads the second line as a number.

</details>

<details><summary>Hint 3</summary>

Compute `2030 - year` inside an f-string.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_strips_name` | Call `.strip()` on the name you read. |
| `test_year_with_spaces` | Convert the second line with `int(...)` and subtract it from 2030. |
| `test_no_prompt_text` | Do not pass a prompt to `input()`; it is printed as part of your output. |
| `test_example` | Check punctuation: `Hello, Ada!` and a full stop after the age. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The first `input()` reads the name and `strip()` removes stray spaces. The second line is
converted to an `int` so that subtraction works. Both results are printed with f-strings.

## References

- [The Python Tutorial: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html) — Python Software Foundation (`S041`)
- [Built-in Functions](https://docs.python.org/3/library/functions.html) — Python Software Foundation (`S048`)
