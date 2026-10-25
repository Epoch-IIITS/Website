# Pipelines and ColumnTransformer

## Learning outcomes

After this lesson you can:

- Preprocess numeric and categorical columns differently with ColumnTransformer
- Impute missing values and one-hot encode categories inside a pipeline
- Fit and predict directly on a pandas DataFrame

## Intuition
Real tables mix numbers (area, age) and categories (city, plan), with gaps. Numbers need
imputing and scaling; categories need imputing and one-hot encoding. `ColumnTransformer` sends
each group of columns through its own mini-pipeline and glues the results together, and the
whole thing still fits and predicts like one model.

## Precise explanation
```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
categorical = make_pipeline(SimpleImputer(strategy="most_frequent"),
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False))
prep = ColumnTransformer([("num", numeric, ["area", "age"]), ("cat", categorical, ["city"])])
model = Pipeline([("prep", prep), ("model", LinearRegression())])
model.fit(df_train, y_train); model.predict(df_test)
```

* Columns are selected **by name** from a DataFrame; columns not listed are dropped.
* `SimpleImputer` learns the median (or most frequent value) on training data and fills gaps.
* `OneHotEncoder` makes one 0/1 column per category seen in training; `handle_unknown="ignore"`
  turns an unseen category into all zeros instead of an error.
* `prep.get_feature_names_out()` lists the output columns, e.g. `num__area`, `cat__city_Pune`.

## Worked example
Training cities [Pune, Delhi, Pune] become columns `cat__city_Delhi`, `cat__city_Pune`. A test
row with city Chennai becomes [0, 0] in those columns, and a missing area is filled with the
training median.

## What the library does inside
The imputers and encoders are fitted on the training rows during `fit` — the same "fit on train,
apply to test" rule as ML-07 — and the column outputs are concatenated side
by side, as `pd.concat(axis=1)` would.

## Common mistakes
* Encoding categories with `pd.get_dummies` on the full dataset (leakage and mismatched columns).
* Forgetting `handle_unknown="ignore"` and crashing on a new category in production.
* Passing a NumPy array when the transformer selects columns by name.

## Why this matters
This is how tabular models are built in practice; the house-price project idea and the capstone
both start from a ColumnTransformer.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
