# NL-02 · Tokenize and Normalize

**Topic:** Natural Language Processing · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** NL-01 Regular Expressions for Text

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `normalize(text)` → NFKD-decompose, remove combining characters, lowercase.
* `tokenize(text)` → `re.findall(r"[a-z0-9]+(?:'[a-z]+)?", normalize(text))`.

**Examples**
```python
normalize("Café ÉLAN")   # 'cafe elan'
tokenize("Café's menu: 2 croissants, NO coffee!")
# ["cafe's", 'menu', '2', 'croissants', 'no', 'coffee']
tokenize("--- ...")      # []
```

## Hints

<details><summary>Hint 1</summary>

`unicodedata.normalize('NFKD', text)`.

</details>

<details><summary>Hint 2</summary>

`''.join(ch for ch in s if not unicodedata.combining(ch)).lower()`.

</details>

<details><summary>Hint 3</summary>

Apply the given regex with `re.findall` to the normalised text.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_normalize` | Use NFKD and drop characters where unicodedata.combining(ch) is non-zero. |
| `test_tokens` | Normalise before applying the lowercase regex. |
| `test_contraction` | Keep the optional (?:'[a-z]+) group in the regex. |
| `test_accent_mid_word` | Accented letters must become plain letters, not separators. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

NFKD splits accented letters into base letters plus combining marks, which are then removed.
Lowercasing finishes normalisation. A compiled regex extracts alphanumeric runs with an optional
apostrophe suffix, so contractions remain one token.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Natural Language Processing with Python (NLTK Book)](https://www.nltk.org/book/) — Steven Bird, Ewan Klein, Edward Loper (`S018`)
