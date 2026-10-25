# NL-08 · Bigram Counts with Sentence Markers

**Topic:** Natural Language Processing · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** NL-04 Stopwords and Word Counts

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `bigram_counts(sentences)` → dict with `"bigrams"` (`Counter` of `(prev, word)` tuples) and
  `"contexts"` (`Counter` of how often each token is the first element of a bigram). Each sentence
  is a token list padded with `<s>` and `</s>`.
* `bigram_prob(w_prev, w, counts)` → MLE probability; raise `KeyError` if `w_prev` was never a
  context.

**Example**
```python
c = bigram_counts([["i", "like", "tea"], ["i", "like", "coffee"]])
c["bigrams"][("i", "like")]        # 2
bigram_prob("like", "tea", c)      # 0.5
bigram_prob("<s>", "i", c)         # 1.0
```

## Hints

<details><summary>Hint 1</summary>

`toks = ['<s>'] + sent + ['</s>']`.

</details>

<details><summary>Hint 2</summary>

`for a, b in zip(toks, toks[1:]): bigrams[(a, b)] += 1; contexts[a] += 1`.

</details>

<details><summary>Hint 3</summary>

`counts['bigrams'][(w_prev, w)] / counts['contexts'][w_prev]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_counts` | Pad every sentence with <s> and </s> before pairing. |
| `test_no_cross_sentence` | Count pairs within each sentence only. |
| `test_unknown_context` | Raise KeyError when the context was never seen. |
| `test_sums_to_one` | Divide by context counts (first element of bigrams), not all unigram counts. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each padded sentence contributes its consecutive pairs; the first token of every pair is also
counted as a context. The MLE probability divides the pair count by the context count, so
probabilities for a context sum to one.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Natural Language Processing with Python (NLTK Book)](https://www.nltk.org/book/) — Steven Bird, Ewan Klein, Edward Loper (`S018`)
