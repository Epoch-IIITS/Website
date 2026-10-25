r"""Reference solution for CV-03 OpenCV Basics: BGR, dtypes and Indexing.

`cvtColor` handles the channel order and the greyscale weights. The crop converts OpenCV's (x, y,
w, h) rectangle into NumPy's row-then-column slice and copies it so the caller can modify the crop
without touching the original.
"""
import cv2
import numpy as np


def to_rgb_and_gray(bgr):
    if not isinstance(bgr, np.ndarray) or bgr.dtype != np.uint8 or bgr.ndim != 3 or bgr.shape[2] != 3:
        raise ValueError("expected a uint8 BGR image of shape (h, w, 3)")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB), cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)


def crop(image, x, y, w, h):
    height, width = image.shape[:2]
    if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > width or y + h > height:
        raise ValueError("rectangle does not fit inside the image")
    return image[y:y + h, x:x + w].copy()
