"""Computer vision with OpenCV and PyTorch (library revision, Phase 3).

Library steps are followed by the NumPy implementations they replace on the required path, kept
as optional deep dives: [[flip-rotate]], [[threshold-binary]], [[intensity-histogram]],
[[sobel-edges]], [[max-pool-2d]], [[psnr]], [[bilinear-resize]], [[connected-components]].
"""

CV_PACKAGES = ["numpy", "opencv-python-headless"]

PROBLEMS = [
# ---------------------------------------------------------------- cv-opencv-basics
{
"slug": "cv-opencv-basics", "title": "OpenCV Basics: BGR, dtypes and Indexing",
"difficulty": "beginner", "prereqs": ["rgb-to-gray"], "packages": CV_PACKAGES,
"objectives": ["Convert between OpenCV's BGR order, RGB and greyscale with cv2.cvtColor",
               "Keep images as uint8 arrays and know where OpenCV expects them",
               "Translate OpenCV (x, y) coordinates into NumPy [row, column] indexing"],
"tags": ["opencv", "colour-spaces", "bgr", "image-arrays"],
"sources": ["S115", "S023"], "entry": "to_rgb_and_gray(bgr); crop(image, x, y, w, h)",
"article": r'''
# OpenCV Basics: BGR, dtypes and Indexing

## Intuition
OpenCV images are plain NumPy arrays, so everything from [[image-arrays]] still applies. Two
conventions trip everyone up: OpenCV stores colour channels as **B, G, R** (not R, G, B), and its
functions take points as **(x, y)** — column first — while NumPy indexes `[row, column]`.

## Precise explanation
```python
import cv2
bgr = cv2.imread("photo.jpg")                    # (height, width, 3), uint8, channels B, G, R
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)        # for matplotlib or PyTorch models
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)      # (height, width), uint8
patch = bgr[y:y + h, x:x + w]                     # rows first: y, then x
```

* Greyscale uses 0.299 R + 0.587 G + 0.114 B, rounded to the nearest integer — the weights from
  [[rgb-to-gray]]. Passing an RGB image with `COLOR_BGR2GRAY` silently swaps the red and blue
  weights.
* Most OpenCV functions expect `uint8` (0–255) or `float32`. Arithmetic on `uint8` arrays wraps
  around (250 + 10 = 4), so convert with `.astype(np.float32)` before doing maths.
* A slice such as `bgr[y:y+h, x:x+w]` is a **view**: writing to it changes the original image.
  Use `.copy()` when you need an independent crop.
* `cv2.imread` returns `None` (no exception) when the file is missing.

## Worked example
A pure blue pixel in BGR is `[255, 0, 0]`. Converted to RGB it becomes `[0, 0, 255]`, and to grey
round(0.114 × 255) = 29. The rectangle with top-left corner x = 4, y = 1, width 3 and height 2 is
`image[1:3, 4:7]`.

## Common mistakes
* Showing a BGR image with matplotlib and getting blue faces.
* Indexing `image[x, y]`.
* Adding brightness to a `uint8` image without clipping and getting dark wrap-around pixels.
* Forgetting to check `cv2.imread`'s result for `None`.

## Why this matters
Every later step — thresholds, edges, contours, CNN inputs — starts from a correctly ordered,
correctly typed array.
''',
"statement": r'''
1. `to_rgb_and_gray(bgr)` returns `(rgb, gray)` using `cv2.cvtColor` with `COLOR_BGR2RGB` and
   `COLOR_BGR2GRAY`. Raise `ValueError` unless `bgr` is a `uint8` array of shape `(h, w, 3)`.
2. `crop(image, x, y, w, h)` returns a **copy** of the rectangle whose top-left corner is column
   `x`, row `y`, with width `w` and height `h`. Raise `ValueError` if `w` or `h` is not positive or
   the rectangle does not fit inside the image.

**Example**
```python
rgb, gray = to_rgb_and_gray(np.array([[[255, 0, 0]]], dtype=np.uint8))
rgb.tolist(), gray.tolist()     # ([[[0, 0, 255]]], [[29]])
```
''',
"starter": r'''
import cv2
import numpy as np


def to_rgb_and_gray(bgr):
    # TODO
    pass


def crop(image, x, y, w, h):
    # TODO
    pass
''',
"hints": [
    "Check `isinstance(bgr, np.ndarray)`, `bgr.dtype == np.uint8`, `bgr.ndim == 3` and `bgr.shape[2] == 3`.",
    "`cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)` and `cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)`.",
    "Rows come first: `image[y:y + h, x:x + w].copy()` after checking `x + w <= width` and `y + h <= height`.",
],
"solution": r'''
import cv2
import numpy as np


def to_rgb_and_gray(bgr):
    if not isinstance(bgr, np.ndarray) or bgr.dtype != np.uint8 or bgr.ndim != 3 or bgr.shape[2] != 3:
        raise ValueError("expected a uint8 BGR image of shape (h, w, 3)")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB), cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)


def crop(image, x, y, w, h):
    height, width = image.shape[:2]
    if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > width or y + h > height:
        raise ValueError("rectangle does not fit inside the image")
    return image[y:y + h, x:x + w].copy()
''',
"explanation": r'''
`cvtColor` handles the channel order and the greyscale weights. The crop converts OpenCV's (x, y,
w, h) rectangle into NumPy's row-then-column slice and copies it so the caller can modify the crop
without touching the original.
''',
"tests": r'''
import numpy as np


class TestOpenCVBasics(unittest.TestCase):
    def test_blue_pixel(self):
        rgb, gray = S.to_rgb_and_gray(np.array([[[255, 0, 0]]], dtype=np.uint8))
        self.assertEqual(rgb.tolist(), [[[0, 0, 255]]])
        self.assertEqual(gray.tolist(), [[29]])

    def test_gray_weights(self):
        rng = np.random.default_rng(0)
        bgr = rng.integers(0, 256, size=(4, 5, 3), dtype=np.uint8)
        _, gray = S.to_rgb_and_gray(bgr)
        b, g, r = (bgr[..., i].astype(float) for i in range(3))
        self.assertTrue(np.all(np.abs(gray - (0.299 * r + 0.587 * g + 0.114 * b)) <= 1))
        self.assertEqual((gray.shape, gray.dtype), ((4, 5), np.uint8))

    def test_rgb_is_reversed_channels(self):
        bgr = np.arange(24, dtype=np.uint8).reshape(2, 4, 3)
        rgb, _ = S.to_rgb_and_gray(bgr)
        self.assertTrue(np.array_equal(rgb, bgr[..., ::-1]))

    def test_crop_rows_then_columns(self):
        image = np.arange(48).reshape(6, 8)
        self.assertEqual(S.crop(image, 4, 1, 3, 2).tolist(), [[12, 13, 14], [20, 21, 22]])

    def test_crop_is_copy(self):
        image = np.zeros((5, 5), dtype=np.uint8)
        patch = S.crop(image, 1, 1, 2, 2)
        patch[:] = 255
        self.assertEqual(int(image.sum()), 0)

    def test_invalid(self):
        for bad in (np.zeros((3, 3), np.uint8), np.zeros((3, 3, 3), np.float32), np.zeros((3, 3, 4), np.uint8)):
            with self.assertRaises(ValueError):
                S.to_rgb_and_gray(bad)
        with self.assertRaises(ValueError):
            S.crop(np.zeros((4, 4)), 2, 2, 3, 1)
''',
"feedback": [
    ("test_blue_pixel", "OpenCV images are BGR: use COLOR_BGR2RGB and COLOR_BGR2GRAY."),
    ("test_crop_rows_then_columns", "Index image[y:y + h, x:x + w] — rows (y) first."),
    ("test_crop_is_copy", "Return .copy() of the slice."),
    ("test_invalid", "Require uint8 (h, w, 3) images and rectangles inside the image."),
],
},
# ---------------------------------------------------------------- cv-geometric-transforms
{
"slug": "cv-geometric-transforms", "title": "Flips, Rotations and Affine Warps",
"difficulty": "beginner", "prereqs": ["cv-opencv-basics"], "packages": CV_PACKAGES,
"objectives": ["Flip and rotate images by multiples of 90° with cv2.flip and cv2.rotate",
               "Rotate about the centre with getRotationMatrix2D and warpAffine",
               "Translate an image with a 2×3 affine matrix"],
"tags": ["opencv", "geometric-transforms", "affine", "rotation"],
"sources": ["S116", "S122"], "entry": "transform(image, op); rotate_about_centre(image, angle); translate(image, dx, dy)",
"article": r'''
# Flips, Rotations and Affine Warps

## Intuition
Flips and quarter turns just rearrange pixels. Arbitrary rotations, shifts and scalings move
pixels to positions between grid points, so the new image must be **resampled**. OpenCV describes
all of these with one 2×3 **affine** matrix and one function, `warpAffine`.

## Precise explanation
```python
cv2.flip(img, 1)                          # 1: left-right, 0: up-down, -1: both
cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)  # also ROTATE_180, ROTATE_90_COUNTERCLOCKWISE
M = cv2.getRotationMatrix2D(center=(cx, cy), angle=30, scale=1.0)
out = cv2.warpAffine(img, M, (width, height))           # note: size is (width, height)
T = np.float32([[1, 0, dx], [0, 1, dy]])                # shift right by dx, down by dy
```

* An affine matrix maps a point (x, y) to (a·x + b·y + c, d·x + e·y + f): the left 2×2 block
  rotates/scales, the last column translates.
* Positive angles in `getRotationMatrix2D` rotate **counter-clockwise** on screen (the y axis points
  down). For the exact centre of an image use ((w − 1)/2, (h − 1)/2).
* Pixels that come from outside the source are filled with `borderValue` (0 by default).
* `cv2.ROTATE_90_CLOCKWISE` equals `np.rot90(img, -1)`; `cv2.flip(img, 1)` equals `img[:, ::-1]`.

## Worked example
Rotating a 5×5 image by 90° about (2, 2) gives exactly `np.rot90(img, 1)` (counter-clockwise).
Translating by dx = 2 moves column 0 to column 2 and fills columns 0–1 with zeros.

## What the library does inside
For every output pixel, `warpAffine` applies the inverse matrix to find where it came from and
interpolates there — bilinear by default, as in [[bilinear-resize]]. Your [[flip-rotate]] (the
optional deep dive after this step) does the exact quarter-turn rearrangements with NumPy.

## Common mistakes
* Passing `(height, width)` as the output size.
* Using the centre (w/2, h/2), which is half a pixel off for exact quarter turns.
* Expecting clockwise rotation from a positive angle.

## Why this matters
Augmentation (random flips, small rotations and shifts) and document straightening (the
document-scanner project idea) are built from these transforms.
''',
"statement": r'''
1. `transform(image, op)` with `op` one of `"flip_h"`, `"flip_v"`, `"rot90_cw"`, `"rot180"`,
   `"rot90_ccw"`, using `cv2.flip` and `cv2.rotate`; any other op raises `ValueError`.
2. `rotate_about_centre(image, angle, scale=1.0)` rotates about ((w − 1)/2, (h − 1)/2) with
   `getRotationMatrix2D` and `warpAffine`, keeping the image size.
3. `translate(image, dx, dy)` shifts the image right by `dx` and down by `dy` pixels with
   `warpAffine`, filling uncovered pixels with 0.

Results keep the input's dtype.
''',
"starter": r'''
import cv2
import numpy as np


def transform(image, op):
    # TODO
    pass


def rotate_about_centre(image, angle, scale=1.0):
    # TODO
    pass


def translate(image, dx, dy):
    # TODO
    pass
''',
"hints": [
    "Map op names to `lambda img: cv2.flip(img, 1)`, `cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)` and so on.",
    "`h, w = image.shape[:2]`; `M = cv2.getRotationMatrix2D(((w - 1) / 2, (h - 1) / 2), angle, scale)`.",
    "`cv2.warpAffine(image, M, (w, h))` — the size is (width, height); for translation `M = np.float32([[1, 0, dx], [0, 1, dy]])`.",
],
"solution": r'''
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
''',
"explanation": r'''
Flips and quarter turns are exact rearrangements. A rotation about the pixel-exact centre and a
pure translation are both affine matrices; `warpAffine` resamples the image through them into an
output of the original (width, height), filling uncovered pixels with zeros.
''',
"tests": r'''
import numpy as np

IMG = np.arange(20, dtype=np.uint8).reshape(4, 5)


class TestGeometricTransforms(unittest.TestCase):

    def test_flips(self):
        self.assertTrue(np.array_equal(S.transform(IMG, "flip_h"), IMG[:, ::-1]))
        self.assertTrue(np.array_equal(S.transform(IMG, "flip_v"), IMG[::-1, :]))

    def test_quarter_turns(self):
        self.assertTrue(np.array_equal(S.transform(IMG, "rot90_cw"), np.rot90(IMG, -1)))
        self.assertTrue(np.array_equal(S.transform(IMG, "rot90_ccw"), np.rot90(IMG, 1)))
        self.assertTrue(np.array_equal(S.transform(IMG, "rot180"), np.rot90(IMG, 2)))

    def test_rotate_about_centre_is_counter_clockwise(self):
        square = np.arange(25, dtype=np.uint8).reshape(5, 5)
        self.assertTrue(np.array_equal(S.rotate_about_centre(square, 90), np.rot90(square, 1)))

    def test_rotation_keeps_size_and_dtype(self):
        out = S.rotate_about_centre(IMG, 30, scale=0.8)
        self.assertEqual((out.shape, out.dtype), ((4, 5), np.uint8))

    def test_translate(self):
        out = S.translate(IMG, 2, 1)
        self.assertTrue(np.array_equal(out[1:, 2:], IMG[:-1, :-2]))
        self.assertEqual(int(out[0].sum()) + int(out[:, :2].sum()), 0)

    def test_unknown_op(self):
        with self.assertRaises(ValueError):
            S.transform(IMG, "rot45")
''',
"feedback": [
    ("test_flips", "flip_h is cv2.flip(img, 1); flip_v is cv2.flip(img, 0)."),
    ("test_rotate_about_centre_is_counter_clockwise", "Rotate about ((w - 1) / 2, (h - 1) / 2)."),
    ("test_rotation_keeps_size_and_dtype", "warpAffine's size argument is (width, height)."),
    ("test_translate", "The translation matrix is [[1, 0, dx], [0, 1, dy]]."),
],
},
# ---------------------------------------------------------------- cv-threshold-otsu
{
"slug": "cv-threshold-otsu", "title": "Thresholding and Otsu's Method",
"difficulty": "beginner", "prereqs": ["cv-geometric-transforms"], "packages": CV_PACKAGES,
"objectives": ["Binarise an image with cv2.threshold and a fixed threshold",
               "Let Otsu's method choose the threshold from the histogram",
               "Invert masks with THRESH_BINARY_INV"],
"tags": ["opencv", "thresholding", "otsu", "segmentation"],
"sources": ["S117", "S023"], "entry": "binarise(gray, threshold=None, invert=False)",
"article": r'''
# Thresholding and Otsu's Method

## Intuition
To separate dark text from a light page, or bright cells from a dark background, mark every pixel
brighter than some value as foreground. Picking that value by hand works for one photo and fails
on the next; Otsu's method picks it from the image's own histogram.

## Precise explanation
```python
t, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)          # mask = 255 where gray > 127
t, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)   # t chosen by Otsu
```

* `THRESH_BINARY` sets pixels **strictly greater** than the threshold to `maxval` (255), others
  to 0; `THRESH_BINARY_INV` does the opposite.
* With `THRESH_OTSU` the threshold argument is ignored and the returned `t` is the chosen value.
  Otsu tries every threshold and keeps the one that maximises the **between-class variance**
  w₀w₁(μ₀ − μ₁)², where w are the fractions of pixels below/above and μ their mean intensities.
  It works best when the histogram has two clear peaks.
* The input must be single-channel `uint8` for Otsu.

## Worked example
Pixels [10, 30, 200, 220]: any threshold from 30 to 199 separates the two groups; Otsu returns
30, and the mask is [0, 0, 255, 255].

## What the library does inside
A fixed threshold is the comparison `gray > t` from [[threshold-binary]] (the optional deep dive
after this step). Otsu adds one pass over the 256-bin histogram ([[cv-histograms]] next) to score
each candidate threshold.

## Common mistakes
* Expecting pixels equal to the threshold to be foreground (the test is strict).
* Passing a colour image to Otsu.
* Thresholding a photo with uneven lighting; blur first, or use `cv2.adaptiveThreshold`.

## Why this matters
Thresholding is the first step of document scanning, cell counting and many industrial
inspection systems; contours and connected components work on its masks.
''',
"statement": r'''
Write `binarise(gray, threshold=None, invert=False)` returning `(t, mask)` where `t` is a float and
`mask` a `uint8` array of 0s and 255s.

* With a number, use `cv2.threshold(gray, threshold, 255, kind)`; with `None`, use Otsu
  (`kind + cv2.THRESH_OTSU`, threshold argument 0).
* `kind` is `cv2.THRESH_BINARY_INV` when `invert` is true, else `cv2.THRESH_BINARY`.
* Raise `ValueError` unless `gray` is a 2-D `uint8` array.
''',
"starter": r'''
import cv2
import numpy as np


def binarise(gray, threshold=None, invert=False):
    # TODO
    pass
''',
"hints": [
    "Validate: `gray.ndim == 2 and gray.dtype == np.uint8`.",
    "`kind = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY`.",
    "For Otsu: `cv2.threshold(gray, 0, 255, kind + cv2.THRESH_OTSU)`; return `float(t), mask`.",
],
"solution": r'''
import cv2
import numpy as np


def binarise(gray, threshold=None, invert=False):
    if not isinstance(gray, np.ndarray) or gray.ndim != 2 or gray.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 image")
    kind = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    if threshold is None:
        t, mask = cv2.threshold(gray, 0, 255, kind + cv2.THRESH_OTSU)
    else:
        t, mask = cv2.threshold(gray, threshold, 255, kind)
    return float(t), mask
''',
"explanation": r'''
One `cv2.threshold` call covers both cases; adding the Otsu flag makes OpenCV choose the
threshold from the histogram and return it. Inversion only swaps which side becomes 255.
''',
"tests": r'''
import numpy as np


def otsu_brute_force(gray):
    values = gray.ravel().astype(float)
    best_t, best_score = 0, -1.0
    for t in range(256):
        low, high = values[values <= t], values[values > t]
        if len(low) == 0 or len(high) == 0:
            continue
        w0, w1 = len(low) / len(values), len(high) / len(values)
        score = w0 * w1 * (low.mean() - high.mean()) ** 2
        if score > best_score + 1e-9:
            best_t, best_score = t, score
    return best_t


class TestBinarise(unittest.TestCase):
    def test_fixed_threshold_is_strict(self):
        t, mask = S.binarise(np.array([[99, 100, 101]], np.uint8), 100)
        self.assertEqual(t, 100.0)
        self.assertEqual(mask.tolist(), [[0, 0, 255]])

    def test_otsu_example(self):
        t, mask = S.binarise(np.array([[10, 30], [200, 220]], np.uint8))
        self.assertEqual(mask.tolist(), [[0, 0], [255, 255]])
        self.assertTrue(30 <= t < 200)

    def test_otsu_matches_between_class_variance(self):
        rng = np.random.default_rng(0)
        gray = np.clip(np.concatenate([rng.normal(60, 15, 300), rng.normal(170, 20, 200)]), 0, 255).astype(np.uint8).reshape(20, 25)
        t, _ = S.binarise(gray)
        self.assertEqual(int(t), otsu_brute_force(gray))

    def test_invert(self):
        _, mask = S.binarise(np.array([[10, 200]], np.uint8), 100, invert=True)
        self.assertEqual(mask.tolist(), [[255, 0]])

    def test_output_types(self):
        t, mask = S.binarise(np.arange(16, dtype=np.uint8).reshape(4, 4) * 16)
        self.assertIs(type(t), float)
        self.assertEqual(mask.dtype, np.uint8)
        self.assertTrue(set(np.unique(mask).tolist()) <= {0, 255})

    def test_invalid(self):
        for bad in (np.zeros((2, 2), np.float32), np.zeros((2, 2, 3), np.uint8)):
            with self.assertRaises(ValueError):
                S.binarise(bad)
''',
"feedback": [
    ("test_fixed_threshold_is_strict", "THRESH_BINARY marks pixels strictly greater than the threshold."),
    ("test_otsu_matches_between_class_variance", "With threshold=None add cv2.THRESH_OTSU and return the chosen t."),
    ("test_invert", "Use THRESH_BINARY_INV when invert is true."),
    ("test_invalid", "Only 2-D uint8 images are accepted."),
],
},
# ---------------------------------------------------------------- cv-histograms
{
"slug": "cv-histograms", "title": "Histograms and Equalisation",
"difficulty": "beginner", "prereqs": ["cv-threshold-otsu"], "packages": CV_PACKAGES,
"objectives": ["Compute intensity histograms with cv2.calcHist",
               "Improve contrast with cv2.equalizeHist",
               "Explain equalisation as mapping intensities through the cumulative histogram"],
"tags": ["opencv", "histograms", "contrast", "equalisation"],
"sources": ["S118", "S023"], "entry": "histogram_and_equalise(gray, bins=256)",
"article": r'''
# Histograms and Equalisation

## Intuition
A histogram counts how many pixels have each brightness. A dull, low-contrast photo bunches its
counts into a narrow band. **Equalisation** stretches the band so that intensities are spread
over the full 0–255 range, making details visible.

## Precise explanation
```python
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])   # shape (256, 1), float32 counts
equal = cv2.equalizeHist(gray)                             # uint8, same shape
```

* `calcHist(images, channels, mask, histSize, ranges)`: lists because it handles several images
  and channels at once; `ranges` is [low, high) — the upper bound is exclusive, so use 256.
  `histSize=[4]` groups intensities into 4 bins of width 64.
* Equalisation maps each intensity v to round(255 · (cdf(v) − cdf_min)/(N − cdf_min)), where cdf is
  the cumulative histogram and N the number of pixels. The mapping is increasing, so darker pixels
  stay darker than brighter ones.
* It works on single-channel images. For colour photos, equalise only a brightness channel
  (for example the Y of YCrCb), not B, G and R separately.

## Worked example
For pixels [0, 50, 50, 100]: the cdf is 1, 3, 4 at 0, 50, 100, so 0 → 0, 50 → 255·2/3 = 170 and
100 → 255. The result [0, 170, 170, 255] uses the full range.

## What the library does inside
`calcHist` with 256 bins is `np.bincount` — your [[intensity-histogram]] (the optional deep dive
after this step). `equalizeHist` builds the cumulative histogram and applies it as a lookup table.

## Common mistakes
* Using `ranges=[0, 255]`, which drops the value 255.
* Equalising B, G and R separately and shifting colours.
* Expecting `calcHist` to return integers (it returns float32).

## Why this matters
Histograms drive Otsu thresholding, exposure correction and simple image-similarity features;
equalisation is a standard preprocessing step for low-light and medical images.
''',
"statement": r'''
Write `histogram_and_equalise(gray, bins=256)` returning
`{"hist": list[int], "equalized": uint8 array}` where `hist` is `cv2.calcHist` with `bins` bins over
`[0, 256)` converted to a list of ints, and `equalized` is `cv2.equalizeHist(gray)`.

Raise `ValueError` unless `gray` is a 2-D `uint8` array and `1 <= bins <= 256`.
''',
"starter": r'''
import cv2
import numpy as np


def histogram_and_equalise(gray, bins=256):
    # TODO
    pass
''',
"hints": [
    "Validate the image and the bin count first.",
    "`cv2.calcHist([gray], [0], None, [bins], [0, 256])` returns shape (bins, 1).",
    "`[int(v) for v in hist.ravel()]`; `cv2.equalizeHist(gray)`.",
],
"solution": r'''
import cv2
import numpy as np


def histogram_and_equalise(gray, bins=256):
    if not isinstance(gray, np.ndarray) or gray.ndim != 2 or gray.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 image")
    if not 1 <= bins <= 256:
        raise ValueError("bins must be between 1 and 256")
    hist = cv2.calcHist([gray], [0], None, [bins], [0, 256])
    return {"hist": [int(v) for v in hist.ravel()], "equalized": cv2.equalizeHist(gray)}
''',
"explanation": r'''
`calcHist` counts pixels in equal-width bins across [0, 256); flattening and converting gives a
plain list of counts. `equalizeHist` remaps intensities through the cumulative histogram so the
output spreads over the full range.
''',
"tests": r'''
import numpy as np


class TestHistograms(unittest.TestCase):
    def test_worked_example(self):
        r = S.histogram_and_equalise(np.array([[0, 50], [50, 100]], np.uint8))
        self.assertEqual(r["equalized"].tolist(), [[0, 170], [170, 255]])

    def test_matches_bincount(self):
        rng = np.random.default_rng(0)
        gray = rng.integers(0, 256, size=(30, 40), dtype=np.uint8)
        r = S.histogram_and_equalise(gray)
        self.assertEqual(r["hist"], np.bincount(gray.ravel(), minlength=256).tolist())

    def test_coarse_bins(self):
        gray = np.array([[0, 63, 64, 255]], np.uint8)
        self.assertEqual(S.histogram_and_equalise(gray, bins=4)["hist"], [2, 1, 0, 1])

    def test_equalisation_spreads_and_keeps_order(self):
        rng = np.random.default_rng(1)
        gray = rng.integers(100, 140, size=(50, 50)).astype(np.uint8)
        eq = S.histogram_and_equalise(gray)["equalized"]
        self.assertEqual((int(eq.min()), int(eq.max())), (0, 255))
        order = np.argsort(gray.ravel(), kind="stable")
        self.assertTrue(np.all(np.diff(eq.ravel()[order].astype(int)) >= 0))

    def test_types(self):
        r = S.histogram_and_equalise(np.zeros((3, 3), np.uint8))
        self.assertTrue(all(type(v) is int for v in r["hist"]))
        self.assertEqual(sum(r["hist"]), 9)
        self.assertEqual(r["equalized"].dtype, np.uint8)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.histogram_and_equalise(np.zeros((2, 2, 3), np.uint8))
        with self.assertRaises(ValueError):
            S.histogram_and_equalise(np.zeros((2, 2), np.uint8), bins=0)
''',
"feedback": [
    ("test_matches_bincount", "calcHist ranges are [0, 256): the upper bound is exclusive."),
    ("test_coarse_bins", "Pass [bins] as histSize."),
    ("test_types", "Convert the float32 counts to a list of ints."),
    ("test_invalid", "Require a 2-D uint8 image and 1 <= bins <= 256."),
],
},
# ---------------------------------------------------------------- cv-sobel-canny
{
"slug": "cv-sobel-canny", "title": "Edges with Sobel and Canny",
"difficulty": "intermediate", "prereqs": ["conv2d-filter", "cv-histograms"], "packages": CV_PACKAGES,
"objectives": ["Compute image gradients with cv2.Sobel in a float output type",
               "Detect thin edges with Gaussian blur and cv2.Canny",
               "Explain Canny's hysteresis thresholds"],
"tags": ["opencv", "edge-detection", "sobel", "canny", "gradients"],
"sources": ["S119", "S023"], "entry": "edges(gray, low, high, blur_ksize=5)",
"article": r'''
# Edges with Sobel and Canny

## Intuition
An edge is where brightness changes quickly. The Sobel filter measures that change in x and y;
the gradient magnitude is large on edges. Canny goes further: it keeps only the thin ridge of
strongest change and links edge pieces together, giving clean one-pixel-wide outlines.

## Precise explanation
```python
gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)     # d/dx — responds to vertical edges
gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)     # d/dy — horizontal edges
magnitude = np.hypot(gx, gy)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)                 # uint8 mask of 0 and 255
```

* Use a float output depth (`cv2.CV_64F`): gradients are negative on one side of an edge, and a
  `uint8` output would clip them to 0.
* Canny steps: smooth, Sobel gradients, **non-maximum suppression** (keep a pixel only if it is the
  largest along the gradient direction), then **hysteresis**: pixels above `high` are edges, pixels
  between `low` and `high` are kept only if connected to a strong edge.
* A ratio high:low of about 2:1 to 3:1 is typical. Blurring first removes noise edges.

## Worked example
A white square on black: gx is large on the left and right sides (positive on one, negative on the
other) and 0 on the top and bottom; Canny returns a closed one-pixel outline around the square.

## What the library does inside
`cv2.Sobel` is the convolution with the 3×3 kernels in [[sobel-edges]] (the optional deep dive
after this step); Canny adds the suppression and hysteresis passes.

## Common mistakes
* `cv2.Sobel(gray, -1, 1, 0)`: keeps uint8 and loses negative gradients.
* Running Canny on a noisy, unblurred photo.
* Setting `low` above `high`.

## Why this matters
Edges feed contour finding, lane detection and document scanning, and they are what the first layer
of a trained CNN tends to learn.
''',
"statement": r'''
Write `edges(gray, low, high, blur_ksize=5)` returning
`{"gx": float64 array, "gy": float64 array, "magnitude": float64 array, "canny": uint8 array}`.

* `gx`, `gy`: `cv2.Sobel` with `cv2.CV_64F`, `ksize=3`, on the original image.
* `magnitude`: `np.hypot(gx, gy)`.
* `canny`: `cv2.Canny` on `cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)` with `low`, `high`.
* Raise `ValueError` unless `gray` is 2-D `uint8`, `0 <= low <= high`, and `blur_ksize` is a positive
  odd integer.
''',
"starter": r'''
import cv2
import numpy as np


def edges(gray, low, high, blur_ksize=5):
    # TODO
    pass
''',
"hints": [
    "Validate the image, the thresholds and that `blur_ksize % 2 == 1`.",
    "`cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)` for gx and `(0, 1)` for gy.",
    "`cv2.Canny(cv2.GaussianBlur(gray, (k, k), 0), low, high)`.",
],
"solution": r'''
import cv2
import numpy as np


def edges(gray, low, high, blur_ksize=5):
    if not isinstance(gray, np.ndarray) or gray.ndim != 2 or gray.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 image")
    if not 0 <= low <= high:
        raise ValueError("need 0 <= low <= high")
    if blur_ksize < 1 or blur_ksize % 2 != 1:
        raise ValueError("blur_ksize must be a positive odd integer")
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    blurred = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    return {"gx": gx, "gy": gy, "magnitude": np.hypot(gx, gy), "canny": cv2.Canny(blurred, low, high)}
''',
"explanation": r'''
Sobel with a float depth keeps the sign of the gradient; the magnitude combines both directions.
Canny runs on a blurred copy so that noise does not produce spurious edges, and returns a binary
mask of thin, connected edges.
''',
"tests": r'''
import numpy as np


def square(size=32, lo=8, hi=24):
    img = np.zeros((size, size), np.uint8)
    img[lo:hi, lo:hi] = 200
    return img


class TestEdges(unittest.TestCase):
    def test_vertical_edge_in_gx_only(self):
        img = np.zeros((10, 10), np.uint8); img[:, 5:] = 100
        r = S.edges(img, 50, 150)
        self.assertGreater(r["gx"][5, 4], 0)
        self.assertEqual(float(np.abs(r["gy"][2:8, 2:8]).max()), 0.0)

    def test_negative_gradients_kept(self):
        img = np.zeros((10, 10), np.uint8); img[:, :5] = 100
        self.assertLess(S.edges(img, 50, 150)["gx"][5, 4], 0)

    def test_magnitude(self):
        r = S.edges(square(), 50, 150)
        self.assertTrue(np.allclose(r["magnitude"], np.sqrt(r["gx"] ** 2 + r["gy"] ** 2)))
        self.assertEqual(r["gx"].dtype, np.float64)

    def test_canny_outline(self):
        r = S.edges(square(), 50, 150)
        canny = r["canny"]
        self.assertEqual(canny.dtype, np.uint8)
        self.assertTrue(set(np.unique(canny).tolist()) <= {0, 255})
        ys, xs = np.nonzero(canny)
        self.assertTrue(6 <= ys.min() <= 9 and 22 <= ys.max() <= 25)
        self.assertEqual(int(canny[14:18, 14:18].sum()), 0)

    def test_flat_image_has_no_edges(self):
        r = S.edges(np.full((16, 16), 80, np.uint8), 10, 30)
        self.assertEqual(int(r["canny"].sum()), 0)
        self.assertEqual(float(r["magnitude"].max()), 0.0)

    def test_invalid(self):
        img = square()
        for args in ((img, 150, 50), (img, 50, 150, 4), (img.astype(np.float32), 50, 150)):
            with self.assertRaises(ValueError):
                S.edges(*args)
''',
"feedback": [
    ("test_negative_gradients_kept", "Use cv2.CV_64F as the Sobel output depth."),
    ("test_magnitude", "magnitude = np.hypot(gx, gy)."),
    ("test_canny_outline", "Blur with GaussianBlur, then cv2.Canny(blurred, low, high)."),
    ("test_invalid", "Check the image type, 0 <= low <= high and an odd blur size."),
],
},
# ---------------------------------------------------------------- cv-pooling-torch
{
"slug": "cv-pooling-torch", "title": "Pooling with nn.MaxPool2d and nn.AvgPool2d",
"difficulty": "intermediate", "prereqs": ["cv-sobel-canny", "torch-conv1d"], "packages": ["torch"],
"objectives": ["Apply max and average pooling to (batch, channels, height, width) tensors",
               "Compute pooled output sizes from kernel, stride and padding",
               "Explain where max pooling sends its gradient"],
"tags": ["pytorch", "pooling", "downsampling", "cnn"],
"sources": ["S123", "S124"], "entry": "pool(x, kind, kernel_size, stride=None, padding=0); pooled_size(n, kernel_size, stride=None, padding=0)",
"article": r'''
# Pooling with nn.MaxPool2d and nn.AvgPool2d

## Intuition
Pooling shrinks a feature map by summarising each small window: max pooling keeps the strongest
response ("is the feature present anywhere here?"), average pooling keeps the mean. Halving height
and width quarters the computation of later layers and makes small shifts matter less.

## Precise explanation
```python
from torch import nn
nn.MaxPool2d(kernel_size=2)(x)            # x: (B, C, H, W) → (B, C, H/2, W/2); stride defaults to kernel_size
nn.AvgPool2d(kernel_size=3, stride=1, padding=1)(x)    # same size, smoothed
```

* Output size per spatial dimension: ⌊(n + 2p − k)/s⌋ + 1.
* Pooling has no learnable parameters and acts on each channel separately.
* Max pooling passes the gradient back **only to the position of the maximum** in each window;
  average pooling spreads it equally, 1/k² per position.
* Padding for max pooling uses −∞ (padded values never win); average pooling counts padded zeros
  by default (`count_include_pad=True`).

## Worked example
For the 4×4 map [[1, 3, 2, 0], [4, 2, 1, 1], [0, 1, 5, 6], [2, 2, 7, 8]], 2×2 max pooling gives
[[4, 2], [2, 8]] and average pooling [[2.5, 1.0], [1.25, 6.5]].

## What the library does inside
The window loops of [[max-pool-2d]] (the optional deep dive after this step), vectorised over the
batch and channels.

## Common mistakes
* Passing an (H, W) tensor: add batch and channel dimensions with `x[None, None]`.
* Assuming stride 1 by default (it equals the kernel size).
* Expecting average pooling to ignore padding.

## Why this matters
The small CNN later in this topic alternates convolutions and max pooling — the classic recipe from
LeNet to VGG.
''',
"statement": r'''
1. `pool(x, kind, kernel_size, stride=None, padding=0)` applies `nn.MaxPool2d` (`kind="max"`) or
   `nn.AvgPool2d` (`kind="avg"`) to a 4-D float tensor (convert with `torch.as_tensor(..., dtype=torch.float32)`).
   Raise `ValueError` for another kind or a tensor that is not 4-D.
2. `pooled_size(n, kernel_size, stride=None, padding=0)` returns ⌊(n + 2·padding − kernel_size)/stride⌋ + 1,
   with `stride` defaulting to `kernel_size`.
''',
"starter": r'''
import torch
from torch import nn


def pool(x, kind, kernel_size, stride=None, padding=0):
    # TODO
    pass


def pooled_size(n, kernel_size, stride=None, padding=0):
    # TODO
    pass
''',
"hints": [
    "Choose the class with a dict: `{\"max\": nn.MaxPool2d, \"avg\": nn.AvgPool2d}`.",
    "`layer = cls(kernel_size, stride=stride, padding=padding)`; stride=None means stride = kernel size.",
    "`(n + 2 * padding - kernel_size) // stride + 1` after `stride = stride or kernel_size`.",
],
"solution": r'''
import torch
from torch import nn

POOLS = {"max": nn.MaxPool2d, "avg": nn.AvgPool2d}


def pool(x, kind, kernel_size, stride=None, padding=0):
    if kind not in POOLS:
        raise ValueError("kind must be 'max' or 'avg'")
    x = torch.as_tensor(x, dtype=torch.float32)
    if x.ndim != 4:
        raise ValueError("expected a (batch, channels, height, width) tensor")
    return POOLS[kind](kernel_size, stride=stride, padding=padding)(x)


def pooled_size(n, kernel_size, stride=None, padding=0):
    stride = stride or kernel_size
    return (n + 2 * padding - kernel_size) // stride + 1
''',
"explanation": r'''
Both pooling layers take the same window arguments, so one dictionary selects the class. The size
formula is the same as for convolution, with the stride defaulting to the kernel size.
''',
"tests": r'''
import torch


MAP = torch.tensor([[1.0, 3, 2, 0], [4, 2, 1, 1], [0, 1, 5, 6], [2, 2, 7, 8]])[None, None]


class TestPooling(unittest.TestCase):
    def test_max_example(self):
        self.assertEqual(S.pool(MAP, "max", 2).tolist(), [[[[4.0, 2.0], [2.0, 8.0]]]])

    def test_avg_example(self):
        self.assertEqual(S.pool(MAP, "avg", 2).tolist(), [[[[2.5, 1.0], [1.25, 6.5]]]])

    def test_sizes(self):
        x = torch.randn(2, 3, 11, 9)
        out = S.pool(x, "max", 3, stride=2, padding=1)
        self.assertEqual(tuple(out.shape), (2, 3, S.pooled_size(11, 3, 2, 1), S.pooled_size(9, 3, 2, 1)))
        self.assertEqual((S.pooled_size(4, 2), S.pooled_size(7, 3, 1, 1)), (2, 7))

    def test_max_gradient_goes_to_argmax(self):
        x = MAP.clone().requires_grad_(True)
        S.pool(x, "max", 2).sum().backward()
        expected = torch.zeros(4, 4); expected[1, 0] = expected[0, 2] = expected[3, 0] = expected[3, 3] = 1
        self.assertTrue(torch.equal(x.grad[0, 0], expected))

    def test_avg_gradient_spreads(self):
        x = MAP.clone().requires_grad_(True)
        S.pool(x, "avg", 2).sum().backward()
        self.assertTrue(torch.allclose(x.grad, torch.full_like(x, 0.25)))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.pool(MAP, "median", 2)
        with self.assertRaises(ValueError):
            S.pool(torch.zeros(4, 4), "max", 2)
''',
"feedback": [
    ("test_max_example", "Use nn.MaxPool2d(kernel_size, stride=stride, padding=padding)."),
    ("test_avg_example", "Use nn.AvgPool2d for kind 'avg'."),
    ("test_sizes", "The output size is (n + 2p - k) // s + 1 with s defaulting to k."),
    ("test_invalid", "Reject unknown kinds and tensors that are not 4-D."),
],
},
# ---------------------------------------------------------------- cv-psnr
{
"slug": "cv-psnr", "title": "Image Quality: MSE and PSNR",
"difficulty": "intermediate", "prereqs": ["conv2d-layer", "cv-pooling-torch"], "packages": CV_PACKAGES,
"objectives": ["Compute MSE between images without uint8 overflow",
               "Compute PSNR with cv2.PSNR and from the formula",
               "Interpret PSNR values for compression and denoising"],
"tags": ["opencv", "image-quality", "psnr", "mse"],
"sources": ["S023", "S122"], "entry": "image_quality(reference, distorted)",
"article": r'''
# Image Quality: MSE and PSNR

## Intuition
How close is a compressed or denoised image to the original? The mean squared error averages
the squared pixel differences. PSNR (peak signal-to-noise ratio) puts that error on a logarithmic
scale relative to the largest possible pixel value, in decibels: higher is better.

## Precise explanation
$$\text{MSE} = \frac{1}{N}\sum (I - K)^2,\qquad \text{PSNR} = 10\log_{10}\frac{255^2}{\text{MSE}}\ \text{dB}$$

```python
cv2.PSNR(reference, distorted)        # uint8 images, peak 255
```

* Compute differences in floating point: `reference - distorted` on `uint8` arrays wraps around
  (3 − 5 = 254).
* Identical images have MSE 0 and infinite PSNR; `cv2.PSNR` instead returns a large finite value
  (about 361 dB), so handle MSE = 0 yourself.
* Rough guide for 8-bit images: above 40 dB differences are hard to see; 30–40 dB is good
  compression; below 20 dB the distortion is obvious. PSNR does not model human perception well —
  SSIM is a common complement.

## Worked example
If every pixel differs by exactly 1, MSE = 1 and PSNR = 10·log₁₀(65025) = 48.13 dB. Uniform noise
of ±10 gives about 28 dB.

## What the library does inside
The formula you implement by hand in [[psnr]] (the optional deep dive after this step), computed in
double precision over all channels.

## Common mistakes
* Subtracting `uint8` arrays directly.
* Comparing images of different sizes or channel orders.
* Reporting `cv2.PSNR`'s 361 dB for identical images as a meaningful number.

## Why this matters
PSNR is the standard sanity metric for compression, super-resolution and denoising models, and a
quick way to check that an image pipeline did not change pixels it should not have.
''',
"statement": r'''
Write `image_quality(reference, distorted)` returning `{"mse": float, "psnr": float}` for two
`uint8` images of the same shape.

* `mse` is computed in floating point.
* `psnr` is `math.inf` when `mse` is 0, otherwise `cv2.PSNR(reference, distorted)`.
* Raise `ValueError` if the shapes differ or either image is not `uint8`.
''',
"starter": r'''
import math

import cv2
import numpy as np


def image_quality(reference, distorted):
    # TODO
    pass
''',
"hints": [
    "Check `reference.shape == distorted.shape` and both dtypes.",
    "`diff = reference.astype(np.float64) - distorted.astype(np.float64)`; `mse = float(np.mean(diff ** 2))`.",
    "Return `math.inf` for zero error, otherwise `float(cv2.PSNR(reference, distorted))`.",
],
"solution": r'''
import math

import cv2
import numpy as np


def image_quality(reference, distorted):
    if reference.shape != distorted.shape or reference.dtype != np.uint8 or distorted.dtype != np.uint8:
        raise ValueError("need two uint8 images of the same shape")
    diff = reference.astype(np.float64) - distorted.astype(np.float64)
    mse = float(np.mean(diff ** 2))
    return {"mse": mse, "psnr": math.inf if mse == 0 else float(cv2.PSNR(reference, distorted))}
''',
"explanation": r'''
Converting to float before subtracting avoids uint8 wrap-around. OpenCV's PSNR uses the 8-bit peak
of 255; zero error is reported as infinity instead of OpenCV's large finite stand-in.
''',
"tests": r'''
import numpy as np


class TestImageQuality(unittest.TestCase):
    def test_off_by_one(self):
        ref = np.full((8, 8), 100, np.uint8)
        r = S.image_quality(ref, ref + 1)
        self.assertEqual(r["mse"], 1.0)
        self.assertAlmostEqual(r["psnr"], 10 * math.log10(255 ** 2), places=6)

    def test_no_wraparound(self):
        a = np.array([[3]], np.uint8); b = np.array([[5]], np.uint8)
        self.assertEqual(S.image_quality(a, b)["mse"], 4.0)

    def test_identical_is_infinite(self):
        img = np.arange(16, dtype=np.uint8).reshape(4, 4)
        r = S.image_quality(img, img.copy())
        self.assertEqual(r["mse"], 0.0)
        self.assertEqual(r["psnr"], math.inf)

    def test_more_noise_lower_psnr(self):
        rng = np.random.default_rng(0)
        ref = rng.integers(20, 230, size=(32, 32, 3)).astype(np.uint8)
        mild = np.clip(ref + rng.integers(-3, 4, ref.shape), 0, 255).astype(np.uint8)
        strong = np.clip(ref + rng.integers(-30, 31, ref.shape), 0, 255).astype(np.uint8)
        self.assertGreater(S.image_quality(ref, mild)["psnr"], S.image_quality(ref, strong)["psnr"])

    def test_symmetric_and_formula(self):
        rng = np.random.default_rng(1)
        a = rng.integers(0, 256, (10, 10)).astype(np.uint8); b = rng.integers(0, 256, (10, 10)).astype(np.uint8)
        r1, r2 = S.image_quality(a, b), S.image_quality(b, a)
        self.assertEqual(r1, r2)
        self.assertAlmostEqual(r1["psnr"], 10 * math.log10(255 ** 2 / r1["mse"]), places=6)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.image_quality(np.zeros((2, 2), np.uint8), np.zeros((2, 3), np.uint8))
        with self.assertRaises(ValueError):
            S.image_quality(np.zeros((2, 2), np.float32), np.zeros((2, 2), np.float32))
''',
"feedback": [
    ("test_no_wraparound", "Convert to float before subtracting uint8 images."),
    ("test_identical_is_infinite", "Return math.inf when the MSE is zero."),
    ("test_symmetric_and_formula", "PSNR = 10·log10(255² / MSE)."),
    ("test_invalid", "Require two uint8 images with the same shape."),
],
},
# ---------------------------------------------------------------- cv-resize
{
"slug": "cv-resize", "title": "Resizing with cv2.resize",
"difficulty": "advanced", "prereqs": ["cv-psnr"], "packages": CV_PACKAGES,
"objectives": ["Resize images with cv2.resize and the (width, height) size convention",
               "Choose nearest, linear, cubic or area interpolation for the task",
               "Downscale without aliasing using INTER_AREA"],
"tags": ["opencv", "resizing", "interpolation", "image-pyramids"],
"sources": ["S122", "S023"], "entry": "resize(image, width, height, method=\"linear\")",
"article": r'''
# Resizing with cv2.resize

## Intuition
Models want fixed input sizes, screens want thumbnails, and big photos are slow. Resizing computes
new pixels from old ones. Enlarging must invent values between pixels; shrinking must combine many
pixels into one without creating jagged patterns.

## Precise explanation
```python
small = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)    # size is (W, H)!
big = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
```

| Method | Use for |
|---|---|
| `INTER_NEAREST` | label masks and class maps (never invents new values) |
| `INTER_LINEAR` (default) | general enlarging, fast |
| `INTER_CUBIC` | higher-quality enlarging, slower, may overshoot |
| `INTER_AREA` | **shrinking** — averages the pixels each output pixel covers |

* Shrinking with nearest or linear interpolation skips pixels and causes aliasing (moiré on fine
  patterns); `INTER_AREA` averages instead. Halving with it averages each 2×2 block.
* For masks, any interpolation other than nearest creates in-between labels such as 127.

## Worked example
Halving [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]] with `INTER_AREA` gives the
block means [[2.5, 4.5], [10.5, 12.5]], rounded to uint8 as [[3, 5], [11, 13]].

## What the library does inside
`INTER_LINEAR` is the bilinear interpolation you implement in [[bilinear-resize]] (the optional
deep dive after this step), with OpenCV's half-pixel alignment of the pixel grids.

## Common mistakes
* Passing `(height, width)`.
* Resizing segmentation masks with linear interpolation.
* Shrinking photos with `INTER_NEAREST` and getting jagged or flickering results.

## Why this matters
Every CNN pipeline resizes its inputs; choosing the interpolation correctly keeps labels valid and
images free of artefacts.
''',
"statement": r'''
Write `resize(image, width, height, method="linear")` returning `cv2.resize(image, (width, height),
interpolation=...)` with `method` one of `"nearest"`, `"linear"`, `"cubic"`, `"area"`.

Raise `ValueError` for an unknown method or a non-positive width or height.
''',
"starter": r'''
import cv2
import numpy as np


def resize(image, width, height, method="linear"):
    # TODO
    pass
''',
"hints": [
    "Map the names to `cv2.INTER_NEAREST`, `cv2.INTER_LINEAR`, `cv2.INTER_CUBIC`, `cv2.INTER_AREA`.",
    "Validate `width > 0 and height > 0`.",
    "`cv2.resize(image, (width, height), interpolation=METHODS[method])` — width first.",
],
"solution": r'''
import cv2
import numpy as np

METHODS = {"nearest": cv2.INTER_NEAREST, "linear": cv2.INTER_LINEAR,
           "cubic": cv2.INTER_CUBIC, "area": cv2.INTER_AREA}


def resize(image, width, height, method="linear"):
    if method not in METHODS:
        raise ValueError("unknown interpolation method " + str(method))
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    return cv2.resize(image, (width, height), interpolation=METHODS[method])
''',
"explanation": r'''
A dictionary maps readable names to OpenCV's interpolation flags. The only subtle part is the size
argument, which OpenCV takes as (width, height) although the result's shape is (height, width).
''',
"tests": r'''
import numpy as np


class TestResize(unittest.TestCase):
    def test_size_order(self):
        out = S.resize(np.zeros((10, 20), np.uint8), 8, 4)
        self.assertEqual(out.shape, (4, 8))

    def test_area_halving_averages_blocks(self):
        img = np.arange(16, dtype=np.uint8).reshape(4, 4)
        self.assertEqual(S.resize(img, 2, 2, "area").tolist(), [[3, 5], [11, 13]])

    def test_nearest_keeps_labels(self):
        mask = np.array([[0, 1], [2, 3]], np.uint8)
        out = S.resize(mask, 7, 5, "nearest")
        self.assertTrue(set(np.unique(out).tolist()) <= {0, 1, 2, 3})
        linear = S.resize(np.array([[0, 255]], np.uint8), 8, 1, "linear")
        self.assertTrue(len(set(linear.ravel().tolist())) > 2)

    def test_linear_upscale_is_monotone(self):
        out = S.resize(np.array([[0, 100]], np.uint8), 4, 1, "linear")
        self.assertEqual(out.tolist(), [[0, 25, 75, 100]])

    def test_colour_and_dtype_kept(self):
        img = np.random.default_rng(0).integers(0, 256, (6, 9, 3)).astype(np.uint8)
        out = S.resize(img, 3, 2, "cubic")
        self.assertEqual((out.shape, out.dtype), ((2, 3, 3), np.uint8))

    def test_invalid(self):
        img = np.zeros((4, 4), np.uint8)
        with self.assertRaises(ValueError):
            S.resize(img, 2, 2, "lanczos9")
        with self.assertRaises(ValueError):
            S.resize(img, 0, 2)
''',
"feedback": [
    ("test_size_order", "cv2.resize takes (width, height)."),
    ("test_area_halving_averages_blocks", "Use cv2.INTER_AREA for 'area'."),
    ("test_nearest_keeps_labels", "Use cv2.INTER_NEAREST for 'nearest'."),
    ("test_invalid", "Reject unknown methods and non-positive sizes."),
],
},
# ---------------------------------------------------------------- cv-contours
{
"slug": "cv-contours", "title": "Contours and Bounding Boxes",
"difficulty": "advanced", "prereqs": ["cv-resize"], "packages": CV_PACKAGES,
"objectives": ["Find object outlines in a binary mask with cv2.findContours",
               "Measure each object's bounding box, area and centroid",
               "Filter small objects and ignore holes with RETR_EXTERNAL"],
"tags": ["opencv", "contours", "bounding-boxes", "shape-analysis"],
"sources": ["S120", "S121"], "entry": "find_objects(mask, min_area=0)",
"article": r'''
# Contours and Bounding Boxes

## Intuition
After thresholding, each white blob is an object. A **contour** is the list of points along a
blob's boundary. From it you get a bounding box (where is it?), an area (how big?) and a centroid
(where is its centre of mass?) — enough to count, locate and filter objects.

## Precise explanation
```python
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    x, y, w, h = cv2.boundingRect(c)       # top-left corner and size, in pixels
    area = cv2.contourArea(c)               # area of the polygon through the boundary pixels
    m = cv2.moments(c)
    cx, cy = m["m10"] / m["m00"], m["m01"] / m["m00"]   # centroid (needs m00 > 0)
```

* The mask must be single-channel `uint8`; any non-zero pixel is foreground.
* `RETR_EXTERNAL` returns only outer boundaries, so holes inside objects are ignored;
  `RETR_TREE` returns the full nesting.
* `CHAIN_APPROX_SIMPLE` stores only the corners of straight runs (a rectangle has 4 points).
* `contourArea` measures the polygon through boundary **pixel centres**, so a filled w × h rectangle
  has area (w − 1)(h − 1), not w·h. For pixel counts use connected components (later in this topic).
* In OpenCV 4.x `findContours` returns two values.

## Worked example
A filled rectangle covering columns 4–11 and rows 5–9 gives `boundingRect` (4, 5, 8, 5),
`contourArea` 7 × 4 = 28 and centroid (7.5, 7.0).

## Common mistakes
* Passing a greyscale photo instead of a binary mask.
* Expecting `contourArea` to equal the number of pixels.
* Dividing by `m00` for a degenerate contour (a single pixel or line) without checking for zero.

## Why this matters
Contours locate documents in photos, count parts on a conveyor belt and produce the boxes that
detection post-processing (IoU and NMS, later in this topic) works with. The document-scanner
project idea after this step is built on them.
''',
"statement": r'''
Write `find_objects(mask, min_area=0)` returning one dict per outer contour,
`{"x", "y", "w", "h", "area", "centroid"}`, sorted by `(y, x)`.

* Use `cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`.
* `x, y, w, h` are ints from `cv2.boundingRect`; `area` is `float(cv2.contourArea(c))`;
  `centroid` is `(cx, cy)` from `cv2.moments`, or the bounding-box centre `(x + (w - 1) / 2, y + (h - 1) / 2)`
  when `m00` is 0.
* Keep only contours whose `area >= min_area`.
* Raise `ValueError` unless `mask` is a 2-D `uint8` array.
''',
"starter": r'''
import cv2
import numpy as np


def find_objects(mask, min_area=0):
    # TODO
    pass
''',
"hints": [
    "Validate the mask; then `contours, _ = cv2.findContours(...)`.",
    "For each contour read `boundingRect`, `contourArea` and `moments`; guard `m00 == 0`.",
    "Filter by area and sort with `key=lambda o: (o[\"y\"], o[\"x\"])`.",
],
"solution": r'''
import cv2
import numpy as np


def find_objects(mask, min_area=0):
    if not isinstance(mask, np.ndarray) or mask.ndim != 2 or mask.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 mask")
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for c in contours:
        x, y, w, h = (int(v) for v in cv2.boundingRect(c))
        area = float(cv2.contourArea(c))
        if area < min_area:
            continue
        m = cv2.moments(c)
        if m["m00"] > 0:
            centroid = (m["m10"] / m["m00"], m["m01"] / m["m00"])
        else:
            centroid = (x + (w - 1) / 2, y + (h - 1) / 2)
        objects.append({"x": x, "y": y, "w": w, "h": h, "area": area, "centroid": centroid})
    return sorted(objects, key=lambda o: (o["y"], o["x"]))
''',
"explanation": r'''
`RETR_EXTERNAL` gives one contour per separate blob; bounding box, polygon area and moments
describe each one. Degenerate contours (a line or a single pixel) have zero area, so their centre
falls back to the middle of the bounding box. Sorting gives a stable, top-to-bottom order.
''',
"tests": r'''
import numpy as np


def two_rectangles():
    mask = np.zeros((30, 30), np.uint8)
    mask[5:10, 4:12] = 255          # 8 wide, 5 tall
    mask[15:27, 18:26] = 255        # 8 wide, 12 tall
    return mask


class TestFindObjects(unittest.TestCase):
    def test_boxes(self):
        objs = S.find_objects(two_rectangles())
        self.assertEqual([(o["x"], o["y"], o["w"], o["h"]) for o in objs], [(4, 5, 8, 5), (18, 15, 8, 12)])

    def test_area_and_centroid(self):
        first = S.find_objects(two_rectangles())[0]
        self.assertEqual(first["area"], 28.0)
        self.assertAlmostEqual(first["centroid"][0], 7.5)
        self.assertAlmostEqual(first["centroid"][1], 7.0)

    def test_min_area_filter(self):
        objs = S.find_objects(two_rectangles(), min_area=50)
        self.assertEqual([(o["x"], o["y"]) for o in objs], [(18, 15)])

    def test_holes_ignored(self):
        mask = np.zeros((20, 20), np.uint8)
        mask[2:18, 2:18] = 255
        mask[7:13, 7:13] = 0
        self.assertEqual(len(S.find_objects(mask)), 1)

    def test_empty_and_single_pixel(self):
        self.assertEqual(S.find_objects(np.zeros((5, 5), np.uint8)), [])
        dot = np.zeros((5, 5), np.uint8); dot[2, 3] = 255
        [obj] = S.find_objects(dot)
        self.assertEqual((obj["x"], obj["y"], obj["w"], obj["h"], obj["area"]), (3, 2, 1, 1, 0.0))
        self.assertEqual(obj["centroid"], (3.0, 2.0))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.find_objects(np.zeros((5, 5), np.float32))
''',
"feedback": [
    ("test_boxes", "Use RETR_EXTERNAL and boundingRect, and sort by (y, x)."),
    ("test_area_and_centroid", "area is cv2.contourArea; the centroid is (m10/m00, m01/m00)."),
    ("test_holes_ignored", "RETR_EXTERNAL returns only outer boundaries."),
    ("test_empty_and_single_pixel", "When m00 is 0 use the bounding-box centre."),
],
},
# ---------------------------------------------------------------- cv-small-cnn
{
"slug": "cv-small-cnn", "title": "A Small CNN in PyTorch",
"difficulty": "advanced", "prereqs": ["cv-contours", "torch-training-loop"], "packages": ["numpy", "torch"],
"objectives": ["Stack Conv2d, ReLU and MaxPool2d layers into a CNN",
               "Compute the flattened feature size before the classifier layer",
               "Train the CNN on generated images and evaluate it on new ones"],
"tags": ["pytorch", "cnn", "image-classification", "conv2d"],
"sources": ["S124", "S093"], "entry": "class SmallCNN(nn.Module); train_cnn(images, labels, epochs=8, lr=0.01, seed=0)",
"article": r'''
# A Small CNN in PyTorch

## Intuition
A convolutional network learns its own filters. Early layers find edges and blobs, later layers
combine them into parts; pooling shrinks the maps so later filters see larger regions. Because the
same filter slides everywhere, the network recognises a pattern wherever it appears.

## Precise explanation
For 1-channel 16×16 images and 3 classes:

```python
self.features = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),    # 8 × 8 × 8
    nn.Conv2d(8, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),   # 16 × 4 × 4
)
self.classifier = nn.Linear(16 * 4 * 4, n_classes)

def forward(self, x):                     # x: (B, 1, 16, 16), float32 in [0, 1]
    return self.classifier(torch.flatten(self.features(x), 1))
```

* `padding=1` with a 3×3 kernel keeps height and width; each `MaxPool2d(2)` halves them.
* The classifier's input size is channels × height × width after the last pool — compute it
  ([[cv-pooling-torch]]) or run a dummy tensor through `features` and read the shape.
* `nn.Conv2d(in, out, k)` has out·in·k·k + out parameters — far fewer than a dense layer on raw
  pixels, which is why CNNs generalise well on images.
* Images become tensors of shape (B, C, H, W) with values scaled to [0, 1]; labels are `long`.

## Worked example
On synthetic 16×16 images of horizontal bars, vertical bars and square outlines at random
positions, this network reaches over 95% accuracy on new images after a few epochs, while a
logistic regression on raw pixels struggles because the shapes move around.

## What the library does inside
Each `Conv2d` computes the multi-channel sums of [[conv2d-layer]] for all positions at once; the
training loop is the one from [[torch-training-loop]].

## Common mistakes
* A wrong flattened size, giving "mat1 and mat2 shapes cannot be multiplied".
* Feeding (B, H, W) without the channel dimension, or channels-last (B, H, W, C) arrays.
* Forgetting to scale uint8 pixels to [0, 1].

## Why this matters
This is a miniature of the networks behind image classification, medical imaging and visual
inspection; the shape-sorter project idea builds on it.
''',
"statement": r'''
1. `class SmallCNN(nn.Module)` with `__init__(self, n_classes=3, size=16)`: `self.features` and
   `self.classifier` exactly as in the lesson, with the classifier input `16 * (size // 4) ** 2`.
   `forward(x)` returns logits.
2. `train_cnn(images, labels, epochs=8, lr=0.01, seed=0)` where `images` is an array
   `(n, size, size)` of uint8 pixels: scale to [0, 1], add the channel dimension, call
   `torch.manual_seed(seed)`, build `SmallCNN(max(labels) + 1, size)`, and train with Adam,
   `CrossEntropyLoss` and a `DataLoader(batch_size=32, shuffle=True, generator=torch.Generator().manual_seed(seed))`.
   Return `(model, history)` with the mean loss per epoch and the model in `eval()` mode.
3. `predict(model, images)` returns a list of class indices for uint8 images, scaled the same way.
''',
"starter": r'''
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class SmallCNN(nn.Module):
    def __init__(self, n_classes=3, size=16):
        super().__init__()
        # TODO

    def forward(self, x):
        # TODO
        pass


def train_cnn(images, labels, epochs=8, lr=0.01, seed=0):
    # TODO
    pass


def predict(model, images):
    # TODO
    pass
''',
"hints": [
    "Write a helper `to_tensor(images)` returning `torch.as_tensor(np.asarray(images), dtype=torch.float32)[:, None] / 255`.",
    "The classifier is `nn.Linear(16 * (size // 4) ** 2, n_classes)`; forward flattens with `torch.flatten(x, 1)`.",
    "The training loop is the one from the training-loop step, with the epoch loss weighted by batch size.",
],
"solution": r'''
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


class SmallCNN(nn.Module):
    def __init__(self, n_classes=3, size=16):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(8, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Linear(16 * (size // 4) ** 2, n_classes)

    def forward(self, x):
        return self.classifier(torch.flatten(self.features(x), 1))


def to_tensor(images):
    return torch.as_tensor(np.asarray(images), dtype=torch.float32)[:, None] / 255


def train_cnn(images, labels, epochs=8, lr=0.01, seed=0):
    X = to_tensor(images)
    y = torch.as_tensor(labels, dtype=torch.long)
    torch.manual_seed(seed)
    model = SmallCNN(int(y.max()) + 1, X.shape[-1])
    loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    history = []
    for _ in range(epochs):
        model.train()
        total = 0.0
        for xb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            total += loss.item() * len(yb)
        history.append(total / len(y))
    model.eval()
    return model, history


def predict(model, images):
    model.eval()
    with torch.no_grad():
        return model(to_tensor(images)).argmax(dim=1).tolist()
''',
"explanation": r'''
Two convolution blocks turn a 16×16 image into 16 feature maps of 4×4; one linear layer maps them to
class scores. Training is the standard loop; scaling pixels to [0, 1] and adding the channel axis
happen in one helper used by both training and prediction.
''',
"tests": r'''
import numpy as np
import torch
from torch import nn


def make_shapes(n, seed, size=16):
    """Class 0: horizontal bar, 1: vertical bar, 2: square outline; random positions and noise."""
    rng = np.random.default_rng(seed)
    images = np.zeros((n, size, size), np.uint8)
    labels = np.arange(n) % 3
    for i, label in enumerate(labels):
        r, c = rng.integers(2, size - 8, 2)
        if label == 0:
            images[i, r + 3, c:c + 7] = 255
        elif label == 1:
            images[i, r:r + 7, c + 3] = 255
        else:
            images[i, r:r + 6, c] = images[i, r:r + 6, c + 5] = 255
            images[i, r, c:c + 6] = images[i, r + 5, c:c + 6] = 255
        images[i] = np.clip(images[i].astype(int) + rng.integers(0, 40, (size, size)), 0, 255)
    return images, labels


class TestSmallCNN(unittest.TestCase):
    def test_shapes_through_network(self):
        model = S.SmallCNN(3, 16)
        self.assertEqual(tuple(model(torch.zeros(5, 1, 16, 16)).shape), (5, 3))
        self.assertEqual(model.classifier.in_features, 256)

    def test_layers(self):
        model = S.SmallCNN(4, 32)
        convs = [m for m in model.features if isinstance(m, nn.Conv2d)]
        pools = [m for m in model.features if isinstance(m, nn.MaxPool2d)]
        self.assertEqual([(c.in_channels, c.out_channels) for c in convs], [(1, 8), (8, 16)])
        self.assertEqual(len(pools), 2)
        self.assertEqual(model.classifier.in_features, 16 * 8 * 8)

    def test_learns_shapes(self):
        X, y = make_shapes(300, 0)
        model, history = S.train_cnn(X, y, epochs=8)
        Xt, yt = make_shapes(150, 1)
        self.assertGreater(np.mean(np.array(S.predict(model, Xt)) == yt), 0.9)
        self.assertLess(history[-1], history[0])

    def test_reproducible(self):
        X, y = make_shapes(64, 2)
        _, a = S.train_cnn(X, y, epochs=2, seed=3)
        _, b = S.train_cnn(X, y, epochs=2, seed=3)
        self.assertEqual(a, b)

    def test_eval_mode_and_types(self):
        X, y = make_shapes(30, 3)
        model, history = S.train_cnn(X, y, epochs=1)
        self.assertFalse(model.training)
        preds = S.predict(model, X[:4])
        self.assertEqual(len(preds), 4)
        self.assertTrue(all(type(p) is int for p in preds))

    def test_parameter_count(self):
        n = sum(p.numel() for p in S.SmallCNN(3, 16).parameters())
        self.assertEqual(n, (1 * 8 * 9 + 8) + (8 * 16 * 9 + 16) + (256 * 3 + 3))
''',
"feedback": [
    ("test_shapes_through_network", "Two padded 3×3 convolutions with 2×2 max pooling; classifier input 16 * (size // 4) ** 2."),
    ("test_learns_shapes", "Scale pixels to [0, 1], add the channel axis and train with Adam and CrossEntropyLoss."),
    ("test_reproducible", "Seed before building the model and pass a seeded generator to the DataLoader."),
    ("test_eval_mode_and_types", "Call model.eval() and return predictions as a list of ints."),
],
},
# ---------------------------------------------------------------- cv-augmentation
{
"slug": "cv-augmentation", "title": "Data Augmentation",
"difficulty": "advanced", "prereqs": ["cv-small-cnn"], "packages": CV_PACKAGES,
"objectives": ["Write label-preserving augmentations: flips, small shifts and brightness changes",
               "Apply augmentations reproducibly with a seeded generator",
               "Keep augmented images in the valid uint8 range"],
"tags": ["opencv", "data-augmentation", "regularisation", "image-classification"],
"sources": ["S125", "S116"], "entry": "augment(image, rng, max_shift=2); augment_batch(images, seed=0, max_shift=2)",
"article": r'''
# Data Augmentation

## Intuition
A cat is still a cat when the photo is mirrored, shifted a little or slightly darker. Showing the
network randomly transformed copies of each training image during training teaches it that these
changes do not matter, which works like having more data.

## Precise explanation
An augmentation must **preserve the label**. Typical choices for photos:

* horizontal flip with probability 0.5 (not for text or digits, where mirroring changes meaning);
* translation by a few pixels with `cv2.warpAffine` ([[cv-geometric-transforms]]);
* brightness scaling by a factor in [0.8, 1.2], computed in float and clipped back to [0, 255].

```python
rng = np.random.default_rng(seed)
if rng.random() < 0.5:
    image = cv2.flip(image, 1)
dx, dy = rng.integers(-2, 3, size=2)
image = cv2.warpAffine(image, np.float32([[1, 0, dx], [0, 1, dy]]), (w, h))
image = np.clip(image.astype(np.float32) * rng.uniform(0.8, 1.2), 0, 255).astype(np.uint8)
```

* Augment **only the training data**, and freshly every epoch; evaluate on unchanged images.
* Draw all random choices from one seeded generator so a run can be reproduced.
* Libraries such as `torchvision.transforms` and Albumentations provide ready-made pipelines of
  these operations.

## Worked example
Training the small CNN of [[cv-small-cnn]] on 60 images, then testing on images shifted to new
positions: without augmentation accuracy drops noticeably; with random shifts during training it
stays high, because the network has seen shapes in many positions.

## Common mistakes
* Augmenting the test set.
* Transforms that change the label (flipping a "b" into a "d", rotating a "6" into a "9").
* Brightness changes on uint8 arrays without float conversion and clipping.
* Using an unseeded generator, so results cannot be reproduced.

## Why this matters
Augmentation is one of the most effective regularisers for vision models and is standard in every
modern training pipeline; the shape-sorter project idea uses it.
''',
"statement": r'''
1. `augment(image, rng, max_shift=2)` for a 2-D or 3-D `uint8` image, using the NumPy generator
   `rng` in this order:
   * if `rng.random() < 0.5`, flip horizontally with `cv2.flip(image, 1)`;
   * `dx, dy = rng.integers(-max_shift, max_shift + 1, size=2)`, then translate with `warpAffine`
     (uncovered pixels 0);
   * multiply by `rng.uniform(0.8, 1.2)` in float32, clip to [0, 255] and convert back to uint8.
   Return an image with the same shape and dtype. Raise `ValueError` for non-uint8 input.
2. `augment_batch(images, seed=0, max_shift=2)` augments each image in order with one generator
   `np.random.default_rng(seed)` and returns a NumPy array of the same shape.
''',
"starter": r'''
import cv2
import numpy as np


def augment(image, rng, max_shift=2):
    # TODO
    pass


def augment_batch(images, seed=0, max_shift=2):
    # TODO
    pass
''',
"hints": [
    "Keep the order of random draws exactly as stated, so results are reproducible.",
    "`M = np.float32([[1, 0, dx], [0, 1, dy]])`; `cv2.warpAffine(image, M, (w, h))`.",
    "`np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)`.",
],
"solution": r'''
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
''',
"explanation": r'''
Each augmentation draws its random choices from the generator in a fixed order, so the same seed
always produces the same batch. Flip and shift rearrange pixels; the brightness change is done in
float and clipped so no value wraps around.
''',
"tests": r'''
import numpy as np


def bar(horizontal=True, size=16):
    img = np.zeros((size, size), np.uint8)
    if horizontal:
        img[8, 3:13] = 200
    else:
        img[3:13, 8] = 200
    return img


class TestAugmentation(unittest.TestCase):
    def test_shape_and_dtype(self):
        rng = np.random.default_rng(0)
        for image in (bar(), np.zeros((12, 10, 3), np.uint8)):
            out = S.augment(image, rng)
            self.assertEqual((out.shape, out.dtype), (image.shape, np.uint8))

    def test_reproducible(self):
        images = np.stack([bar(i % 2 == 0) for i in range(6)])
        self.assertTrue(np.array_equal(S.augment_batch(images, seed=4), S.augment_batch(images, seed=4)))
        self.assertFalse(np.array_equal(S.augment_batch(images, seed=4), S.augment_batch(images, seed=5)))

    def test_label_preserved(self):
        rng = np.random.default_rng(1)
        for _ in range(20):
            out = S.augment(bar(True), rng).astype(int)
            self.assertGreater(out.sum(axis=1).max(), 3 * out.sum(axis=0).max())

    def test_values_clipped(self):
        rng = np.random.default_rng(2)
        bright = np.full((8, 8), 250, np.uint8)
        outs = [S.augment(bright, rng, max_shift=0) for _ in range(20)]
        self.assertTrue(all(int(o.max()) <= 255 for o in outs))
        self.assertTrue(any(int(o.max()) == 255 for o in outs))

    def test_zero_shift_and_flip_frequency(self):
        rng = np.random.default_rng(3)
        img = np.zeros((6, 6), np.uint8); img[:, 0] = 100
        flips = sum(int(S.augment(img, rng, max_shift=0)[0, 5] > 0) for _ in range(200))
        self.assertTrue(60 < flips < 140)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.augment(np.zeros((4, 4), np.float32), np.random.default_rng(0))
''',
"feedback": [
    ("test_reproducible", "Use one np.random.default_rng(seed) for the whole batch and draw in the stated order."),
    ("test_label_preserved", "Use small shifts and horizontal flips only, so a horizontal bar stays horizontal."),
    ("test_values_clipped", "Scale brightness in float32 and clip to [0, 255] before converting to uint8."),
    ("test_zero_shift_and_flip_frequency", "Flip when rng.random() < 0.5."),
],
},
# ---------------------------------------------------------------- cv-connected-components
{
"slug": "cv-connected-components", "title": "Connected Components with OpenCV",
"difficulty": "advanced", "prereqs": ["non-max-suppression"], "packages": CV_PACKAGES,
"objectives": ["Label blobs with cv2.connectedComponentsWithStats",
               "Read each component's area, bounding box and centroid from the stats table",
               "Compare 4- and 8-connectivity and filter small components"],
"tags": ["opencv", "connected-components", "segmentation", "counting"],
"sources": ["S121", "S023"], "entry": "label_objects(mask, connectivity=8, min_area=1)",
"article": r'''
# Connected Components with OpenCV

## Intuition
Counting objects in a mask means grouping touching foreground pixels into blobs and numbering them.
Unlike contours, connected components count every **pixel**, so areas are exact, and each pixel gets
the label of its blob.

## Precise explanation
```python
n, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
```

* `n` counts the components **including the background** (label 0).
* `labels` is an int32 image: 0 for background, 1 … n − 1 for components.
* `stats[i]` is `[x, y, width, height, area]` (use `cv2.CC_STAT_AREA` etc. as indices); `area` is
  the pixel count.
* `centroids[i]` is the (x, y) mean position of the component's pixels.
* `connectivity=4` joins pixels that share an edge; `8` also joins diagonal neighbours. Two pixels
  touching only at a corner are one object with 8-connectivity and two with 4.

## Worked example
A 5 × 8 rectangle (40 pixels) and a 4 × 4 square (16 pixels) give n = 3, areas [40, 16] and
centroids (7.5, 7.0) and (15.5, 15.5). Removing components below 20 pixels leaves one object.

## What the library does inside
The flood fill of [[connected-components]] (the optional deep dive after this step), done in two
fast raster passes with union–find.

## Common mistakes
* Forgetting that label 0 / `stats[0]` is the background.
* Counting noise speckles as objects — filter by area.
* Using 4-connectivity for thin diagonal structures and splitting them.

## Why this matters
Counting cells, coins, defects or parked cars usually ends with connected components; the
object-counter project idea after this step combines them with thresholding and NMS.
''',
"statement": r'''
Write `label_objects(mask, connectivity=8, min_area=1)` returning
`{"count": int, "areas": list[int], "boxes": list[tuple], "centroids": list[tuple]}` for the
non-background components whose area is at least `min_area`, in label order.

* Use `cv2.connectedComponentsWithStats(mask, connectivity=connectivity)`.
* `boxes` are `(x, y, w, h)` int tuples, `centroids` `(cx, cy)` float tuples.
* Raise `ValueError` unless `mask` is 2-D `uint8` and `connectivity` is 4 or 8.
''',
"starter": r'''
import cv2
import numpy as np


def label_objects(mask, connectivity=8, min_area=1):
    # TODO
    pass
''',
"hints": [
    "Validate the mask and connectivity first.",
    "`n, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=connectivity)`.",
    "Loop over `range(1, n)`: `x, y, w, h, area = stats[i]` and keep those with `area >= min_area`.",
],
"solution": r'''
import cv2
import numpy as np


def label_objects(mask, connectivity=8, min_area=1):
    if not isinstance(mask, np.ndarray) or mask.ndim != 2 or mask.dtype != np.uint8:
        raise ValueError("expected a 2-D uint8 mask")
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    n, _, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=connectivity)
    areas, boxes, centres = [], [], []
    for i in range(1, n):
        x, y, w, h, area = (int(v) for v in stats[i])
        if area < min_area:
            continue
        areas.append(area)
        boxes.append((x, y, w, h))
        centres.append((float(centroids[i][0]), float(centroids[i][1])))
    return {"count": len(areas), "areas": areas, "boxes": boxes, "centroids": centres}
''',
"explanation": r'''
OpenCV labels every pixel and returns one stats row and centroid per label. Skipping label 0
removes the background; the area filter drops speckles; the remaining rows are converted to plain
ints and floats.
''',
"tests": r'''
import numpy as np


def scene():
    mask = np.zeros((30, 30), np.uint8)
    mask[5:10, 4:12] = 255
    mask[14:18, 14:18] = 255
    mask[25, 25] = 255
    return mask


class TestLabelObjects(unittest.TestCase):
    def test_counts_and_areas(self):
        r = S.label_objects(scene())
        self.assertEqual(r["count"], 3)
        self.assertEqual(r["areas"], [40, 16, 1])

    def test_boxes_and_centroids(self):
        r = S.label_objects(scene())
        self.assertEqual(r["boxes"][:2], [(4, 5, 8, 5), (14, 14, 4, 4)])
        self.assertAlmostEqual(r["centroids"][0][0], 7.5)
        self.assertAlmostEqual(r["centroids"][1][1], 15.5)

    def test_min_area(self):
        r = S.label_objects(scene(), min_area=20)
        self.assertEqual((r["count"], r["areas"]), (1, [40]))

    def test_connectivity(self):
        diagonal = np.zeros((4, 4), np.uint8)
        diagonal[0, 0] = diagonal[1, 1] = diagonal[2, 2] = 255
        self.assertEqual(S.label_objects(diagonal, connectivity=8)["count"], 1)
        self.assertEqual(S.label_objects(diagonal, connectivity=4)["count"], 3)

    def test_types_and_empty(self):
        r = S.label_objects(scene())
        self.assertTrue(all(type(v) is int for box in r["boxes"] for v in box))
        self.assertTrue(all(type(v) is float for c in r["centroids"] for v in c))
        self.assertEqual(S.label_objects(np.zeros((5, 5), np.uint8))["count"], 0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.label_objects(scene(), connectivity=6)
        with self.assertRaises(ValueError):
            S.label_objects(scene().astype(np.int32))
''',
"feedback": [
    ("test_counts_and_areas", "Skip label 0, the background, and report stats areas in label order."),
    ("test_min_area", "Keep only components with area >= min_area."),
    ("test_connectivity", "Pass connectivity through to connectedComponentsWithStats."),
    ("test_types_and_empty", "Convert stats to ints and centroids to floats."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "document-scanner", "title": "Document Scanner",
"tags": ["opencv", "contours", "perspective"],
"brief": r'''
Turn a phone photo of a page lying on a desk into a flat, black-and-white scan: find the page,
straighten it, and clean up the lighting — what scanner apps do.
''',
"uses": ["cv-opencv-basics", "cv-geometric-transforms", "cv-threshold-otsu", "cv-sobel-canny", "cv-contours"],
"milestones": [
    "Load a photo, resize it to about 800 pixels wide and convert it to greyscale.",
    "Blur, run Canny and find the largest contour.",
    "Approximate the contour with cv2.approxPolyDP until it has four corners; draw them on the photo.",
    "Order the corners and warp the page flat with cv2.getPerspectiveTransform and cv2.warpPerspective.",
    "Clean the result with adaptive or Otsu thresholding and save it as a PNG.",
],
"stretch": [
    "Handle photos where the page is not the largest object.",
    "Process a folder of photos into one multi-page PDF.",
    "Add a fallback that lets the user click the four corners when detection fails.",
],
"data": r'''
Photograph a few printed pages on a contrasting desk with your phone (different angles and lighting).
No dataset download is needed.
''',
"setup": r'''
```bash
pip install opencv-python numpy
python scan.py photo.jpg scanned.png
```
''',
},
{
"kind": "project", "slug": "shape-sorter", "title": "Shape and Colour Sorter",
"tags": ["cnn", "augmentation", "image-classification"],
"brief": r'''
Train a CNN that sorts photos of simple objects — for example coloured blocks, coins or bottle caps —
into classes, and test it with your webcam or new photos taken in different light.
''',
"uses": ["cv-opencv-basics", "cv-resize", "cv-small-cnn", "cv-augmentation", "torch-training-loop"],
"milestones": [
    "Collect 30–50 photos per class (or generate synthetic shapes) and resize them to 64×64.",
    "Split into train, validation and test folders and write a Dataset that loads them with OpenCV.",
    "Train the small CNN, adapted to 3 colour channels and 64×64 inputs.",
    "Add augmentation (flips, shifts, brightness) and compare validation accuracy with and without it.",
    "Classify frames from a webcam with cv2.VideoCapture and show the predicted label on screen.",
],
"stretch": [
    "Fine-tune a pretrained torchvision model (for example ResNet-18) and compare.",
    "Add a confidence threshold that answers 'unknown' for low-probability predictions.",
    "Export the model with TorchScript or ONNX.",
],
"data": r'''
Take your own photos with a phone or webcam. For a synthetic start, draw coloured circles, squares and
triangles with `cv2.circle`, `cv2.rectangle` and `cv2.fillPoly` at random positions and sizes.
''',
"setup": r'''
```bash
pip install torch opencv-python numpy
python train_sorter.py data/
```
''',
},
{
"kind": "project", "slug": "object-counter", "title": "Simple Object Counter",
"tags": ["segmentation", "counting", "connected-components"],
"brief": r'''
Count objects in images — coins on a table or cell nuclei under a microscope — and report their
sizes. Compare your counts with the ground truth and find out which images are hard and why.
''',
"uses": ["cv-threshold-otsu", "cv-contours", "iou", "non-max-suppression", "cv-connected-components"],
"milestones": [
    "Load an image, convert to greyscale, blur and threshold with Otsu.",
    "Clean the mask with morphological opening (cv2.morphologyEx) to remove speckles.",
    "Count objects with connectedComponentsWithStats and filter by area.",
    "Draw numbered bounding boxes and save an annotated image.",
    "On a labelled dataset, compare counts with the ground truth and report the mean absolute error.",
],
"stretch": [
    "Separate touching objects with the distance transform and watershed.",
    "Match predicted boxes to ground-truth boxes with IoU and report precision and recall.",
    "Measure object sizes in millimetres using a reference object of known size.",
],
"data": r'''
* [BBBC039](https://bbbc.broadinstitute.org/BBBC039): fluorescent nuclei images with ground-truth
  masks (Broad Bioimage Benchmark Collection).
* A coins image ships with scikit-image: `skimage.data.coins()`
  ([data module](https://scikit-image.org/docs/stable/api/skimage.data.html)), or photograph coins yourself.
''',
"setup": r'''
```bash
pip install opencv-python numpy scikit-image
python count.py image.png
```
''',
},
]
