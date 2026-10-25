# TF-IDF

## Learning outcomes

After this lesson you can:

- Compute document frequency and smoothed IDF
- Weight term frequencies by IDF
- L2-normalise document vectors

## Intuition
A word matters for a document if it appears there often (term frequency) but is rare across the
collection (inverse document frequency). "the" is frequent everywhere — low weight; "photosynthesis"
in one biology document — high weight.

## Precise explanation
Given a count matrix $C$ `(n_docs, n_terms)` (NL-07):
* document frequency $\text{df}_t$ = number of documents with $C_{dt} > 0$;
* smoothed IDF (the scikit-learn default `smooth_idf=True`):
  $\text{idf}_t = \ln\frac{1 + n}{1 + \text{df}_t} + 1$;
* weights $W_{dt} = C_{dt}\cdot \text{idf}_t$ (raw counts as TF);
* L2-normalise each row: $W_d / \lVert W_d\rVert_2$ (rows of all zeros stay zero).
The "+1"s avoid division by zero and keep terms that appear in every document from getting
weight exactly 0.

## Worked example
2 docs, terms [a, b]: C = [[1, 1], [2, 0]]. df = [2, 1]; idf = [ln(3/3)+1, ln(3/2)+1] =
[1, 1.405]. Row 0: [1, 1.405] / 1.725 = [0.580, 0.815]; row 1: [2, 0] → [1, 0].

## Common mistakes
* Using log base 10 vs natural log inconsistently.
* Normalising columns instead of rows.
* Dividing by zero for empty documents.

## Why this matters
TF-IDF is a strong baseline for search and classification and the "sparse" half of modern
hybrid retrieval in RAG systems.

## Library implementation

`sklearn.feature_extraction.text.TfidfTransformer()` with its defaults (`smooth_idf=True`,
`norm="l2"`, raw counts) uses exactly this formula: $\mathrm{idf} = \ln\frac{1+n}{1+df} + 1$ and
L2-normalised rows. `TfidfVectorizer` does tokenising, counting and weighting together.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
