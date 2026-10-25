# ML-27 · Capstone: an End-to-End Tabular Model

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy, pandas, scikit-learn

**Builds on:** ML-25 k-Means and Silhouette Scores, ML-18 Pipelines and ColumnTransformer

Read the lesson first: [article.md](article.md)

## Task

Write `end_to_end(df, target, numeric, categorical, seed=0)` for a binary 0/1 target column,
returning
`{"best_C": float, "cv_auc": float, "test_accuracy": float, "test_auc": float, "baseline_accuracy": float, "model": fitted_pipeline}`.

1. `train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)` where `X` is every
   column except the target.
2. Preprocess numeric columns with median imputation and scaling, categorical columns with
   most-frequent imputation and `OneHotEncoder(handle_unknown="ignore", sparse_output=False)`.
3. Model `LogisticRegression(max_iter=1000)` named `"model"`; search `{"model__C": [0.01, 0.1, 1, 10]}`
   with `StratifiedKFold(5, shuffle=True, random_state=seed)` and `scoring="roc_auc"` on the training data.
4. Test accuracy and AUC come from the best estimator; the baseline is
   `DummyClassifier(strategy="most_frequent")` fitted on the training data, scored on the test data.

Raise `ValueError` if the target column is missing or not binary.

## Hints

<details><summary>Hint 1</summary>

Check `target in df.columns` and that its values are exactly {0, 1}; split before anything is fitted.

</details>

<details><summary>Hint 2</summary>

Build the ColumnTransformer as in the previous step and wrap it with the model in a Pipeline.

</details>

<details><summary>Hint 3</summary>

Use `search.best_estimator_.predict_proba(X_test)[:, 1]` for the test AUC.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_beats_baseline` | Tune with GridSearchCV on the training split, then score the best estimator on the test split. |
| `test_baseline_is_majority_share` | Split with test_size=0.25, stratify=y, random_state=seed before fitting anything. |
| `test_model_handles_new_rows` | Impute and use OneHotEncoder(handle_unknown='ignore') inside the pipeline. |
| `test_invalid_target` | Raise ValueError if the target column is missing or not 0/1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The split happens first, so the grid search, imputers, scaler and encoder only ever see training
rows. The search picks C by cross-validated AUC and refits on the whole training set; the test set
is used exactly once, next to a majority-class baseline that shows what the scores mean.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
