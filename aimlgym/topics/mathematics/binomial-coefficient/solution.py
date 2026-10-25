r"""Reference solution for MA-07 Binomial Coefficient.

After the edge cases, symmetry halves the work. Multiplying before the integer division keeps
the intermediate value an exact product of consecutive binomial coefficients, so `//` never
truncates. Python's arbitrary-precision ints keep large results exact.
"""
def comb(n, k):
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative")
    if k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r
