r"""Reference solution for XA-07 Permutation Importance with sklearn.inspection.

The function shuffles each original column of the DataFrame several times, measures the drop in score
of the whole pipeline, and reports the mean and spread per column, most important first.
"""
import pandas as pd
from sklearn.inspection import permutation_importance


def importance_table(model, X, y, n_repeats=10, seed=0, scoring=None):
    if not isinstance(X, pd.DataFrame) or n_repeats < 1:
        raise ValueError("need a DataFrame and n_repeats >= 1")
    result = permutation_importance(model, X, y, n_repeats=n_repeats, random_state=seed, scoring=scoring)
    rows = [(str(c), float(m), float(s)) for c, m, s in zip(X.columns, result.importances_mean, result.importances_std)]
    return sorted(rows, key=lambda row: (-row[1], row[0]))
