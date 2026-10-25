r"""Reference solution for MA-12 Trapezoidal Integration.

The endpoints are weighted by ½ and each interior point by 1, then everything is multiplied by
the strip width h. Points are computed as `a + i*h` to avoid accumulated rounding. A negative h
(for a > b) automatically gives a negative integral.
"""
def trapezoid(f, a, b, n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive int")
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        total += f(a + i * h)
    return total * h
