# NL-14 · Multinomial Naive Bayes Text Classifier

**Topic:** Natural Language Processing · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** NL-07 Bag-of-Words Vectors, ST-07 Conditional Probability and Bayes' Rule

Read the lesson first: [article.md](article.md)

## Task

Implement `class MultinomialNB(alpha=1.0)` for an integer count matrix `X` `(n, V)` and labels
`y` (any hashable class values):
* `fit(X, y)` → stores `classes_` (sorted unique labels), `class_log_prior_` `(K,)` and
  `feature_log_prob_` `(K, V)`; returns `self`. Raise `ValueError` if `alpha <= 0`.
* `predict_log_proba(X)` → `(n, K)` normalised log posteriors (rows log-sum-exp to 0).
* `predict(X)` → array of class labels (argmax; ties → first class in `classes_`).

**Example**
```python
X = np.array([[3, 0], [0, 2]]); y = np.array(["spam", "ham"])
m = MultinomialNB().fit(X, y)
np.exp(m.feature_log_prob_)      # [[0.25, 0.75], [0.8, 0.2]]   (classes_ = ['ham', 'spam'])
m.predict(np.array([[1, 0]]))    # ['spam']
```

## Hints

<details><summary>Hint 1</summary>

`self.classes_ = np.unique(y)`; for each class, `Nc = X[y == c].sum(axis=0)`.

</details>

<details><summary>Hint 2</summary>

`feature_log_prob = np.log((Nc + a) / (Nc.sum() + a * V))`.

</details>

<details><summary>Hint 3</summary>

Joint `= X @ flp.T + prior`; subtract the row log-sum-exp.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_params` | θ = (N_ct + α)/(Σ_t N_ct + αV) per class, using term counts. |
| `test_log_proba_normalised` | Subtract the log-sum-exp of each row. |
| `test_smoothing_unseen_word` | Laplace smoothing must give unseen words a non-zero probability. |
| `test_long_document_no_underflow` | Stay in log space; don't exponentiate before normalising. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Training reduces to counting: class frequencies give priors, and smoothed per-class term counts
give word probabilities, all stored as logs. Prediction is a matrix product of counts with log
probabilities plus log priors, normalised with log-sum-exp; argmax picks the most probable class.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
