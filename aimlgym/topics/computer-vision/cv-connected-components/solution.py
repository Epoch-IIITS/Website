r"""Reference solution for CV-25 Connected Components with OpenCV.

OpenCV labels every pixel and returns one stats row and centroid per label. Skipping label 0
removes the background; the area filter drops speckles; the remaining rows are converted to plain
ints and floats.
"""
import cv2
import numpy as np


def label_objects(mask, connectivity=8, min_area=1):
    if not isinstance(mask, np.ndarray) or mask.ndim != 2 or mask.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 mask")
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    n, _, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=connectivity)
    areas, boxes, centres = [], [], []
    for i in range(1, n):
        x, y, w, h, area = (int(v) for v in stats[i])
        if area < min_area:
            continue
        areas.append(area)
        boxes.append((x, y, w, h))
        centres.append((float(centroids[i][0]), float(centroids[i][1])))
    return {"count": len(areas), "areas": areas, "boxes": boxes, "centroids": centres}
