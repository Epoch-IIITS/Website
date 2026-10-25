r"""Reference solution for CV-16 Image Quality: MSE and PSNR.

Converting to float before subtracting avoids uint8 wrap-around. OpenCV's PSNR uses the 8-bit peak
of 255; zero error is reported as infinity instead of OpenCV's large finite stand-in.
"""
import math

import cv2
import numpy as np


def image_quality(reference, distorted):
    if reference.shape != distorted.shape or reference.dtype != np.uint8 or distorted.dtype != np.uint8:
        raise ValueError("need two uint8 images of the same shape")
    diff = reference.astype(np.float64) - distorted.astype(np.float64)
    mse = float(np.mean(diff ** 2))
    return {"mse": mse, "psnr": math.inf if mse == 0 else float(cv2.PSNR(reference, distorted))}
