r"""Reference solution for PY-19 Validated Factorial.

Type validation comes before value validation so that comparing `n < 0` is never attempted on,
say, a string. `bool` is rejected explicitly because it is a subclass of `int`. The loop starts
at 2 because multiplying by 1 changes nothing; for n = 0 or 1 the loop body never runs and the
empty product 1 is returned.
"""
def factorial(n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result
