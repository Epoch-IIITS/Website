r"""Reference solution for CV-23 Intersection over Union.

Broadcasting A against B produces all pairwise intersection rectangles at once; clipping makes
non-overlapping pairs contribute zero. Union follows from inclusion–exclusion.
"""
import numpy as np


def box_area(boxes):
    b = np.asarray(boxes, dtype=float).reshape(-1, 4)
    if ((b[:, 2] <= b[:, 0]) | (b[:, 3] <= b[:, 1])).any():
        raise ValueError("boxes must satisfy x2 > x1 and y2 > y1")
    return (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])


def iou_matrix(A, B):
    A = np.asarray(A, dtype=float).reshape(-1, 4)
    B = np.asarray(B, dtype=float).reshape(-1, 4)
    area_a, area_b = box_area(A), box_area(B)
    ix1 = np.maximum(A[:, None, 0], B[None, :, 0])
    iy1 = np.maximum(A[:, None, 1], B[None, :, 1])
    ix2 = np.minimum(A[:, None, 2], B[None, :, 2])
    iy2 = np.minimum(A[:, None, 3], B[None, :, 3])
    inter = np.clip(ix2 - ix1, 0, None) * np.clip(iy2 - iy1, 0, None)
    return inter / (area_a[:, None] + area_b[None, :] - inter)
