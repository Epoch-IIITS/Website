r"""Reference solution for CV-22 Data Augmentation.

Each augmentation draws its random choices from the generator in a fixed order, so the same seed
always produces the same batch. Flip and shift rearrange pixels; the brightness change is done in
float and clipped so no value wraps around.
"""
import cv2
import numpy as np


def augment(image, rng, max_shift=2):
    if not isinstance(image, np.ndarray) or image.dtype != np.uint8:
        raise ValueError("expected a uint8 image")
    h, w = image.shape[:2]
    if rng.random() < 0.5:
        image = cv2.flip(image, 1)
    dx, dy = rng.integers(-max_shift, max_shift + 1, size=2)
    image = cv2.warpAffine(image, np.float32([[1, 0, dx], [0, 1, dy]]), (w, h))
    factor = rng.uniform(0.8, 1.2)
    return np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)


def augment_batch(images, seed=0, max_shift=2):
    rng = np.random.default_rng(seed)
    return np.stack([augment(image, rng, max_shift) for image in images])
