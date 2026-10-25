r"""Reference solution for XA-13 Minimal Counterfactual Search.

All step combinations are generated (immutable features fixed at 0), sorted by cost and then
lexicographically, and evaluated in one batch. The first in-bounds candidate whose predicted label
differs from the original is, by construction, a minimum-cost counterfactual.
"""
from itertools import product

import numpy as np


def find_counterfactual(predict, x, steps, max_steps=3, lower=None, upper=None):
    x = np.asarray(x, dtype=float)
    steps = np.asarray(steps, dtype=float)
    if steps.shape != x.shape or max_steps < 1:
        raise ValueError("steps must match x and max_steps must be >= 1")
    c = predict(x[None, :])[0]
    ranges = [range(-max_steps, max_steps + 1) if s != 0 else (0,) for s in steps]
    ks = sorted((k for k in product(*ranges) if any(k)), key=lambda k: (sum(abs(v) for v in k), k))
    if not ks:
        return None
    K = np.array(ks, dtype=float)
    cands = x + K * steps
    ok = np.ones(len(cands), dtype=bool)
    if lower is not None:
        ok &= (cands >= np.asarray(lower, dtype=float)).all(axis=1)
    if upper is not None:
        ok &= (cands <= np.asarray(upper, dtype=float)).all(axis=1)
    labels = predict(cands)
    for i in range(len(ks)):
        if ok[i] and labels[i] != c:
            return {"x_cf": cands[i], "k": tuple(int(v) for v in ks[i]), "cost": int(sum(abs(v) for v in ks[i])),
                    "label": labels[i]}
    return None
