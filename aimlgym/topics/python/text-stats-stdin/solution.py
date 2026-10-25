r"""Reference solution for PY-24 Text Statistics from stdin.

All counting lives in `text_stats`, which is pure and easy to test. `main` is three lines of I/O:
read everything, compute, print once. `splitlines` handles a missing final newline correctly,
which `count("\n")` would not.
"""
import sys


def text_stats(text):
    return len(text.splitlines()), len(text.split()), len(text)


def main():
    text = sys.stdin.read()
    lines, words, chars = text_stats(text)
    print(f"lines={lines} words={words} chars={chars}")


if __name__ == "__main__":
    main()
