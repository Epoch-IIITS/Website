# PY-16 · Unique Words in Order

**Topic:** Python · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** PY-15 Importing the Standard Library

Read the lesson first: [article.md](article.md)

## Task

Write `unique_words(sentence)` that returns the list of distinct words in order of first
appearance.

**Rules**
1. Split on whitespace with `str.split()`.
2. Normalise each token: strip characters in `string.punctuation` from both ends, then lowercase.
3. Discard tokens that are empty after stripping.
4. Keep the first occurrence of each normalised word.

**Constraints:** `len(sentence)` ≤ 10⁵.

**Examples**
```python
unique_words("The cat saw the CAT, then the dog.")
# ['the', 'cat', 'saw', 'then', 'dog']
unique_words("Don't stop -- don't!")
# ["don't", 'stop']   — inner apostrophe kept; '--' becomes empty and is dropped
```

## Hints

<details><summary>Hint 1</summary>

`token.strip(string.punctuation).lower()` normalises one token.

</details>

<details><summary>Hint 2</summary>

Skip a token if it is empty after normalising.

</details>

<details><summary>Hint 3</summary>

Use a `seen` set alongside an output list to keep order.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_order_not_sorted` | Don't sort; keep first-occurrence order. |
| `test_apostrophe_and_dash` | Strip punctuation only from the ends (str.strip), and drop empty tokens. |
| `test_multiple_spaces` | Use `split()` with no argument to handle tabs/newlines/multiple spaces. |
| `test_only_punctuation` | Tokens that are empty after stripping must not be added. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each token is normalised by stripping punctuation from its ends and lowercasing. The set gives
constant-time duplicate checks while the list records first-occurrence order. Empty tokens
(pure punctuation) are skipped by the `if word` condition.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
