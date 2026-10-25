# k-Means and Silhouette Scores

## Learning outcomes

After this lesson you can:

- Cluster data with KMeans and read labels_, cluster_centers_ and inertia_
- Compare numbers of clusters with inertia and silhouette scores
- Make clustering reproducible with n_init and random_state

## Intuition
k-means places k centres and assigns every point to the nearest one, then moves each centre to
the mean of its points, repeating until nothing changes. The hard part is choosing k: more
clusters always fit tighter, so you need a score that also rewards clusters being far apart.

## Precise explanation
```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
km.labels_, km.cluster_centers_, km.inertia_
silhouette_score(X, km.labels_)
```

* **Inertia** is the sum of squared distances from points to their centre. It never increases as
  k grows (with enough restarts), so the "elbow" where it stops dropping quickly is only a hint.
* **Silhouette** for one point: (b − a)/max(a, b), where a is the mean distance to its own cluster
  and b the mean distance to the nearest other cluster. The average lies in [−1, 1]; higher means
  compact, well-separated clusters. It needs at least 2 clusters.
* k-means can stop at a poor local optimum; `n_init=10` runs ten random starts and keeps the
  lowest inertia. `random_state` makes those starts reproducible.
* Scale features first: k-means uses Euclidean distance.

## Worked example
Three well-separated blobs: inertia drops sharply from k = 2 to k = 3 and slowly afterwards; the
silhouette is highest at k = 3 (about 0.7) and lower at k = 2 and k = 4.

## What the library does inside
Lloyd's algorithm from ML-26 (the optional deep dive after this step), with "k-means++"
starting centres that are spread out, several restarts, and vectorised distance computations.

## Common mistakes
* Interpreting cluster numbers as meaningful (label 0 in one run may be label 2 in another).
* Choosing k by inertia alone, which always prefers more clusters.
* Clustering unscaled features with very different ranges.

## Why this matters
Clustering segments customers, groups documents and initialises other models; silhouette analysis
is the standard sanity check when no labels exist.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
