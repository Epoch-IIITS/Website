# Your First Program: print()

## Learning outcomes

After this lesson you can:

- Run a Python program that prints text
- Write string literals with single and double quotes
- Control print's separator and line ending with sep and end
- Write comments

## Intuition
A Python program is a text file of instructions that run from the top line to the bottom line.
The first instruction most people learn is `print`, which shows text on the screen (the
*standard output*). Everything you print here is checked by the tests, character by character.

## Precise explanation
```python
# A comment starts with # and is ignored by Python.
print("Hello, world!")        # text in double quotes is a *string*
print('Single quotes work too')
print("Python", "is", "fun")  # several values are joined with a space: Python is fun
print("2026", "10", "24", sep="-")   # sep replaces the space: 2026-10-24
print()                        # an empty line
print("Loading", end="...")   # end replaces the newline normally printed at the end
print("done")                  # continues on the same line: Loading...done
```
* A **string** is text between matching quotes. Use double quotes when the text contains a
  single quote (`"It's"`) and single quotes when it contains double quotes (`'She said "hi"'`).
* `print(a, b, c)` prints its arguments separated by `sep` (default `" "`) and then prints
  `end` (default `"\n"`, a newline).
* Python runs lines in order; a typo such as `Print(...)` stops the program with a `NameError`.

## Worked example
```python
print("Score", "10", sep=": ", end="!\n")
```
prints `Score: 10!` followed by a newline.

## Common mistakes
* Missing quotes: `print(Hello)` makes Python look for a variable called `Hello`.
* Mismatched quotes: `print("Hi')` is a `SyntaxError`.
* Extra spaces: `print("a ", "b")` prints `a  b` (two spaces) because `sep` adds one more.
* Forgetting that `end=""` removes the newline, so the next print continues on the same line.

## Why this matters
Every later program reports results through `print` or through return values. Getting output
exactly right is also how automatic graders and command-line tools communicate.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [The Python Tutorial: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html) — Python Software Foundation (`S041`)
