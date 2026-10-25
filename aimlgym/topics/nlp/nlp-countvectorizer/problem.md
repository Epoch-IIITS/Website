# NL-03 · Counting Words with Counter and CountVectorizer

**Topic:** Natural Language Processing · **Difficulty:** beginner · **Allowed packages:** numpy, scikit-learn

**Builds on:** NL-02 Tokenize and Normalize, ML-02 The scikit-learn Estimator API

Read the lesson first: [article.md](article.md)

## Task

1. `top_words(texts, k, stop_words=())` lowercases each text, finds tokens with
   `re.findall(r"[a-z']+", text.lower())`, drops tokens in `stop_words`, and returns the `k` most
   common as `(word, count)` pairs, sorted by count descending and then alphabetically.
2. `count_matrix(texts, stop_words=None, min_df=1)` fits `CountVectorizer(stop_words=stop_words,
   min_df=min_df)` and returns `(vocabulary, rows)`: the feature names as a list of strings and the
   dense matrix as a list of lists of ints.

Raise `ValueError` in both if `texts` is empty, and in `top_words` if `k < 1`.

## Hints

<details><summary>Hint 1</summary>

Update one Counter with the filtered tokens of every text.

</details>

<details><summary>Hint 2</summary>

`sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]` gives the ordering.

</details>

<details><summary>Hint 3</summary>

`vec = CountVectorizer(...)`; `X = vec.fit_transform(texts)`; return `list(vec.get_feature_names_out())` and `X.toarray().tolist()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_count_matrix_example` | Fit CountVectorizer(stop_words=...) and return get_feature_names_out() and the dense rows. |
| `test_top_words_ties_alphabetical` | Sort by (-count, word). |
| `test_min_df` | Pass min_df to CountVectorizer. |
| `test_single_letters_dropped_and_types` | Return plain str and int values. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`Counter` accumulates token frequencies across all texts; sorting on negative count and then the
word gives a deterministic top-k. `CountVectorizer` learns the vocabulary and produces one count row
per document; its feature names are already in column order.

## References

- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
