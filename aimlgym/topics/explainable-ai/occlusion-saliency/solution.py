r"""Reference solution for XA-09 Occlusion Saliency Map.

Each patch is occluded on a fresh copy; slicing past the edge automatically gives smaller edge
patches. The saliency is the score drop relative to the unoccluded image.
"""
import numpy as np


def occlusion_map(score_fn, img, patch=2, baseline=0.0):
    if patch < 1:
        raise ValueError("patch must be >= 1")
    img = np.asarray(img, dtype=float)
    H, W = img.shape
    Hp, Wp = -(-H // patch), -(-W // patch)
    base = float(score_fn(img))
    sal = np.zeros((Hp, Wp))
    for pi in range(Hp):
        for pj in range(Wp):
            occ = img.copy()
            occ[pi * patch:(pi + 1) * patch, pj * patch:(pj + 1) * patch] = baseline
            sal[pi, pj] = base - float(score_fn(occ))
    return sal
