r"""Reference solution for ML-04 Splitting Data with scikit-learn.

One `train_test_split` call shuffles all arrays with the same permutation, so features and labels
stay aligned; `stratify` makes the split per class. `StratifiedShuffleSplit` yields index arrays,
which are converted to lists of plain ints.
"""
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split


def split_data(X, y, test_size=0.25, seed=0, stratify=False):
    if len(X) != len(y):
        raise ValueError("X and y must have the same length")
    return train_test_split(X, y, test_size=test_size, random_state=seed,
                            stratify=y if stratify else None)


def stratified_splits(X, y, n_splits=3, test_size=0.25, seed=0):
    if len(X) != len(y):
        raise ValueError("X and y must have the same length")
    splitter = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=seed)
    return [([int(i) for i in train], [int(i) for i in test]) for train, test in splitter.split(X, y)]
