# Regular Expressions for Text

## Learning outcomes

After this lesson you can:

- Write patterns with character classes, quantifiers and anchors
- Use re.findall, re.sub and re.fullmatch
- Capture parts of a match with named groups
- Compare a regex with the equivalent character loop

## Intuition
A regular expression (regex) is a tiny language for describing text patterns: "one or more
digits", "a word starting with #", "a date like 2026-10-24". Python's `re` module searches,
extracts and replaces such patterns, replacing many lines of character-by-character loops.

## Precise explanation
Always write patterns as **raw strings** (`r"..."`) so backslashes reach `re` unchanged.

| Pattern | Matches |
|---|---|
| `a`, `cat` | those exact characters |
| `.` | any character except newline |
| `[abc]`, `[a-z0-9]`, `[^0-9]` | one character from a set / not from a set |
| `\d`, `\w`, `\s` | digit, word character (letter, digit, `_`), whitespace |
| `\D`, `\W`, `\S` | the opposites |
| `x*`, `x+`, `x?`, `x{2,4}` | 0+, 1+, 0 or 1, 2–4 repetitions of `x` |
| `^`, `$`, `\b` | start, end, word boundary |
| `(...)`, `(?P<name>...)`, `(?:...)` | capturing group, named group, non-capturing group |
| `a|b` | either |

* `re.findall(p, s)` → list of all matches (or of group values if the pattern has one group).
* `re.sub(p, repl, s)` → replace every match.
* `re.fullmatch(p, s)` → a match object only if the **whole** string matches, else `None`;
  `m.group("name")` reads a named group.
* Quantifiers are **greedy** (take as much as possible); add `?` (`.*?`) for the shortest match.

## Worked example
```python
re.sub(r"\s+", " ", "a   b\t\nc")              # 'a b c'
re.findall(r"-?\d+(?:\.\d+)?", "x=-3.5, y=2")   # ['-3.5', '2']
m = re.fullmatch(r"(?P<y>\d{4})-(?P<m>\d\d)", "2026-10")
m.group("y")                                  # '2026'
```

## Common mistakes
* Forgetting the `r` prefix: `"\b"` is a backspace character, `r"\b"` is a word boundary.
* Using `re.match` (anchored only at the start) when you meant `re.fullmatch`.
* A group inside a `findall` pattern changes what is returned; use `(?:...)` when you only need
  grouping.
* Writing one giant pattern instead of several small, tested ones.

## Why this matters
Tokenisers (NL-02), log parsers, data cleaning and parsing model output
(AG-02) all use regular expressions.

## References

- [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) — Python Software Foundation (A.M. Kuchling) (`S059`)
- [re — Regular expression operations](https://docs.python.org/3/library/re.html) — Python Software Foundation (`S060`)
