r"""Reference solution for MA-14 Numerical Gradient of f(x1..xn).

Each partial derivative perturbs a fresh copy of x along one axis in both directions, so x itself
is never changed. `gd_step` combines the gradient with the descent update element-wise.
"""
def numerical_gradient(f, x, h=1e-5):
    if h <= 0:
        raise ValueError("h must be positive")
    grad = []
    for i in range(len(x)):
        xp = list(x)
        xm = list(x)
        xp[i] += h
        xm[i] -= h
        grad.append((f(xp) - f(xm)) / (2 * h))
    return grad


def gd_step(f, x, lr):
    g = numerical_gradient(f, x)
    return [xi - lr * gi for xi, gi in zip(x, g)]
