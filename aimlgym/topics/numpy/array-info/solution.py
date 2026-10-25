r"""Reference solution for NP-01 Create an Array and Inspect It.

An explicit row-length check gives a clear error message (NumPy would also raise). `describe`
converts NumPy's attributes into plain Python types so they compare cleanly in tests.
"""
import numpy as np


def to_array(rows, dtype=float):
    if isinstance(rows, (list, tuple)) and rows and isinstance(rows[0], (list, tuple)):
        n = len(rows[0])
        if any(len(r) != n for r in rows):
            raise ValueError("ragged rows")
    return np.array(rows, dtype=dtype)


def describe(a):
    return {"shape": tuple(a.shape), "ndim": int(a.ndim), "size": int(a.size),
            "dtype": str(a.dtype)}
