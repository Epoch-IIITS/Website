# NL-15 · A Text Classification Pipeline

**Topic:** Natural Language Processing · **Difficulty:** advanced · **Allowed packages:** numpy, scikit-learn

**Builds on:** NL-14 Multinomial Naive Bayes Text Classifier, NL-10 Search with TfidfVectorizer and Cosine Similarity

Read the lesson first: [article.md](article.md)

## Task

1. `train_text_classifier(texts, labels, C=1.0)` fits and returns
   `Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)), ("clf", LogisticRegression(C=C, max_iter=1000))])`.
   Raise `ValueError` if the lengths differ or there are fewer than two classes.
2. `top_features(pipe, n=5)` for a binary pipeline returns `{"positive": [...], "negative": [...]}`:
   the `n` features with the largest and with the most negative coefficients, each list ordered from
   strongest to weakest.

## Hints

<details><summary>Hint 1</summary>

Validate `len(texts) == len(labels)` and `len(set(labels)) >= 2`, then build and fit the pipeline.

</details>

<details><summary>Hint 2</summary>

`names = pipe.named_steps["tfidf"].get_feature_names_out()`; `weights = pipe.named_steps["clf"].coef_[0]`.

</details>

<details><summary>Hint 3</summary>

`order = np.argsort(weights)`: the last n reversed are positive, the first n are negative.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_accuracy_on_new_reviews` | Fit a Pipeline of TfidfVectorizer and LogisticRegression on the raw texts. |
| `test_pipeline_structure` | Use ngram_range=(1, 2), sublinear_tf=True and the given C. |
| `test_top_features_make_sense` | Positive coefficients point to class 1; sort coef_[0]. |
| `test_invalid` | Require matching lengths and at least two classes. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The pipeline learns the vocabulary and the weights together from raw text. For a binary model each
coefficient belongs to one word or word pair; sorting them shows the phrases that most strongly
indicate each class.

## References

- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
