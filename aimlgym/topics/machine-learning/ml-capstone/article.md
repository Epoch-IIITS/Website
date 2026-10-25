# Capstone: an End-to-End Tabular Model

## Learning outcomes

After this lesson you can:

- Combine a stratified split, a ColumnTransformer and a classifier in one pipeline
- Tune the model with cross-validated grid search on the training set only
- Report a baseline, the cross-validated score and the final test scores

## Intuition
Everything in this topic fits into one recipe. Split once and lock the test set away. Build all
preprocessing into a pipeline. Tune with cross-validation on the training part only. Compare with
a baseline. Then — once — evaluate on the test set.

## Precise explanation
```python
X, y = df.drop(columns=[target]), df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=0)

prep = ColumnTransformer([...])                                       # ML-18
pipe = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))])
search = GridSearchCV(pipe, {"model__C": [0.01, 0.1, 1, 10]},
                      cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="roc_auc")
search.fit(X_train, y_train)                                          # never sees the test set

baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
```

| Number | Comes from | Answers |
|---|---|---|
| baseline accuracy | `DummyClassifier` on test | what "doing nothing" scores |
| cross-validated AUC | `search.best_score_` | how good the chosen setting is, estimated on training data |
| test accuracy and AUC | `search.best_estimator_` on test | the honest final estimate |

## Worked example
For a churn table with 40% churners, the majority baseline has 0.60 accuracy. A tuned logistic
pipeline reaching 0.80 accuracy and 0.85 AUC on the test set is a real improvement; one at 0.61
accuracy is not, however good its training score.

## Common mistakes
* Preprocessing before splitting (leakage) or tuning on the test set.
* Reporting accuracy without the baseline on imbalanced data.
* Looking at test results, changing the model, and looking again — the test set is then a
  validation set.

## Why this matters
This is the workflow behind the house-price and spam/fraud project ideas, and the model you can
serve with FastAPI in "Serve your model".

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
