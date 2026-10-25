# NL-17 · PPMI Co-occurrence Matrix

**Topic:** Natural Language Processing · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** NL-07 Bag-of-Words Vectors, NL-09 TF-IDF

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `cooccurrence(sentences, vocab, window=2)` → int matrix `(V, V)` with `vocab` a dict word → index;
  tokens not in vocab are skipped as targets **and** contexts but still occupy positions.
  Raise `ValueError` if `window < 1`.
* `ppmi(C)` → float PPMI matrix (log base 2, zeros where C is 0). Raise `ValueError` if `C.sum() == 0`.

**Example**
```python
vocab = {"a": 0, "b": 1, "c": 2}
C = cooccurrence([["a", "b"], ["a", "c"]], vocab, window=1)   # [[0,1,1],[1,0,0],[1,0,0]]
ppmi(C)[0, 1]    # 1.0
```

## Hints

<details><summary>Hint 1</summary>

For each i, loop `j in range(max(0, i - window), min(len(s), i + window + 1))`, skipping j == i.

</details>

<details><summary>Hint 2</summary>

`P = C / N`, `pw = P.sum(1, keepdims=True)`, `pc = P.sum(0, keepdims=True)`.

</details>

<details><summary>Hint 3</summary>

Compute log2 only where C > 0: `np.log2(P / (pw * pc), where=C > 0, out=np.zeros_like(P))`, then clip at 0.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_counts` | Count neighbours within the window inside each sentence, excluding the word itself. |
| `test_oov_positions` | OOV tokens still occupy positions; don't delete them before windowing. |
| `test_ppmi_value` | PMI = log2(P(w,c) / (P(w)P(c))) with marginals from row/column sums. |
| `test_ppmi_nonneg_finite` | Only take logs where C > 0 and clip negatives to 0. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Counting walks a symmetric window inside each sentence, skipping the centre and out-of-vocabulary
tokens (which still keep their positions). PPMI converts counts to joint and marginal probabilities
and takes log2 only where counts are positive, clipping negatives to zero.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
