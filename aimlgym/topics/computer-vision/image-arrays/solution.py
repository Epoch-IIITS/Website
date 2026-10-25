r"""Reference solution for CV-01 Images as Arrays.

All arithmetic happens in float so nothing wraps around; one helper rounds, clips and converts
back to `uint8`. Normalisation is a division by 255 and its inverse a multiplication.
Transposing the axes moves the channel dimension without copying pixel values.
"""
import numpy as np


def image_info(img):
    img = np.asarray(img)
    return {"height": img.shape[0], "width": img.shape[1],
            "channels": img.shape[2] if img.ndim == 3 else 1, "dtype": str(img.dtype)}


def _clip_uint8(x):
    return np.clip(np.rint(x), 0, 255).astype(np.uint8)


def adjust(img, brightness=0, contrast=1.0):
    out = (np.asarray(img, dtype=float) - 128) * contrast + 128 + brightness
    return _clip_uint8(out)


def to_float(img):
    return np.asarray(img, dtype=float) / 255.0


def to_uint8(x):
    return _clip_uint8(np.asarray(x, dtype=float) * 255.0)


def channels_first(img):
    img = np.asarray(img)
    if img.ndim != 3:
        raise ValueError("expected (H, W, C)")
    return np.transpose(img, (2, 0, 1))


def channels_last(x):
    x = np.asarray(x)
    if x.ndim != 3:
        raise ValueError("expected (C, H, W)")
    return np.transpose(x, (1, 2, 0))
