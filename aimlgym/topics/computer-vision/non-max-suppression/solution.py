r"""Reference solution for CV-24 Non-Maximum Suppression.

Candidates are processed in descending score order. Each iteration keeps the best remaining box
and filters out the rest that overlap it beyond the threshold, so every kept box suppresses its
own duplicates.
"""
import numpy as np


def _iou_one(b, many):
    x1 = np.maximum(b[0], many[:, 0]); y1 = np.maximum(b[1], many[:, 1])
    x2 = np.minimum(b[2], many[:, 2]); y2 = np.minimum(b[3], many[:, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    area_m = (many[:, 2] - many[:, 0]) * (many[:, 3] - many[:, 1])
    return inter / (area_b + area_m - inter)


def nms(boxes, scores, iou_threshold=0.5, score_threshold=0.0):
    boxes = np.asarray(boxes, dtype=float).reshape(-1, 4)
    scores = np.asarray(scores, dtype=float)
    if len(scores) != len(boxes):
        raise ValueError("boxes and scores must have the same length")
    order = np.argsort(-scores, kind="stable")
    order = order[scores[order] >= score_threshold]
    keep = []
    while order.size:
        i = int(order[0])
        keep.append(i)
        rest = order[1:]
        if rest.size == 0:
            break
        order = rest[_iou_one(boxes[i], boxes[rest]) <= iou_threshold]
    return keep
