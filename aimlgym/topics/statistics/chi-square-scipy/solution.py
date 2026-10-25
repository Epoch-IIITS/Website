r"""Reference solution for ST-15 Chi-Square Test with SciPy.

SciPy needs expected counts, so the probabilities are scaled by the total. `chisquare` returns the
statistic and the upper-tail probability under the chi-square distribution with k − 1 degrees of
freedom; comparing that p-value with α replaces the table lookup of a critical value.
"""
from scipy import stats


def chi_square_test(observed, probs, alpha=0.05):
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if len(observed) != len(probs) or len(observed) < 2:
        raise ValueError("need matching observed and probs with at least two categories")
    if any(p <= 0 for p in probs) or abs(sum(probs) - 1) > 1e-9:
        raise ValueError("probs must be positive and sum to 1")
    if any(o < 0 for o in observed):
        raise ValueError("counts must be non-negative")
    total = sum(observed)
    if total == 0:
        raise ValueError("total count is zero")
    expected = [total * p for p in probs]
    result = stats.chisquare(observed, f_exp=expected)
    p_value = float(result.pvalue)
    return {"statistic": float(result.statistic), "p_value": p_value,
            "df": len(observed) - 1, "reject": p_value < alpha}
