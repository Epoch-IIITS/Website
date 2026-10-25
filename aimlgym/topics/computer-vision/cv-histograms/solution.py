r"""Reference solution for CV-08 Histograms and Equalisation.

`calcHist` counts pixels in equal-width bins across [0, 256); flattening and converting gives a
plain list of counts. `equalizeHist` remaps intensities through the cumulative histogram so the
output spreads over the full range.
"""
import cv2
import numpy as np


def histogram_and_equalise(gray, bins=256):
    if not isinstance(gray, np.ndarray) or gray.ndim != 2 or gray.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 image")
    if not 1 <= bins <= 256:
        raise ValueError("bins must be between 1 and 256")
    hist = cv2.calcHist([gray], [0], None, [bins], [0, 256])
    return {"hist": [int(v) for v in hist.ravel()], "equalized": cv2.equalizeHist(gray)}
