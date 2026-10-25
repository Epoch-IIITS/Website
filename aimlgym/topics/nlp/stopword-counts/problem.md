# NL-04 · Stopwords and Word Counts

**Topic:** Natural Language Processing · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** NL-02 Tokenize and Normalize

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `remove_stopwords(tokens, stopwords)` → new list without stopwords (order kept).
* `top_words(tokens, n, stopwords=())` → list of `(word, count)` for the `n` most frequent
  non-stopwords, sorted by count descending then word ascending. Raise `ValueError` if `n < 1`.

**Example**
```python
toks = ["the", "cat", "and", "the", "hat", "cat", "sat"]
remove_stopwords(toks, {"the", "and"})   # ['cat', 'hat', 'cat', 'sat']
top_words(toks, 2, {"the", "and"})       # [('cat', 2), ('hat', 1)]
```

## Hints

<details><summary>Hint 1</summary>

Convert stopwords to a set once: `sw = set(stopwords)`.

</details>

<details><summary>Hint 2</summary>

`Counter(remove_stopwords(tokens, stopwords))`.

</details>

<details><summary>Hint 3</summary>

`sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_top` | Sort by (-count, word) so ties are alphabetical. |
| `test_order_independent` | Counter.most_common keeps insertion order on ties — sort explicitly. |
| `test_remove` | Keep the original order of non-stopwords. |
| `test_bad_n` | Raise ValueError when n < 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A set makes stopword checks constant time. `Counter` tallies the remaining tokens and an explicit
sort key gives a stable, deterministic ranking independent of token order.

## References

- [Natural Language Processing with Python (NLTK Book)](https://www.nltk.org/book/) — Steven Bird, Ewan Klein, Edward Loper (`S018`)
- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
