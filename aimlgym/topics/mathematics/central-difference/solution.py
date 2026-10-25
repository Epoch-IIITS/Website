r"""Reference solution for MA-10 Numerical Derivative (Central Difference).

Both functions translate their formulas directly. The central version evaluates symmetrically
around x, so the leading error term cancels and the estimate is far more accurate for the same h.
"""
def forward_diff(f, x, h=1e-6):
    if h <= 0:
        raise ValueError("h must be positive")
    return (f(x + h) - f(x)) / h


def central_diff(f, x, h=1e-5):
    if h <= 0:
        raise ValueError("h must be positive")
    return (f(x + h) - f(x - h)) / (2 * h)
