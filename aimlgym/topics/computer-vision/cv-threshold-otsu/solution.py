r"""Reference solution for CV-06 Thresholding and Otsu's Method.

One `cv2.threshold` call covers both cases; adding the Otsu flag makes OpenCV choose the
threshold from the histogram and return it. Inversion only swaps which side becomes 255.
"""
import cv2
import numpy as np


def binarise(gray, threshold=None, invert=False):
    if not isinstance(gray, np.ndarray) or gray.ndim != 2 or gray.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 image")
    kind = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    if threshold is None:
        t, mask = cv2.threshold(gray, 0, 255, kind + cv2.THRESH_OTSU)
    else:
        t, mask = cv2.threshold(gray, threshold, 255, kind)
    return float(t), mask
