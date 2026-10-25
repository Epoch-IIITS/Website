r"""Reference solution for ML-18 Pipelines and ColumnTransformer.

Two small pipelines handle the column types; the ColumnTransformer applies each to its columns
and concatenates the outputs; the outer pipeline adds the model. Everything is learned in `fit`
from the training rows, so the same object can predict on new DataFrames safely.
"""
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_model(numeric, categorical):
    if not numeric and not categorical:
        raise ValueError("need at least one column")
    if set(numeric) & set(categorical):
        raise ValueError("a column cannot be both numeric and categorical")
    numeric_pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
    categorical_pipe = make_pipeline(SimpleImputer(strategy="most_frequent"),
                                     OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    prep = ColumnTransformer([("num", numeric_pipe, list(numeric)), ("cat", categorical_pipe, list(categorical))])
    return Pipeline([("prep", prep), ("model", LinearRegression())])
