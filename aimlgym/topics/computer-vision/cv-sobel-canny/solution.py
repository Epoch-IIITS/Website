r"""Reference solution for CV-11 Edges with Sobel and Canny.

Sobel with a float depth keeps the sign of the gradient; the magnitude combines both directions.
Canny runs on a blurred copy so that noise does not produce spurious edges, and returns a binary
mask of thin, connected edges.
"""
import cv2
import numpy as np


def edges(gray, low, high, blur_ksize=5):
    if not isinstance(gray, np.ndarray) or gray.ndim != 2 or gray.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 image")
    if not 0 <= low <= high:
        raise ValueError("need 0 <= low <= high")
    if blur_ksize < 1 or blur_ksize % 2 != 1:
        raise ValueError("blur_ksize must be a positive odd integer")
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    blurred = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    return {"gx": gx, "gy": gy, "magnitude": np.hypot(gx, gy), "canny": cv2.Canny(blurred, low, high)}
