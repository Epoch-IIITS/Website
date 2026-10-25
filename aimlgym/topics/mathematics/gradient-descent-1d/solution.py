r"""Reference solution for MA-13 Gradient Descent in 1D.

Each iteration computes the step from the current slope, moves against it, and records the new
point. The loop ends on a tiny step (converged), a non-finite value (diverged) or the step cap,
so it always terminates.
"""
import math


def gradient_descent(df, x0, lr, max_steps=1000, tol=1e-8):
    if lr <= 0:
        raise ValueError("lr must be positive")
    if max_steps < 1:
        raise ValueError("max_steps must be >= 1")
    x = x0
    history = [x]
    for _ in range(max_steps):
        step = lr * df(x)
        x = x - step
        history.append(x)
        if not math.isfinite(x) or abs(step) < tol:
            break
    return x, history
