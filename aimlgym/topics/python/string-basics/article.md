# Strings: Indexing, Slicing and Methods

## Learning outcomes

After this lesson you can:

- Index characters with positive and negative indices
- Slice substrings, including with a step
- Use len(), upper(), lower(), strip(), replace() and the in operator

## Intuition
A string is a row of characters with numbered positions, starting at 0. You can point at one
position, cut out a piece, or ask the string to produce a changed copy of itself.

## Precise explanation
```
 P   y   t   h   o   n
 0   1   2   3   4   5     positive index
-6  -5  -4  -3  -2  -1     negative index (counts from the end)
```
* `word[0]` → `"P"`, `word[-1]` → `"n"`. An index past the end raises `IndexError`.
* **Slicing** `word[start:stop]` takes positions `start` up to but **not including** `stop`:
  `word[0:3]` → `"Pyt"`; omitted ends mean "from the start"/"to the end": `word[:3]`, `word[3:]`.
  Slices never raise errors: `"ab"[:3]` → `"ab"`.
* A third number is the step: `word[::2]` → `"Pto"`, `word[::-1]` → `"nohtyP"` (reversed).
* `len(word)` → 6. `"th" in word` → `True` (substring test).
* Methods return **new** strings: `word.upper()`, `word.lower()`, `"  x ".strip()`,
  `"a-b".replace("-", "+")`, `"py".title()`. Strings are immutable: `word[0] = "J"` is an error.

## Worked example
`word = "Python"` → `len(word)` 6, `word[0]` P, `word[-1]` n, `word[:3]` Pyt,
`word[::-1]` nohtyP, `word.upper()` PYTHON, `"th" in word` True.

## Common mistakes
* Off-by-one: the last character is `word[len(word) - 1]`, not `word[len(word)]`.
* Expecting `word.upper()` to change `word`; store the result if you need it.
* Confusing `word[1:3]` (2 characters) with "characters 1 to 3 inclusive".

## Why this matters
Text cleaning in NLP, parsing HTTP requests and file names, and reading model output all rely on
slicing and string methods.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — Python Software Foundation (`S049`)
