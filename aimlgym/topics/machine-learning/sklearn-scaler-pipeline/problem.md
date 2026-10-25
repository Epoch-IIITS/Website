# ML-07 · Scaling inside a Pipeline

**Topic:** Machine Learning · **Difficulty:** beginner · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-04 Splitting Data with scikit-learn

Read the lesson first: [article.md](article.md)

## Task

Write `train_and_predict(X_train, y_train, X_test)` that builds a **new** pipeline
`Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])`, fits it on the
training data and returns `(pipeline, predictions)` with predictions as a list of Python ints.

**Example**
```python
pipe, pred = train_and_predict([[0, 100], [1, 110], [2, 300], [3, 310]], [0, 0, 1, 1], [[0.5, 105], [2.5, 305]])
pred                                       # [0, 1]
pipe.named_steps["scale"].mean_.tolist()   # [1.5, 205.0]   (training statistics)
```

## Hints

<details><summary>Hint 1</summary>

Create the pipeline inside the function so each call gets fresh steps.

</details>

<details><summary>Hint 2</summary>

`pipe.fit(X_train, y_train)` fits the scaler and then the model.

</details>

<details><summary>Hint 3</summary>

`[int(v) for v in pipe.predict(X_test)]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_scaler_uses_training_statistics` | Fit the pipeline on the training data only; never on X_test. |
| `test_step_names` | Name the steps 'scale' and 'model'. |
| `test_new_pipeline_each_call` | Build the Pipeline inside the function. |
| `test_plain_ints` | Convert predictions with int(...). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Fitting the pipeline fits the scaler on the training rows only and trains the model on the scaled
rows; predicting transforms the test rows with the stored training statistics before the model
sees them. Building the pipeline inside the function keeps calls independent.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
