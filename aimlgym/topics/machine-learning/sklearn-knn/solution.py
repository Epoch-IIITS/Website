r"""Reference solution for ML-12 k-Nearest Neighbours with scikit-learn.

Each k gets its own freshly fitted pipeline, so scaling statistics always come from the training
rows. The best k is chosen by sorting on negative accuracy and then on k, which resolves ties
towards the simpler, smaller neighbourhood.
"""
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def knn_accuracy_by_k(X_train, y_train, X_test, y_test, ks):
    if not ks or any(k < 1 or k > len(X_train) for k in ks):
        raise ValueError("each k must be between 1 and the number of training rows")
    accuracy = {}
    for k in ks:
        pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
        pipe.fit(X_train, y_train)
        accuracy[k] = float(accuracy_score(y_test, pipe.predict(X_test)))
    best_k = min(ks, key=lambda k: (-accuracy[k], k))
    return {"accuracy": accuracy, "best_k": best_k}
