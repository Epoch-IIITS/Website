r"""Reference solution for MA-04 Dot Product.

Length validation protects against `zip` silently truncating. The accumulator starts at 0 (the
additive identity), so empty vectors correctly give 0, and each pair contributes its product.
"""
def dot(u, v):
    if len(u) != len(v):
        raise ValueError("vectors must have the same length")
    total = 0
    for a, b in zip(u, v):
        total += a * b
    return total
