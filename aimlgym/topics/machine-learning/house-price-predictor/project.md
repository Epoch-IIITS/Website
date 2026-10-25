# ML-P1 · Project idea: House-Price Predictor

**Topic:** Machine Learning · ungraded

## Brief

Build a model that estimates house prices from a table of homes, and an error analysis that shows
where it is wrong. Someone pricing a home should be able to see the estimate, a typical error, and
which kinds of homes the model struggles with.

## You will use

- ML-02 The scikit-learn Estimator API
- ML-04 Splitting Data with scikit-learn
- ML-16 Cross-Validation with scikit-learn
- ML-18 Pipelines and ColumnTransformer

## Milestones

1. Load the data with pandas, look at missing values and the distribution of prices.
2. Split once into train and test, and fit a mean baseline and a LinearRegression pipeline.
3. Build a ColumnTransformer for numeric and categorical columns and compare models with 5-fold cross-validation.
4. Try predicting log(price) and engineered features (age of house, price per room) and keep what helps.
5. Evaluate once on the test set and list the 20 largest errors to look for patterns.

## Stretch goals

- Tune a Ridge or gradient-boosting model with GridSearchCV.
- Report a prediction interval (for example from quantile regression) instead of a single number.
- Save the pipeline with joblib and load it in a separate script.

## Data

* California housing (20,640 districts, numeric features): `sklearn.datasets.fetch_california_housing()`
  downloads it the first time — see the
  [dataset page](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html).
* Ames house prices with many categorical columns: the
  [Kaggle competition data](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)
  (free account needed).

## Run it yourself

```bash
pip install numpy pandas scikit-learn
python train.py
```
Keep notebooks for exploration, but put the final pipeline in a script you can rerun from scratch.
