# NL-18 · Word Embedding Analogies

**Topic:** Natural Language Processing · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** NL-10 Search with TfidfVectorizer and Cosine Similarity, NL-17 PPMI Co-occurrence Matrix

Read the lesson first: [article.md](article.md)

## Task

`emb` is a dict word → 1-D NumPy vector (same length). Implement:
* `most_similar(word, emb, k=3)` → list of `(other_word, cosine)` for the k most similar *other*
  words, highest first, ties alphabetical. Raise `KeyError` for unknown words.
* `analogy(a, b, c, emb)` → the word d (not a, b or c) maximising cosine with `v_b - v_a + v_c`
  (ties alphabetical).

Zero vectors have cosine 0 with everything.

**Example**
```python
emb = {"man": np.array([1., 0, 0]), "woman": np.array([1., 1, 0]),
       "king": np.array([1., 0, 1]), "queen": np.array([1., 1, 1])}
analogy("man", "woman", "king", emb)   # 'queen'
```

## Hints

<details><summary>Hint 1</summary>

Write `_cos(u, v)` returning 0 if either norm is 0.

</details>

<details><summary>Hint 2</summary>

Score every candidate and sort with key `(-score, word)`.

</details>

<details><summary>Hint 3</summary>

Target vector: `emb[b] - emb[a] + emb[c]`; skip {a, b, c}.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_analogy` | Target = v_b − v_a + v_c; rank by cosine. |
| `test_excludes_inputs` | Exclude a, b and c from the candidates. |
| `test_zero_vector` | Return cosine 0 for zero vectors instead of NaN. |
| `test_ties_alphabetical` | Sort by (−score, word). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A shared ranking helper scores candidates by cosine with a target vector, excluding given words,
and sorts by score then name. Similarity search uses the word's own vector; analogies use the
3CosAdd offset vector.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
