r"""Reference solution for CV-09 Intensity Histogram.

`bincount` counts each of the 256 intensities. The cumulative counts define a monotone lookup table
that maps the darkest present value to 0 and the brightest to 255; fancy indexing applies the table
to all pixels.
"""
import numpy as np


def histogram256(gray):
    gray = np.asarray(gray)
    if gray.dtype != np.uint8:
        raise ValueError("expected a uint8 image")
    return np.bincount(gray.ravel(), minlength=256)


def cdf(hist):
    return np.cumsum(np.asarray(hist))


def equalize(gray):
    gray = np.asarray(gray)
    c = cdf(histogram256(gray))
    n = gray.size
    c_min = c[c > 0].min()
    if n == c_min:
        return gray.copy()
    lut = np.rint((c - c_min) / (n - c_min) * 255)
    lut = np.clip(lut, 0, 255).astype(np.uint8)
    return lut[gray]
