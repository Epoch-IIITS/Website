import numpy as np


def image_info(img):
    img = np.asarray(img)
    # TODO
    return {}


def adjust(img, brightness=0, contrast=1.0):
    # TODO: compute in float, round, clip, convert
    return np.asarray(img) + brightness


def to_float(img):
    # TODO
    return np.asarray(img)


def to_uint8(x):
    # TODO
    return np.asarray(x).astype(np.uint8)


def channels_first(img):
    # TODO
    return img


def channels_last(x):
    # TODO
    return x
