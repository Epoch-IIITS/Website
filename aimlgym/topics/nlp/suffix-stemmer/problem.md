# NL-13 · Rule-Based Suffix Stemmer

**Topic:** Natural Language Processing · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** NL-02 Tokenize and Normalize

Read the lesson first: [article.md](article.md)

## Task

Implement for lowercase ASCII words:
* `measure(stem)` → Porter's m.
* `step1ab(word)` → result of Porter Step 1a then Step 1b exactly as described.

**Examples**
```python
measure("tree"), measure("trouble"), measure("oaten")   # (0, 1, 2)
step1ab("caresses"), step1ab("ponies"), step1ab("feed"), step1ab("agreed")
# ('caress', 'poni', 'feed', 'agree')
step1ab("hopping"), step1ab("filing"), step1ab("sing")  # ('hop', 'file', 'sing')
```

## Hints

<details><summary>Hint 1</summary>

`is_consonant`: vowels aeiou → False; 'y' → True at i = 0, else `not is_consonant(word, i-1)`.

</details>

<details><summary>Hint 2</summary>

Build a C/V pattern string, collapse runs, and count occurrences of 'VC'.

</details>

<details><summary>Hint 3</summary>

Write helpers `has_vowel`, `ends_double_consonant`, `ends_cvc`; apply rules with `str.endswith`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_measure` | Collapse the C/V pattern to runs and count 'VC' occurrences. |
| `test_y_consonant` | y is a consonant at the start or after a vowel; a vowel after a consonant. |
| `test_eed_blocks_ed` | If the word ends in 'eed', only the EED rule is considered. |
| `test_step1b` | Tidy-up rules (ATE/BLE/IZE, double consonant, *o + E) apply only after ED/ING removal. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`is_consonant` encodes Porter's y-rule recursively. The measure collapses the C/V pattern into
alternating runs and counts VC pairs. Step 1a picks the first matching suffix. In Step 1b, an EED
match blocks the ED rule even when its m > 0 condition fails (so "feed" stays "feed"), and the
tidy-up rules run only after ED or ING was actually removed.

## References

- [Natural Language Processing with Python (NLTK Book)](https://www.nltk.org/book/) — Steven Bird, Ewan Klein, Edward Loper (`S018`)
- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
