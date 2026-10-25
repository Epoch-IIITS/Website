# PY-10 · Greeting Formatter

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-09 For Loops and range: FizzBuzz

Read the lesson first: [article.md](article.md)

## Task

Write `greet(name="World")` that returns a greeting string.

**Requirements**
1. Remove leading and trailing whitespace from `name`.
2. If the cleaned name is empty, use `"World"`.
3. Convert the name to title case (`str.title()`).
4. Return exactly `"Hello, <Name>!"`. Do not print anything.

**Constraints:** `name` is a `str` of length 0–100.

**Return format:** a `str`.

**Examples**
```python
greet()                    # 'Hello, World!'   — default argument used
greet("  ada lovelace ")   # 'Hello, Ada Lovelace!' — stripped, then title-cased
greet("   ")               # 'Hello, World!'   — only spaces → empty after strip
```

## Hints

<details><summary>Hint 1</summary>

Start with `name = name.strip()`; remember strip returns a new string.

</details>

<details><summary>Hint 2</summary>

An empty string is falsy, so `if not name:` detects it.

</details>

<details><summary>Hint 3</summary>

Build the answer with `f"Hello, {name.title()}!"` and `return` it.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_returns_str_not_none` | You probably used `print` instead of `return`. |
| `test_strip_and_title` | Call `.strip()` before `.title()` and keep the result in a variable. |
| `test_only_spaces` | Check for emptiness *after* stripping, not before. |
| `test_already_capitalised` | `.title()` also lowercases the remaining letters — use it rather than `.capitalize()` on the first letter only. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The function normalises its input first (strip), handles the empty case by falling back to the
default, and only then formats. Doing validation before formatting keeps each step simple and
means the f-string always receives a clean, non-empty name. `str.title()` is applied inside the
f-string so the stored value stays as the user typed it (minus whitespace).

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
- [Learn Python - Interactive Course](https://aqemery.github.io/learn-python/) — aqemery (GitHub user) (`S005`)
