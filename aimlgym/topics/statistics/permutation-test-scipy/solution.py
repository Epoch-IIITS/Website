r"""Reference solution for ST-19 Permutation Test with SciPy.

The statistic takes an `axis` so SciPy can evaluate many relabellings at once. For small samples
SciPy enumerates every split, giving an exact p-value; for larger ones the seed makes the random
resamples reproducible.
"""
from scipy import stats


def mean_diff(a, b, axis):
    return a.mean(axis=axis) - b.mean(axis=axis)


def permutation_mean_diff(x, y, alternative="two-sided", n_resamples=9999, seed=0):
    if len(x) == 0 or len(y) == 0:
        raise ValueError("samples must not be empty")
    if alternative not in ("two-sided", "less", "greater"):
        raise ValueError("unknown alternative")
    result = stats.permutation_test((x, y), mean_diff, permutation_type="independent",
                                    n_resamples=n_resamples, alternative=alternative,
                                    random_state=seed)
    return {"statistic": float(result.statistic), "p_value": float(result.pvalue)}
