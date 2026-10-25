# NL-12 · Levenshtein Edit Distance

**Topic:** Natural Language Processing · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** NL-05 Character n-grams with CountVectorizer

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `levenshtein(a, b)` → int, using DP (insert, delete, substitute all cost 1).
* `suggest(word, vocab, max_dist=2)` → list of vocabulary words with distance `<= max_dist`,
  sorted by distance then alphabetically.

**Examples**
```python
levenshtein("kitten", "sitting")   # 3
levenshtein("", "abc")             # 3
suggest("teh", ["the", "tea", "ten", "apple"], 2)   # ['tea', 'ten', 'the']
```

## Hints

<details><summary>Hint 1</summary>

`prev = list(range(len(b) + 1))` is row 0.

</details>

<details><summary>Hint 2</summary>

For each i: `cur = [i]`; append `min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (a[i-1] != b[j-1]))`.

</details>

<details><summary>Hint 3</summary>

`sorted((levenshtein(word, w), w) for w in vocab)` then filter by max_dist.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_classic` | Substitution cost is 0 when characters match, else 1. |
| `test_empty` | Initialise row 0 as 0..len(b) and column 0 as i. |
| `test_suggest_ordering` | Sort by (distance, word). |
| `test_triangle` | intention→execution is the textbook example with distance 5. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The table is filled row by row keeping only the previous row. Each cell takes the cheapest of
deletion, insertion and substitution (free when characters match). Suggestions sort
(distance, word) pairs for a deterministic ranking.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
