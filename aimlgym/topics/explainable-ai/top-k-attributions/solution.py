r"""Reference solution for XA-02 Ranking Attributions.

Ranking uses absolute values with an alphabetical tie-break; each entry reports the signed value,
its direction and its share of the total absolute effect.
"""
import numpy as np


def top_attributions(names, phi, k=3):
    phi = np.asarray(phi, dtype=float)
    if len(names) != len(phi):
        raise ValueError("names and phi must have the same length")
    if k < 1:
        raise ValueError("k must be >= 1")
    total = float(np.abs(phi).sum())
    order = sorted(range(len(phi)), key=lambda i: (-abs(phi[i]), names[i]))
    out = []
    for i in order[:k]:
        v = float(phi[i])
        d = "+" if v > 0 else "-" if v < 0 else "0"
        out.append((names[i], v, d, abs(v) / total if total else 0.0))
    return out
