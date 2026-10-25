r"""Reference solution for ML-22 Decision Trees and Random Forests.

Both models are fitted with the same seed and depth limit, so the comparison isolates the effect
of averaging. `score` gives accuracy, `get_depth` shows how far the single tree grew, and the
forest's normalised impurity importances identify the feature it relied on most.
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


def compare_tree_forest(X_train, y_train, X_test, y_test, max_depth=None, n_estimators=100, seed=0):
    if n_estimators < 1:
        raise ValueError("n_estimators must be at least 1")
    tree = DecisionTreeClassifier(max_depth=max_depth, random_state=seed).fit(X_train, y_train)
    forest = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                    random_state=seed).fit(X_train, y_train)
    importances = [float(v) for v in forest.feature_importances_]
    return {"tree_train_accuracy": float(tree.score(X_train, y_train)),
            "tree_test_accuracy": float(tree.score(X_test, y_test)),
            "forest_test_accuracy": float(forest.score(X_test, y_test)),
            "tree_depth": int(tree.get_depth()), "top_feature": importances.index(max(importances)),
            "importances": importances}
