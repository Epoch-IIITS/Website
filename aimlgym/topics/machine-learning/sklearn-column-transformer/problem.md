# ML-18 · Pipelines and ColumnTransformer

**Topic:** Machine Learning · **Difficulty:** intermediate · **Allowed packages:** numpy, pandas, scikit-learn

**Builds on:** ML-16 Cross-Validation with scikit-learn

Read the lesson first: [article.md](article.md)

## Task

Write `build_model(numeric, categorical)` that returns an **unfitted**
`Pipeline([("prep", ColumnTransformer(...)), ("model", LinearRegression())])` where

* numeric columns go through `SimpleImputer(strategy="median")` then `StandardScaler()`
  (transformer name `"num"`),
* categorical columns go through `SimpleImputer(strategy="most_frequent")` then
  `OneHotEncoder(handle_unknown="ignore", sparse_output=False)` (transformer name `"cat"`).

Raise `ValueError` if both column lists are empty or a column appears in both.

**Example**
```python
model = build_model(["area"], ["city"]).fit(df, df["price"])
list(model.named_steps["prep"].get_feature_names_out())
# ['num__area', 'cat__city_Delhi', 'cat__city_Pune']
```

## Hints

<details><summary>Hint 1</summary>

Validate the two lists first (empty both, or overlapping names).

</details>

<details><summary>Hint 2</summary>

Each branch is a `make_pipeline(imputer, transformer)`.

</details>

<details><summary>Hint 3</summary>

`ColumnTransformer([("num", numeric_pipe, numeric), ("cat", categorical_pipe, categorical)])`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_feature_names` | Name the transformers 'num' and 'cat' and keep the column order you were given. |
| `test_median_imputation_from_training` | Numeric columns: SimpleImputer(strategy='median') then StandardScaler(). |
| `test_unknown_category_is_zeros` | Use OneHotEncoder(handle_unknown='ignore', sparse_output=False). |
| `test_invalid` | Reject empty column lists and columns listed twice. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Two small pipelines handle the column types; the ColumnTransformer applies each to its columns
and concatenates the outputs; the outer pipeline adds the model. Everything is learned in `fit`
from the training rows, so the same object can predict on new DataFrames safely.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
