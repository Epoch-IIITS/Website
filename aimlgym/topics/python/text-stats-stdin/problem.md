# PY-24 · Text Statistics from stdin

**Topic:** Python · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** PY-23 Files, CSV and JSON

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `text_stats(text)` → tuple `(lines, words, chars)` where
   `lines = len(text.splitlines())`, `words = len(text.split())`, `chars = len(text)`.
2. `main()` → reads **all** of stdin, prints exactly one line
   `lines=<L> words=<W> chars=<C>` and returns `None`.

Guard the call with `if __name__ == "__main__":`.

**stdin/stdout format**
```
input  (stdin):  to be\nor not\n
output (stdout): lines=2 words=4 chars=13
```

**Examples**
```python
text_stats("to be\nor not\n")   # (2, 4, 13)
text_stats("")                  # (0, 0, 0)  — empty input
text_stats("one line no newline")  # (1, 4, 19)
```

## Hints

<details><summary>Hint 1</summary>

`len(text.splitlines())`, `len(text.split())`, `len(text)`.

</details>

<details><summary>Hint 2</summary>

In `main`, `text = sys.stdin.read()`.

</details>

<details><summary>Hint 3</summary>

Use an f-string with exactly one space between fields.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_no_trailing_newline` | Count lines with splitlines(), not count('\n'). |
| `test_main_output` | Print exactly `lines=L words=W chars=C` with single spaces. |
| `test_as_script` | Add `if __name__ == "__main__": main()` at the bottom. |
| `test_blank_lines` | Blank lines still count as lines; words come from split(). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

All counting lives in `text_stats`, which is pure and easy to test. `main` is three lines of I/O:
read everything, compute, print once. `splitlines` handles a missing final newline correctly,
which `count("\n")` would not.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
