r"""Reference solution for ML-27 Capstone: an End-to-End Tabular Model.

The split happens first, so the grid search, imputers, scaler and encoder only ever see training
rows. The search picks C by cross-validated AUC and refits on the whole training set; the test set
is used exactly once, next to a majority-class baseline that shows what the scores mean.
"""
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def end_to_end(df, target, numeric, categorical, seed=0):
    if target not in df.columns or set(df[target].unique()) != {0, 1}:
        raise ValueError("target must be a binary 0/1 column of df")
    X, y = df.drop(columns=[target]), df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)
    prep = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), list(numeric)),
        ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                              OneHotEncoder(handle_unknown="ignore", sparse_output=False)), list(categorical)),
    ])
    pipe = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))])
    search = GridSearchCV(pipe, {"model__C": [0.01, 0.1, 1, 10]},
                          cv=StratifiedKFold(5, shuffle=True, random_state=seed), scoring="roc_auc")
    search.fit(X_train, y_train)
    best = search.best_estimator_
    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    return {"best_C": float(search.best_params_["model__C"]), "cv_auc": float(search.best_score_),
            "test_accuracy": float(best.score(X_test, y_test)),
            "test_auc": float(roc_auc_score(y_test, best.predict_proba(X_test)[:, 1])),
            "baseline_accuracy": float(baseline.score(X_test, y_test)), "model": best}
