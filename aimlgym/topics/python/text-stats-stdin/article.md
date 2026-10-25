# Programs that Read Standard Input

## Learning outcomes

After this lesson you can:

- Read all of standard input
- Separate pure logic from I/O
- Format output exactly

## Intuition
Online judges and code runners such as Piston feed your program text on **standard input
(stdin)** and compare what it prints on **standard output (stdout)**. The trick to writing such
programs well is to keep the *logic* in a pure function you can test, and keep the *I/O* in a
tiny `main()`.

## Precise explanation
* `sys.stdin.read()` returns everything on stdin as one string (possibly empty).
* `text.splitlines()` splits on line boundaries without keeping `\n`. A trailing newline does
  not create an extra empty line: `"a\nb\n".splitlines() == ['a', 'b']`.
* Words: `text.split()` (whitespace-separated tokens).
* Characters: `len(text)` counts every character including spaces and newlines.
* The guard `if __name__ == "__main__": main()` runs `main` only when the file is executed as a
  script, not when it is imported by tests.

```python
def main():
    text = sys.stdin.read()
    lines, words, chars = text_stats(text)
    print(f"lines={lines} words={words} chars={chars}")
```

## Worked example
stdin = `"to be\nor not\n"` → splitlines → 2 lines; split → 4 words; len → 13 chars.
Output: `lines=2 words=4 chars=13`.

## Common mistakes
* `text.count("\n")` for lines — wrong when the last line has no trailing newline.
* Calling `input()` in a loop and crashing with `EOFError` at end of input.
* Printing extra spaces or a different label format — exact-match graders reject it.
* Putting `print` inside `text_stats`, which makes it hard to test.

## Why this matters
Separating computation from I/O is how all testable software is structured — the same idea
reappears when agents (AG topics) separate the "model" from the "tools".

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
