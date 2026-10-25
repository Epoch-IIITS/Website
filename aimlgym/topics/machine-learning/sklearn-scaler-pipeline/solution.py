r"""Reference solution for ML-07 Scaling inside a Pipeline.

Fitting the pipeline fits the scaler on the training rows only and trains the model on the scaled
rows; predicting transforms the test rows with the stored training statistics before the model
sees them. Building the pipeline inside the function keeps calls independent.
"""
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def train_and_predict(X_train, y_train, X_test):
    pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
    pipe.fit(X_train, y_train)
    return pipe, [int(v) for v in pipe.predict(X_test)]
