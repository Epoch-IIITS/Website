r"""Reference solution for CV-04 Flips, Rotations and Affine Warps.

Flips and quarter turns are exact rearrangements. A rotation about the pixel-exact centre and a
pure translation are both affine matrices; `warpAffine` resamples the image through them into an
output of the original (width, height), filling uncovered pixels with zeros.
"""
import cv2
import numpy as np

OPS = {
    "flip_h": lambda img: cv2.flip(img, 1),
    "flip_v": lambda img: cv2.flip(img, 0),
    "rot90_cw": lambda img: cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
    "rot180": lambda img: cv2.rotate(img, cv2.ROTATE_180),
    "rot90_ccw": lambda img: cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE),
}


def transform(image, op):
    if op not in OPS:
        raise ValueError("unknown operation " + str(op))
    return OPS[op](image)


def rotate_about_centre(image, angle, scale=1.0):
    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D(((w - 1) / 2, (h - 1) / 2), angle, scale)
    return cv2.warpAffine(image, M, (w, h))


def translate(image, dx, dy):
    h, w = image.shape[:2]
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(image, M, (w, h))
