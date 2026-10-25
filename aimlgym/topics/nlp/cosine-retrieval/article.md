# Retrieval with Cosine Similarity

## Learning outcomes

After this lesson you can:

- Compute cosine similarity between query and documents
- Rank documents with stable top-k
- Handle zero vectors

## Intuition
Two documents about the same topic use similar words in similar *proportions*, even if one is
much longer. Cosine similarity compares directions, ignoring length.

## Precise explanation
$$\cos(a, b) = \frac{a\cdot b}{\lVert a\rVert\,\lVert b\rVert}\in[-1, 1]$$
(in [0, 1] for non-negative TF-IDF vectors). For matrices with rows as vectors:
normalise rows, then `A_n @ B_n.T` gives all pairwise cosines. A zero vector has no direction;
define its cosine with anything as 0.
**Search:** score every document against the query and return the top k indices (stable order on
ties, NP-09).

## Worked example
q = [1, 1, 0], docs [[2, 2, 0], [0, 0, 5], [1, 0, 0]] → cosines [1, 0, 0.707] → ranking [0, 2, 1].

## Common mistakes
* Dot products without normalisation (long documents always win).
* NaN from 0/0 for empty vectors.
* Reversing argsort and breaking tie order.

## Why this matters
This is the retrieval step in search engines and retrieval-augmented generation (with dense
embeddings instead of TF-IDF).

## Library implementation

`sklearn.metrics.pairwise.cosine_similarity(A, B)` returns the same matrix (treating all-zero
rows as similarity 0). For large collections, vector databases and libraries such as FAISS find
the top-k without computing every score.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
