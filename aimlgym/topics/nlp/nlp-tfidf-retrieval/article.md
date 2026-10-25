# Search with TfidfVectorizer and Cosine Similarity

## Learning outcomes

After this lesson you can:

- Index documents with TfidfVectorizer
- Rank documents for a query with cosine_similarity
- Explain why TF-IDF rows are L2-normalised

## Intuition
A search engine needs a score for "how well does this document match the query?". TF-IDF weights
words that are frequent in a document but rare in the collection; cosine similarity compares the
query's weights with each document's. Rank by score and show the top few.

## Precise explanation
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vec = TfidfVectorizer()
D = vec.fit_transform(docs)                 # one L2-normalised row per document
q = vec.transform([query])                  # same vocabulary and IDF weights
scores = cosine_similarity(q, D)[0]         # one score per document
```

* scikit-learn's IDF is smoothed: idf(t) = ln((1 + n)/(1 + df(t))) + 1, so every word keeps a
  positive weight. Rows are L2-normalised (`norm="l2"`), which makes cosine similarity a plain dot
  product.
* The query is **transformed**, never fitted: it must use the documents' vocabulary and IDF.
* A query of only unknown words gets a zero vector and scores 0 against everything.

## Worked example
Documents "python lists are mutable", "tuples are immutable", "pandas dataframes hold tables":
the query "mutable lists" scores highest on the first document; "are" appears in two documents, so
it has a lower IDF and contributes less.

## What the library does inside
The TF-IDF weighting of NL-09 and the cosine ranking of NL-11 (the optional
deep dive after this step), on sparse matrices so that millions of documents are feasible.

## Common mistakes
* Fitting a new vectorizer on the query.
* Forgetting that `cosine_similarity` returns a 2-D array (one row per query).
* Breaking ties arbitrarily; sort by score and then by document index for stable results.

## Why this matters
This is the retrieval step of the RAG pipeline in the LLM topic and the basis of the blog
semantic-search project idea.

## References

- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
