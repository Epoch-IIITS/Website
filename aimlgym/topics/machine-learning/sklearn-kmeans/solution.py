r"""Reference solution for ML-25 k-Means and Silhouette Scores.

Each k gets ten seeded restarts and keeps the best; inertia measures tightness and the silhouette
balances tightness against separation. Selecting the highest silhouette (smaller k on ties) gives a
reproducible choice, and the labels come from that same fitted model.
"""
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def choose_k(X, ks, seed=0):
    if not ks or any(k < 2 or k >= len(X) for k in ks):
        raise ValueError("each k must satisfy 2 <= k < number of rows")
    models, inertia, silhouette = [], [], []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(X)
        models.append(km)
        inertia.append(float(km.inertia_))
        silhouette.append(float(silhouette_score(X, km.labels_)))
    best = max(range(len(ks)), key=lambda i: (silhouette[i], -ks[i]))
    return {"inertia": inertia, "silhouette": silhouette, "best_k": int(ks[best]),
            "labels": [int(v) for v in models[best].labels_]}
