# NL-05 · Character n-grams with CountVectorizer

**Topic:** Natural Language Processing · **Difficulty:** beginner · **Allowed packages:** numpy, scikit-learn

**Builds on:** NL-03 Counting Words with Counter and CountVectorizer

Read the lesson first: [article.md](article.md)

## Task

1. `char_ngrams(texts, n_min=2, n_max=3)` fits `CountVectorizer(analyzer="char_wb", ngram_range=(n_min, n_max))`
   and returns `(features, rows)` as a list of strings and a list of int lists.
2. `char_similarity(a, b, n=3)` fits a char_wb vectorizer with `ngram_range=(n, n)` on `[a, b]` and
   returns their cosine similarity as a float.

Raise `ValueError` if `n_min < 1` or `n_min > n_max` (and for `n < 1`).

## Hints

<details><summary>Hint 1</summary>

Validate the n-gram sizes before building the vectorizer.

</details>

<details><summary>Hint 2</summary>

`vec = CountVectorizer(analyzer="char_wb", ngram_range=(n_min, n_max))`.

</details>

<details><summary>Hint 3</summary>

`X = vec.fit_transform([a, b])`; `float(cosine_similarity(X[0], X[1])[0, 0])`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_cat_bigrams` | Use analyzer='char_wb', which pads words with spaces. |
| `test_range_includes_both_sizes` | ngram_range=(n_min, n_max). |
| `test_typo_closer_than_unrelated` | Fit one vectorizer on both strings and use cosine_similarity. |
| `test_invalid` | Reject n_min < 1, n_min > n_max and n < 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`char_wb` pads every word with spaces and counts the n-grams inside it. Fitting both strings in one
vectorizer guarantees that their count vectors share columns, so the cosine similarity compares like
with like.

## References

- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
