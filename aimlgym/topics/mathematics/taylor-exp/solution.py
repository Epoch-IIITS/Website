r"""Reference solution for MA-15 Taylor Series for exp(x).

Both functions keep the current term and multiply it by x/k to get the next one, which is exact
algebra and avoids huge factorials. `terms_needed` advances until the first omitted term is below
the tolerance and reports how many terms were included.
"""
def exp_taylor(x, n_terms):
    if n_terms < 0:
        raise ValueError("n_terms must be >= 0")
    total = 0.0
    term = 1.0
    for k in range(n_terms):
        total += term
        term *= x / (k + 1)
    return total


def terms_needed(x, tol):
    if tol <= 0:
        raise ValueError("tol must be positive")
    n = 0
    t = 1.0
    while abs(t) >= tol:
        n += 1
        t *= x / n
    return n
