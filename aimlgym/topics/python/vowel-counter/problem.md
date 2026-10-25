# PY-13 · Vowel Counter

**Topic:** Python · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-12 Filter Even Numbers

Read the lesson first: [article.md](article.md)

## Task

Write `count_vowels(text)` returning `(total, counts)` where `counts` is a dict with exactly the
keys `'a','e','i','o','u'` mapped to how many times each occurs in `text` (case-insensitive), and
`total` is the sum of those counts.

**Constraints:** `text` is a `str` of length 0–10⁵. Only the five ASCII vowels count.

**Examples**
```python
count_vowels("Banana Split!")
# (4, {'a': 3, 'e': 0, 'i': 1, 'o': 0, 'u': 0})
count_vowels("rhythm")
# (0, {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0})   — 'y' is not a vowel here
```

## Hints

<details><summary>Hint 1</summary>

Create `counts = {v: 0 for v in 'aeiou'}` so every key exists.

</details>

<details><summary>Hint 2</summary>

Loop over `text.lower()` and test `if ch in counts`.

</details>

<details><summary>Hint 3</summary>

`total = sum(counts.values())`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_uppercase` | Lower-case the text before counting. |
| `test_keys_exact` | All five vowel keys must be present, even with count 0. |
| `test_no_vowels` | 'y' is not counted in this problem. |
| `test_total_matches` | `total` must equal the sum of the dictionary values. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Pre-filling the dictionary guarantees all five keys appear even when a vowel is absent. Lowering
the text once makes the comparison case-insensitive. Membership in a dict is an O(1) lookup, so
the whole function is a single linear pass.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
