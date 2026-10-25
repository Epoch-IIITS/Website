r"""Reference solution for FL-13 Differentially Private Aggregation.

Clipping bounds each client's contribution; averaging over m clients divides the sensitivity by m;
Gaussian noise with standard deviation z·C/m is then added to the mean. Skipping the draw when σ = 0
keeps the noiseless path exact and leaves the generator untouched.
"""
import numpy as np


def _clip(d, c):
    d = np.asarray(d, dtype=float)
    n = float(np.linalg.norm(d))
    return d if n <= c else d * (c / n)


def dp_mean(deltas, clip_norm, noise_multiplier, rng):
    if not deltas or clip_norm <= 0 or noise_multiplier < 0:
        raise ValueError("invalid arguments")
    clipped = np.array([_clip(d, clip_norm) for d in deltas])
    clean = clipped.mean(axis=0)
    sigma = noise_multiplier * clip_norm / len(deltas)
    if sigma == 0:
        return clean.copy(), clean, 0.0
    return clean + rng.normal(0.0, sigma, size=clean.shape), clean, float(sigma)
