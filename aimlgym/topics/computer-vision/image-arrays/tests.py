"""Tests for CV-01 Images as Arrays.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import importlib
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = importlib.import_module(os.environ.get("AIMLGYM_TARGET", "solution"))


import numpy as np


class TestImageArrays(unittest.TestCase):
    def test_info(self):
        self.assertEqual(S.image_info(np.zeros((4, 6, 3), dtype=np.uint8)),
                         {"height": 4, "width": 6, "channels": 3, "dtype": "uint8"})
        self.assertEqual(S.image_info(np.zeros((2, 5)))["channels"], 1)

    def test_brightness_no_wraparound(self):
        img = np.array([[250, 0, 10]], dtype=np.uint8)
        out = S.adjust(img, brightness=10)
        self.assertEqual(out.dtype, np.uint8)
        np.testing.assert_array_equal(out, [[255, 10, 20]])
        np.testing.assert_array_equal(S.adjust(img, brightness=-20), [[230, 0, 0]])

    def test_contrast(self):
        img = np.array([[0, 100, 128, 200, 255]], dtype=np.uint8)
        np.testing.assert_array_equal(S.adjust(img, contrast=2.0), [[0, 72, 128, 255, 255]])
        np.testing.assert_array_equal(S.adjust(img, contrast=0.5), [[64, 114, 128, 164, 192]])

    def test_float_round_trip(self):
        img = np.arange(256, dtype=np.uint8).reshape(16, 16)
        f = S.to_float(img)
        self.assertEqual(f.dtype, np.float64)
        self.assertAlmostEqual(f.max(), 1.0)
        np.testing.assert_array_equal(S.to_uint8(f), img)

    def test_to_uint8_rounds_and_clips(self):
        np.testing.assert_array_equal(S.to_uint8(np.array([0.5, -0.2, 1.3, 127.6 / 255])), [128, 0, 255, 128])

    def test_channels(self):
        img = np.arange(2 * 3 * 3).reshape(2, 3, 3)
        cf = S.channels_first(img)
        self.assertEqual(cf.shape, (3, 2, 3))
        np.testing.assert_array_equal(cf[1], img[:, :, 1])
        np.testing.assert_array_equal(S.channels_last(cf), img)
        with self.assertRaises(ValueError):
            S.channels_first(np.zeros((4, 4)))


try:
    import torch
except ImportError:
    torch = None


class TestAgainstLibrary(unittest.TestCase):
    def test_uint8_saturation_matches_numpy_clip(self):
        img = np.array([[5, 200, 250]], dtype=np.uint8)
        expected = np.clip(img.astype(int) + 30, 0, 255).astype(np.uint8)
        np.testing.assert_array_equal(S.adjust(img, brightness=30), expected)

    @unittest.skipIf(torch is None, "PyTorch not installed")
    def test_matches_torch_layout(self):
        img = np.arange(4 * 5 * 3, dtype=np.uint8).reshape(4, 5, 3)
        ours = S.channels_first(S.to_float(img))
        theirs = (torch.from_numpy(img).permute(2, 0, 1).double() / 255).numpy()
        np.testing.assert_allclose(ours, theirs)


if __name__ == "__main__":
    unittest.main()
