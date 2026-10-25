# NL-11 · Cosine Similarity Retrieval

**Topic:** Natural Language Processing · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** NL-09 TF-IDF

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `cosine_matrix(A, B)` → `(len(A), len(B))` cosines between rows (0 where a row is all zeros).
* `search(query_vec, doc_matrix, k)` → list of `(doc_index, score)` for the `k` best documents,
  highest score first, ties by lower index. Raise `ValueError` unless `1 <= k <= n_docs`.

**Example**
```python
search(np.array([1., 1., 0.]), np.array([[2., 2., 0.], [0., 0., 5.], [1., 0., 0.]]), 2)
# [(0, 1.0), (2, 0.7071...)]
```

## Hints

<details><summary>Hint 1</summary>

Row-normalise with a guarded division: zero rows stay zero.

</details>

<details><summary>Hint 2</summary>

`An @ Bn.T` gives all cosines.

</details>

<details><summary>Hint 3</summary>

`order = np.argsort(-scores, kind='stable')[:k]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_search` | Normalise rows before taking dot products. |
| `test_zero_vector` | Zero vectors must give cosine 0, not NaN. |
| `test_ties_stable` | Use np.argsort(-scores, kind='stable'). |
| `test_bad_k` | Validate 1 <= k <= number of documents. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Normalising rows turns dot products into cosines; zero rows remain zero so their cosines are 0.
The query's scores against all documents are ranked with a stable descending sort.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
