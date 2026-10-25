r"""Reference solution for CV-26 Connected Components Labeling by Hand.

A raster scan finds the first pixel of each new component, which fixes the label order. BFS with a
deque floods the component, labelling pixels as they are enqueued so none is visited twice, and
counts its size.
"""
from collections import deque

import numpy as np

N4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
N8 = N4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def label_components(mask, connectivity=4):
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    mask = np.asarray(mask, dtype=bool)
    H, W = mask.shape
    labels = np.zeros((H, W), dtype=int)
    offsets = N4 if connectivity == 4 else N8
    sizes = []
    for r in range(H):
        for c in range(W):
            if mask[r, c] and labels[r, c] == 0:
                lab = len(sizes) + 1
                labels[r, c] = lab
                q = deque([(r, c)])
                count = 0
                while q:
                    y, x = q.popleft()
                    count += 1
                    for dy, dx in offsets:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and labels[ny, nx] == 0:
                            labels[ny, nx] = lab
                            q.append((ny, nx))
                sizes.append(count)
    return labels, sizes
