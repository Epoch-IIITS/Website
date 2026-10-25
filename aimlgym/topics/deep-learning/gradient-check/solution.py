r"""Reference solution for DL-13 Gradient Checking by Hand.

Every coordinate is perturbed on fresh copies, giving a central-difference gradient of any shape.
The relative error compares it with the analytic gradient in a scale-free way, and the worst
coordinate is reported to help locate bugs.
"""
import numpy as np


def relative_error(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    r = np.abs(a - b) / np.maximum(np.abs(a) + np.abs(b), 1e-12)
    return r if r.ndim else float(r)


def grad_check(f, grad, x, h=1e-5):
    x = np.asarray(x, dtype=float)
    analytic = np.asarray(grad(x.copy()), dtype=float)
    num = np.zeros_like(x)
    for idx in np.ndindex(x.shape):
        xp = x.copy(); xm = x.copy()
        xp[idx] += h
        xm[idx] -= h
        num[idx] = (f(xp) - f(xm)) / (2 * h)
    rel = np.asarray(relative_error(analytic, num))
    worst = tuple(int(i) for i in np.unravel_index(int(np.argmax(rel)), x.shape))
    return {"max_rel_error": float(rel.max()), "worst_index": worst, "numerical": num}
