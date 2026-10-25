r"""Reference solution for CV-20 Contours and Bounding Boxes.

`RETR_EXTERNAL` gives one contour per separate blob; bounding box, polygon area and moments
describe each one. Degenerate contours (a line or a single pixel) have zero area, so their centre
falls back to the middle of the bounding box. Sorting gives a stable, top-to-bottom order.
"""
import cv2
import numpy as np


def find_objects(mask, min_area=0):
    if not isinstance(mask, np.ndarray) or mask.ndim != 2 or mask.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 mask")
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for c in contours:
        x, y, w, h = (int(v) for v in cv2.boundingRect(c))
        area = float(cv2.contourArea(c))
        if area < min_area:
            continue
        m = cv2.moments(c)
        if m["m00"] > 0:
            centroid = (m["m10"] / m["m00"], m["m01"] / m["m00"])
        else:
            centroid = (x + (w - 1) / 2, y + (h - 1) / 2)
        objects.append({"x": x, "y": y, "w": w, "h": h, "area": area, "centroid": centroid})
    return sorted(objects, key=lambda o: (o["y"], o["x"]))
