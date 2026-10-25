r"""Reference solution for ST-01 Mean and Variance (Population vs Sample).

The mean is computed first, then the sum of squared deviations from it. The only difference
between population and sample variance is the denominator. Validation prevents division by zero.
"""
def mean_variance(data, sample=False):
    n = len(data)
    if n == 0:
        raise ValueError("data must be non-empty")
    if sample and n < 2:
        raise ValueError("sample variance needs at least two values")
    m = sum(data) / n
    ss = sum((x - m) ** 2 for x in data)
    return float(m), ss / (n - 1 if sample else n)
