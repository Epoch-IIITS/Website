r"""Reference solution for CV-18 Resizing with cv2.resize.

A dictionary maps readable names to OpenCV's interpolation flags. The only subtle part is the size
argument, which OpenCV takes as (width, height) although the result's shape is (height, width).
"""
import cv2
import numpy as np

METHODS = {"nearest": cv2.INTER_NEAREST, "linear": cv2.INTER_LINEAR,
           "cubic": cv2.INTER_CUBIC, "area": cv2.INTER_AREA}


def resize(image, width, height, method="linear"):
    if method not in METHODS:
        raise ValueError("unknown interpolation method " + str(method))
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    return cv2.resize(image, (width, height), interpolation=METHODS[method])
