# LM-02 · Next-Token Probabilities (Add-k)

**Topic:** Large Language Models · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** LM-01 Vocabularies and Token IDs, NL-02 Tokenize and Normalize

Read the lesson first: [article.md](article.md)

## Task

Write `next_token_dist(bigrams, prev, vocab, k=1.0)` where `bigrams` maps `(prev, word)` → count.
Return a dict over **every** word in `vocab` (a list) with add-k probabilities. Raise `ValueError`
if `k < 0`, or if `k == 0` and `prev` has no observed bigrams.

**Example**
```python
b = {("like", "tea"): 1, ("like", "coffee"): 1, ("i", "like"): 2}
next_token_dist(b, "like", ["tea", "coffee", "i", "like"])
# {'tea': 0.333.., 'coffee': 0.333.., 'i': 0.1666.., 'like': 0.1666..}
```

## Hints

<details><summary>Hint 1</summary>

Context total: `sum(bigrams.get((prev, w), 0) for w in vocab)`.

</details>

<details><summary>Hint 2</summary>

Denominator: `total + k * len(vocab)`.

</details>

<details><summary>Hint 3</summary>

`{w: (bigrams.get((prev, w), 0) + k) / denom for w in vocab}`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Denominator is total + k·V. |
| `test_full_vocab` | Return a probability for every vocabulary word. |
| `test_unseen_context_uniform` | An unseen context with k > 0 gives 1/V for each word. |
| `test_mle_unseen_raises` | With k = 0 and no counts the distribution is undefined — raise ValueError. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Counts for the context are gathered over the full vocabulary, k pseudo-counts are added to each
word, and everything is divided by the adjusted total, which guarantees a proper distribution.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
