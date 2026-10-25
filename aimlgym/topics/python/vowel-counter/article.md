# Counting with Dictionaries

## Learning outcomes

After this lesson you can:

- Iterate over characters of a string
- Use dictionaries as counters
- Normalise case before comparing

## Intuition
Counting how often each vowel appears is like tallying votes: one box per candidate, add a mark
for each vote. A **dictionary** maps keys (the candidates) to values (the tallies).

## Precise explanation
* Iterating over a string yields its characters: `for ch in "hey": ...` gives `'h'`, `'e'`, `'y'`.
* `ch in "aeiou"` tests membership (works for strings, lists, sets, dict keys).
* Initialise all counters so missing vowels report 0:
  `counts = {v: 0 for v in "aeiou"}` (a **dict comprehension**).
* Lower-case once (`text.lower()`) so `'A'` and `'a'` are counted together.

```python
counts = {v: 0 for v in "aeiou"}
for ch in text.lower():
    if ch in counts:
        counts[ch] += 1
```

## Worked example
`"Banana Split!"` → lower: `"banana split!"` → a appears 3 times, i once →
`{'a': 3, 'e': 0, 'i': 1, 'o': 0, 'u': 0}`; total = 4.

## Common mistakes
* Forgetting to lowercase, so capital vowels are missed.
* Writing `counts[ch] += 1` for a key that doesn't exist → `KeyError`. Pre-fill keys or use
  `dict.get(ch, 0) + 1`.
* Counting `'y'` — this problem defines vowels as `a e i o u` only.

## Why this matters
Frequency counting is the foundation of bag-of-words models, n-gram language models and
histograms. `collections.Counter` does this for you; knowing the manual version helps you read it.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
