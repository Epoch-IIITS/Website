r"""Reference solution for ST-16 Chi-Square Goodness of Fit by Hand.

After validation, expected counts are the total times each probability. The statistic sums the
squared gaps scaled by expected counts; df is one less than the number of categories because the
counts are constrained to sum to N. The optional critical value turns the statistic into a decision.
"""
def chi_square_gof(observed, probs, critical=None):
    if len(observed) != len(probs):
        raise ValueError("observed and probs must match in length")
    if len(observed) < 2:
        raise ValueError("need at least two categories")
    if any(p <= 0 for p in probs) or abs(sum(probs) - 1) > 1e-9:
        raise ValueError("probs must be positive and sum to 1")
    if any(o < 0 for o in observed):
        raise ValueError("counts must be non-negative")
    total = sum(observed)
    if total == 0:
        raise ValueError("total count is zero")
    expected = [total * p for p in probs]
    stat = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
    return {"statistic": stat, "df": len(observed) - 1, "expected": expected,
            "reject": None if critical is None else stat > critical}
