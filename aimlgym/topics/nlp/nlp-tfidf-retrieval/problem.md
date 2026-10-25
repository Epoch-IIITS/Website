# NL-10 · Search with TfidfVectorizer and Cosine Similarity

**Topic:** Natural Language Processing · **Difficulty:** intermediate · **Allowed packages:** numpy, scikit-learn

**Builds on:** NL-09 TF-IDF

Read the lesson first: [article.md](article.md)

## Task

1. `build_index(docs)` returns `(vectorizer, matrix)` from `TfidfVectorizer().fit_transform(docs)`.
   Raise `ValueError` for an empty list.
2. `search(index, query, k=3)` returns up to `k` pairs `(doc_index, score)` sorted by score
   descending and then index ascending, with scores as floats from `cosine_similarity`. Raise
   `ValueError` if `k < 1`.

## Hints

<details><summary>Hint 1</summary>

`vec = TfidfVectorizer(); matrix = vec.fit_transform(docs)`.

</details>

<details><summary>Hint 2</summary>

`scores = cosine_similarity(vec.transform([query]), matrix)[0]`.

</details>

<details><summary>Hint 3</summary>

`sorted(range(len(scores)), key=lambda i: (-scores[i], i))[:k]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_best_match_first` | Transform the query with the fitted vectorizer; do not fit a new one. |
| `test_scores_sorted_and_bounded` | Sort by score descending, then by index. |
| `test_unknown_words` | Unknown words give zero scores; ties keep index order. |
| `test_invalid` | Reject an empty corpus and k < 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The index stores the fitted vectorizer and the document matrix. A query is transformed with the
same vocabulary and IDF; cosine similarity scores it against every document, and a stable sort
returns the best matches first.

## References

- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
