# PY-06 · Strings: Indexing, Slicing and Methods

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-05 Arithmetic Operators

Read the lesson first: [article.md](article.md)

## Task

Read one word (strip surrounding spaces). Print exactly these seven lines for it:

```
Length: <number of characters>
First: <first character>
Last: <last character>
First three: <first three characters, or the whole word if shorter>
Reversed: <the word backwards>
Upper: <the word in upper case>
Contains 'th': <True or False>
```

**Example** for `Python`:
```
Length: 6
First: P
Last: n
First three: Pyt
Reversed: nohtyP
Upper: PYTHON
Contains 'th': True
```
The word has at least one character. The `'th'` test is case-sensitive.

## Hints

<details><summary>Hint 1</summary>

`word[0]` is the first character and `word[-1]` the last.

</details>

<details><summary>Hint 2</summary>

`word[:3]` never fails even if the word is shorter; `word[::-1]` reverses it.

</details>

<details><summary>Hint 3</summary>

`'th' in word` gives True or False; print it inside an f-string.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_short_word` | Use a slice `word[:3]`; slices stop at the end of the string without errors. |
| `test_strip` | Strip the input before measuring its length. |
| `test_contains_false` | The test is case-sensitive: use `'th' in word` on the original word. |
| `test_single_character` | Use `word[-1]` for the last character and `word[::-1]` to reverse. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Indexing picks single characters, slicing with omitted bounds handles short words safely, and a
negative step reverses the string. `upper()` returns a new string and `in` returns a bool.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — Python Software Foundation (`S049`)
