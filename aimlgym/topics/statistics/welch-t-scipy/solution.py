r"""Reference solution for ST-17 Welch's t-test with SciPy.

`ttest_ind(..., equal_var=False)` is Welch's test; the alternative is passed straight through.
SciPy would return `nan` when both samples are constant, so that case is rejected first. The mean
difference is reported because a p-value alone says nothing about how large the effect is.
"""
from scipy import stats


def _variance(values):
    m = sum(values) / len(values)
    return sum((v - m) ** 2 for v in values) / (len(values) - 1)


def compare_means(x, y, alternative="two-sided", alpha=0.05):
    if len(x) < 2 or len(y) < 2:
        raise ValueError("each sample needs at least two values")
    if alternative not in ("two-sided", "less", "greater"):
        raise ValueError("unknown alternative")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if _variance(x) == 0 and _variance(y) == 0:
        raise ValueError("both samples have zero variance")
    result = stats.ttest_ind(x, y, equal_var=False, alternative=alternative)
    p_value = float(result.pvalue)
    return {"mean_diff": sum(x) / len(x) - sum(y) / len(y), "t": float(result.statistic),
            "df": float(result.df), "p_value": p_value, "reject": p_value < alpha}
