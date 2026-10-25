# Reading Input

## Learning outcomes

After this lesson you can:

- Read a line of text with input()
- Remember that input() always returns a str
- Clean input with strip() and convert it to a number

## Intuition
`print` sends text out; `input` brings text in. When a program reaches `input()` it waits for
one line from the keyboard (or from whatever is connected to *standard input*, such as a file or
an automatic grader) and gives it to you as a string.

## Precise explanation
```python
name = input()                 # one line, without the trailing newline, always a str
year = int(input())            # convert when you need a number
city = input("City? ")         # an optional prompt is printed first (not used in graded tasks)
```
* `input()` returns a `str`, even if the user typed digits. `input() + 1` is a `TypeError`.
* `text.strip()` removes spaces, tabs and newlines from both ends. `int()` and `float()`
  already ignore surrounding whitespace, but names and words do not.
* Each call reads the **next** line. If there is no line left, Python raises `EOFError`.

## Worked example
Input:
```
  Grace
1990
```
```python
name = input().strip()     # "Grace"
birth_year = int(input())  # 1990
print(f"Hello, {name}! In 2030 you will turn {2030 - birth_year}.")
```
Output: `Hello, Grace! In 2030 you will turn 40.`

## Common mistakes
* Forgetting `int(...)`, then subtracting a string.
* Printing a prompt in graded tasks: the prompt becomes part of your output and breaks exact
  comparisons. Tests in this site supply input directly, so call `input()` with no prompt.
* Calling `input()` more times than there are lines.

## Why this matters
Reading and validating outside data is where most real programs start: command-line tools,
web forms (FA-01 later) and dataset files all deliver text you must parse.

## References

- [The Python Tutorial: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html) — Python Software Foundation (`S041`)
- [Built-in Functions](https://docs.python.org/3/library/functions.html) — Python Software Foundation (`S048`)
