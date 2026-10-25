# NL-06 · Character n-grams by Hand

**Topic:** Natural Language Processing · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** NL-02 Tokenize and Normalize

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `char_ngrams(word, n_min=3, n_max=3)` → list of n-grams of `"<"+word+">"`, ordered by n
  ascending then by position. Raise `ValueError` if `n_min < 1` or `n_max < n_min`.
* `jaccard(a, b, n=3)` → Jaccard similarity of the *sets* of n-grams of words `a` and `b`
  (1.0 if both sets are empty).

**Examples**
```python
char_ngrams("cat")             # ['<ca', 'cat', 'at>']
char_ngrams("ab", 2, 3)        # ['<a', 'ab', 'b>', '<ab', 'ab>']
jaccard("cat", "cart")         # 0.16666...
```

## Hints

<details><summary>Hint 1</summary>

`s = '<' + word + '>'`.

</details>

<details><summary>Hint 2</summary>

For each n in range(n_min, n_max + 1): `[s[i:i+n] for i in range(len(s) - n + 1)]`.

</details>

<details><summary>Hint 3</summary>

Sets: `A = set(char_ngrams(a, n, n))`; return `len(A & B) / len(A | B)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_cat` | Wrap the word in '<' and '>' before slicing. |
| `test_range` | Order by n first, then by position. |
| `test_jaccard` | Use sets of n-grams: |A ∩ B| / |A ∪ B|. |
| `test_jaccard_disjoint_and_empty` | Return 1.0 when both n-gram sets are empty. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Markers are added once; each n contributes all windows of that length in order. Jaccard compares
n-gram sets, handling the empty case explicitly.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) — Rico Sennrich, Barry Haddow, Alexandra Birch (`S020`)
