# NL-09 · TF-IDF

**Topic:** Natural Language Processing · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** NL-07 Bag-of-Words Vectors

Read the lesson first: [article.md](article.md)

## Task

Write `tfidf(counts)` for an integer count matrix (NumPy array, `(n_docs, n_terms)`) returning
`(W, idf)`: the L2-row-normalised TF-IDF matrix (floats) and the IDF vector, using the smoothed
formula above with natural logs. Raise `ValueError` for negative counts or non-2-D input.

**Example**
```python
W, idf = tfidf(np.array([[1, 1], [2, 0]]))
idf    # [1.        , 1.40546511]
W      # [[0.57973867, 0.81480247], [1., 0.]]
```

## Hints

<details><summary>Hint 1</summary>

`df = (C > 0).sum(axis=0)`; `n = C.shape[0]`.

</details>

<details><summary>Hint 2</summary>

`idf = np.log((1 + n) / (1 + df)) + 1`; `W = C * idf`.

</details>

<details><summary>Hint 3</summary>

`norms = np.linalg.norm(W, axis=1, keepdims=True)`; divide where norms > 0.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_idf_formula` | idf = ln((1 + n)/(1 + df)) + 1 with natural log. |
| `test_unit_rows` | Normalise each row (axis=1) to unit L2 norm. |
| `test_empty_doc` | Guard the division so empty documents stay all-zero. |
| `test_example` | Multiply raw counts by idf before normalising. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Document frequency counts non-zero entries per column; smoothed IDF follows. Broadcasting
multiplies each column by its IDF, and rows are scaled to unit length, with empty rows left as
zeros via a guarded division.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
