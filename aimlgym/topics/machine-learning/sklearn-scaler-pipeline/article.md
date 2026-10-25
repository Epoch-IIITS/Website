# Scaling inside a Pipeline

## Learning outcomes

After this lesson you can:

- Chain a StandardScaler and a model in a Pipeline
- Explain why the scaler must be fitted on training data only (leakage)
- Inspect a fitted step through named_steps

## Intuition
Many models care about feature scale: a feature measured in metres and one in millimetres should
not get different influence just because of units. Standardising (subtract the mean, divide by
the standard deviation) fixes that — but the mean and standard deviation must come from the
**training** data only. A `Pipeline` makes that automatic.

## Precise explanation
```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
pipe.fit(X_train, y_train)    # scaler.fit_transform(X_train), then model.fit
pipe.predict(X_test)          # scaler.transform(X_test) with the TRAINING mean/std, then predict
```

* A pipeline is itself an estimator: it has `fit`, `predict`, `score`, `get_params`.
* Every step but the last is a **transformer** (`fit` + `transform`); the last can be any model.
* `pipe.named_steps["scale"].mean_` and `.scale_` are the statistics learned from training data
  (`scale_` uses the population standard deviation, ddof = 0).
* **Leakage**: fitting the scaler on all data before splitting lets test-set statistics shape
  training. The scores look better than the model will be on truly new data.

## Worked example
Train column [0, 2, 4] has mean 2 and standard deviation 1.633. A test value 6 becomes
(6 − 2)/1.633 = 2.45 — test values are scaled with training statistics, even though the test set
on its own has a different mean.

## What the library does inside
`StandardScaler` stores the column means and standard deviations in `fit` and applies them in
`transform` — the function you build in ML-08, the optional deep dive after this
step. The pipeline just calls the steps in order.

## Common mistakes
* `StandardScaler().fit(X)` on the whole dataset before splitting (leakage).
* Calling `fit_transform` on the test set: it refits the scaler to test statistics.
* Reusing one pipeline object across experiments without cloning; the last fit overwrites it.

## Why this matters
Cross-validation and hyperparameter search refit the whole pipeline on each training fold, so
leakage is prevented everywhere — but only if preprocessing lives inside the pipeline.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
