# Images as Arrays

## Learning outcomes

After this lesson you can:

- Describe an image as an (H, W) or (H, W, C) array and index pixels by (row, column)
- Avoid uint8 overflow when changing brightness and contrast
- Convert between uint8 [0, 255] and float [0, 1]
- Convert between channels-last (H, W, C) and channels-first (C, H, W)

## Intuition
A digital image is a grid of numbers. A greyscale image is a 2-D array: entry `img[r, c]` is the
brightness of the pixel in row `r`, column `c` (row 0 is the top). A colour image adds a third
axis for the red, green and blue **channels**: shape `(H, W, 3)`.

## Precise explanation
* Image files usually store **`uint8`** values: integers 0 (black) to 255 (white). Arithmetic
  on `uint8` **wraps around**: `np.uint8(250) + np.uint8(10)` is `4`, not 260.
* Safe recipe for brightness/contrast: convert to float, compute, then **clip** to `[0, 255]`,
  **round** and convert back: `np.clip(np.rint(x), 0, 255).astype(np.uint8)`.
* Contrast around mid-grey: `new = (old - 128) * contrast + 128 + brightness`.
* Neural networks prefer **floats in [0, 1]**: `img.astype(float) / 255`.
* **Channel order**: NumPy/OpenCV/PIL use channels-last `(H, W, C)`; PyTorch uses channels-first
  `(C, H, W)`. `np.transpose(img, (2, 0, 1))` converts; `(1, 2, 0)` converts back.
* OpenCV loads colour images in **BGR** order, not RGB — another reason to check channels.

## Worked example
```python
img = np.array([[[250, 0, 10]]], dtype=np.uint8)   # one pixel, shape (1, 1, 3)
img + 10              # [[[  4,  10,  20]]]  ← 250 wrapped around
np.clip(img.astype(float) + 10, 0, 255).astype(np.uint8)   # [[[255, 10, 20]]]
```

## Common mistakes
* Adding brightness directly to a `uint8` array.
* Indexing `img[x, y]` thinking x is horizontal — the first index is the **row** (y).
* Truncating with `astype(np.uint8)` without rounding (127.9 → 127).
* Feeding `(H, W, C)` data to a model that expects `(C, H, W)`.

## Why this matters
Every later step reads and writes images with these conventions, and a convolution layer
(CV-15) expects channels-first float input.

## Library implementation

Image libraries provide these conversions: Pillow's `ImageEnhance.Brightness`, OpenCV's
`cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)` (which also saturates instead of
wrapping), and torchvision's `transforms.ToTensor()` (uint8 `(H, W, C)` → float `(C, H, W)` in
[0, 1]). None of these are needed here; NumPy's `np.clip` gives the same saturating behaviour.
When PyTorch is installed, the test checks that your channels-first float conversion matches
`torch.from_numpy(...).permute(2, 0, 1) / 255`.

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
