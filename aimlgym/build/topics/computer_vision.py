"""Problem definitions for the computer vision topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- rgb-to-gray
{
"slug": "rgb-to-gray", "title": "RGB to Grayscale",
"difficulty": "beginner", "prereqs": ["image-arrays"], "packages": ["numpy"],
"objectives": ["Represent colour images as (H, W, 3) arrays", "Convert to luminance with weighted channels",
               "Convert safely to uint8 with rounding and clipping"],
"tags": ["images", "grayscale", "colour", "dtype"],
"sources": ["S023", "S006"], "entry": "rgb_to_gray(img); to_uint8(x)",
"article": r'''
# Images as Arrays and Grayscale Conversion

## Intuition
A colour image is a grid of pixels, each with red, green and blue intensities. Our eyes are most
sensitive to green and least to blue, so a perceptually sensible grey level weights green most.

## Precise explanation
* Colour image: array `(H, W, 3)`, usually `uint8` in 0..255 (RGB order here; OpenCV loads BGR).
* Grayscale: `(H, W)`.
* ITU-R BT.601 luma weights (used by OpenCV's `cvtColor` RGB→GRAY):
  $Y = 0.299R + 0.587G + 0.114B$. With broadcasting: `img @ np.array([0.299, 0.587, 0.114])`.
* Arithmetic on `uint8` wraps around (250 + 10 = 4). Convert to float first; convert back with
  rounding and clipping to [0, 255].

## Worked example
Pure red (255, 0, 0) → 76.245 → 76; pure green → 149.685 → 150; white → 255.

## Common mistakes
* Averaging channels equally (looks wrong: blue appears too bright).
* BGR/RGB confusion with OpenCV.
* `astype(np.uint8)` without rounding/clipping (truncation and wrap-around).

## Why this matters
Many classical algorithms (edges, thresholding) work on single-channel images; dtype handling
prevents silent overflow bugs.
''',
"statement": r'''
Implement:
* `rgb_to_gray(img)` → float array `(H, W)` with BT.601 weights; raise `ValueError` unless
  `img.shape[-1] == 3` and `img.ndim == 3`.
* `to_uint8(x)` → round to nearest (`np.rint`), clip to [0, 255], return `uint8`.

**Examples**
```python
img = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]], dtype=np.uint8)
to_uint8(rgb_to_gray(img))   # [[ 76, 150], [ 29, 255]]
to_uint8(np.array([-5., 300., 12.5]))   # [  0, 255,  12]   (rint rounds half to even)
```
''',
"starter": r'''
import numpy as np


def rgb_to_gray(img):
    pass


def to_uint8(x):
    pass
''',
"hints": [
    "Convert with `img.astype(float)` before multiplying.",
    "`img @ np.array([0.299, 0.587, 0.114])` contracts the channel axis.",
    "`np.clip(np.rint(x), 0, 255).astype(np.uint8)`.",
],
"solution": r'''
import numpy as np

WEIGHTS = np.array([0.299, 0.587, 0.114])


def rgb_to_gray(img):
    img = np.asarray(img)
    if img.ndim != 3 or img.shape[-1] != 3:
        raise ValueError("expected an (H, W, 3) image")
    return img.astype(float) @ WEIGHTS


def to_uint8(x):
    return np.clip(np.rint(np.asarray(x, dtype=float)), 0, 255).astype(np.uint8)
''',
"explanation": r'''
Casting to float avoids uint8 overflow; a matrix product with the weight vector collapses the
channel axis. Conversion back rounds, clips and casts, in that order.
''',
"tests": r'''
import numpy as np

IMG = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]], dtype=np.uint8)

class TestGray(unittest.TestCase):
    def test_values(self):
        np.testing.assert_allclose(S.rgb_to_gray(IMG), [[76.245, 149.685], [29.07, 255.0]])

    def test_uint8(self):
        np.testing.assert_array_equal(S.to_uint8(S.rgb_to_gray(IMG)), [[76, 150], [29, 255]])

    def test_no_overflow(self):
        g = S.rgb_to_gray(np.full((1, 1, 3), 255, dtype=np.uint8))
        self.assertAlmostEqual(float(g[0, 0]), 255.0)

    def test_clip_round(self):
        np.testing.assert_array_equal(S.to_uint8(np.array([-5., 300., 12.5, 12.6])), [0, 255, 12, 13])
        self.assertEqual(S.to_uint8(np.array([1.0])).dtype, np.uint8)

    def test_shape(self):
        self.assertEqual(S.rgb_to_gray(np.zeros((4, 5, 3))).shape, (4, 5))

    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            S.rgb_to_gray(np.zeros((4, 4)))
''',
"feedback": [
    ("test_values", "Use weights 0.299, 0.587, 0.114 for R, G, B."),
    ("test_no_overflow", "Convert to float before arithmetic; uint8 wraps around."),
    ("test_clip_round", "Round with np.rint, then clip, then cast to uint8."),
    ("test_bad_shape", "Require ndim == 3 and 3 channels."),
],
},
# ---------------------------------------------------------------- flip-rotate
{
"slug": "flip-rotate", "title": "Flip and Rotate", "optional": True,
"difficulty": "beginner", "prereqs": ["image-arrays"], "packages": ["numpy"],
"objectives": ["Flip images with negative-step slicing", "Rotate by 90° using transpose + flip",
               "Use flips/rotations as data augmentation"],
"tags": ["geometric-transforms", "augmentation", "slicing"],
"sources": ["S006", "S013"], "entry": "flip_horizontal(img); flip_vertical(img); rotate90_cw(img, k=1)",
"article": r'''
# Flips and 90° Rotations

## Intuition
A mirrored photo of a cat is still a cat. Flips and rotations create extra training examples for
free (**data augmentation**) and are pure index rearrangements — no interpolation needed.

## Precise explanation
For an image with rows (axis 0) and columns (axis 1):
* Horizontal flip (left↔right): `img[:, ::-1]`.
* Vertical flip (top↔bottom): `img[::-1, :]`.
* Rotate 90° **clockwise**: transpose rows/columns, then flip horizontally:
  `img.transpose(1, 0, *rest)[:, ::-1]`. Applying it k times rotates by 90k°; k mod 4 matters.
* `np.rot90(img, k)` rotates **counter-clockwise** — a classic source of confusion.
These work for `(H, W)` and `(H, W, C)` (channels must stay last).

## Worked example
```
[[1, 2, 3],        cw        [[4, 1],
 [4, 5, 6]]      ------>      [5, 2],
                              [6, 3]]
```

## Common mistakes
* Using `np.rot90` and rotating the wrong way.
* Transposing a colour image with `.T` (reverses all three axes, moving channels first).
* Flipping digits/text where orientation changes meaning (augmentation must preserve labels).

## Why this matters
Augmentation pipelines in every CV training script use these operations.
''',
"statement": r'''
Implement (return arrays; `(H, W)` or `(H, W, C)` input):
* `flip_horizontal(img)`, `flip_vertical(img)`.
* `rotate90_cw(img, k=1)` → rotate clockwise by 90°·k (any integer k, negative = counter-clockwise),
  **without** `np.rot90`.

**Example**
```python
a = np.array([[1, 2, 3], [4, 5, 6]])
rotate90_cw(a)     # [[4, 1], [5, 2], [6, 3]]
flip_horizontal(a) # [[3, 2, 1], [6, 5, 4]]
```
''',
"starter": r'''
import numpy as np


def flip_horizontal(img):
    pass


def flip_vertical(img):
    pass


def rotate90_cw(img, k=1):
    pass
''',
"hints": [
    "Slicing: `img[:, ::-1]` and `img[::-1]`.",
    "One clockwise step: `np.swapaxes(img, 0, 1)[:, ::-1]`.",
    "Use `k % 4` repetitions.",
],
"solution": r'''
import numpy as np


def flip_horizontal(img):
    return np.asarray(img)[:, ::-1]


def flip_vertical(img):
    return np.asarray(img)[::-1]


def rotate90_cw(img, k=1):
    out = np.asarray(img)
    for _ in range(k % 4):
        out = np.swapaxes(out, 0, 1)[:, ::-1]
    return out
''',
"explanation": r'''
Negative-step slices reverse an axis. Swapping the two spatial axes and then reversing columns
maps pixel (r, c) to (c, H−1−r), a clockwise quarter turn; channels stay last because only axes
0 and 1 are swapped.
''',
"tests": r'''
import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6]])

class TestFlipRotate(unittest.TestCase):
    def test_flips(self):
        np.testing.assert_array_equal(S.flip_horizontal(A), [[3, 2, 1], [6, 5, 4]])
        np.testing.assert_array_equal(S.flip_vertical(A), [[4, 5, 6], [1, 2, 3]])

    def test_cw(self):
        np.testing.assert_array_equal(S.rotate90_cw(A), [[4, 1], [5, 2], [6, 3]])

    def test_matches_rot90_negative(self):
        for k in range(-3, 6):
            np.testing.assert_array_equal(S.rotate90_cw(A, k), np.rot90(A, -k))

    def test_four_is_identity(self):
        np.testing.assert_array_equal(S.rotate90_cw(A, 4), A)

    def test_color(self):
        img = np.arange(2 * 3 * 3).reshape(2, 3, 3)
        out = S.rotate90_cw(img)
        self.assertEqual(out.shape, (3, 2, 3))
        np.testing.assert_array_equal(out[0, 0], img[1, 0])

    def test_double_flip(self):
        np.testing.assert_array_equal(S.flip_horizontal(S.flip_horizontal(A)), A)
''',
"feedback": [
    ("test_cw", "Clockwise = swap spatial axes, then flip horizontally."),
    ("test_matches_rot90_negative", "np.rot90 is counter-clockwise; use k % 4 steps of your own rotation."),
    ("test_color", "Only swap axes 0 and 1 so channels stay last (don't use .T on 3-D arrays)."),
    ("test_flips", "Horizontal flip reverses columns: img[:, ::-1]."),
],
},
# ---------------------------------------------------------------- threshold-binary
{
"slug": "threshold-binary", "title": "Binary Thresholding", "optional": True,
"difficulty": "beginner", "prereqs": ["rgb-to-gray"], "packages": ["numpy"],
"objectives": ["Create binary masks from grayscale images", "Invert masks and measure foreground fraction",
               "Apply a mask to an image"],
"tags": ["thresholding", "segmentation", "masks"],
"sources": ["S023"], "entry": "threshold(gray, t, invert=False); foreground_fraction(mask); apply_mask(img, mask)",
"article": r'''
# Binary Thresholding

## Intuition
To separate dark text from a white page, call every pixel brighter than some level "background"
and the rest "foreground". Thresholding is the simplest segmentation.

## Precise explanation
* Binary threshold: `mask = gray > t` (OpenCV's `THRESH_BINARY` uses strictly greater than).
  `invert=True` gives `gray <= t`.
* Foreground fraction = `mask.mean()` (True counts as 1).
* Applying a mask: keep pixels where mask is True, zero elsewhere — `np.where(mask[..., None], img, 0)`
  for colour images (the mask broadcasts over channels).
* Choosing t automatically: Otsu's method ([[intensity-histogram]] extension) picks the threshold that best separates
  two histogram modes.

## Worked example
gray [[10, 200], [128, 127]], t = 127 → mask [[F, T], [T, F]] → fraction 0.5.

## Common mistakes
* `>=` vs `>` at the boundary.
* Producing 0/255 uint8 images and then using them as booleans incorrectly.
* Forgetting to broadcast the mask over colour channels.

## Why this matters
Masks are the language of segmentation: models output per-pixel masks and evaluation compares them.
''',
"statement": r'''
Implement:
* `threshold(gray, t, invert=False)` → boolean mask (`gray > t`, or `gray <= t` if inverted).
* `foreground_fraction(mask)` → float fraction of True pixels (raise `ValueError` for empty).
* `apply_mask(img, mask)` → copy of `img` (gray or colour) with pixels outside the mask set to 0;
  raise `ValueError` if spatial shapes differ.

**Example**
```python
g = np.array([[10, 200], [128, 127]])
threshold(g, 127)            # [[False, True], [True, False]]
foreground_fraction(threshold(g, 127))   # 0.5
```
''',
"starter": r'''
import numpy as np


def threshold(gray, t, invert=False):
    pass


def foreground_fraction(mask):
    pass


def apply_mask(img, mask):
    pass
''',
"hints": [
    "`m = np.asarray(gray) > t`; return `~m` if invert.",
    "`float(np.mean(mask))`.",
    "For colour: `mask[..., None]` broadcasts over channels; use `np.where`.",
],
"solution": r'''
import numpy as np


def threshold(gray, t, invert=False):
    m = np.asarray(gray) > t
    return ~m if invert else m


def foreground_fraction(mask):
    mask = np.asarray(mask, dtype=bool)
    if mask.size == 0:
        raise ValueError("empty mask")
    return float(mask.mean())


def apply_mask(img, mask):
    img = np.asarray(img)
    mask = np.asarray(mask, dtype=bool)
    if img.shape[:2] != mask.shape:
        raise ValueError("mask must match image height and width")
    m = mask if img.ndim == 2 else mask[..., None]
    return np.where(m, img, 0).astype(img.dtype)
''',
"explanation": r'''
A comparison produces the mask; inversion is logical NOT. The mean of a boolean mask is the
foreground fraction. Masking uses `np.where`, adding a channel axis for colour images so the mask
broadcasts, and preserves the input dtype.
''',
"tests": r'''
import numpy as np

G = np.array([[10, 200], [128, 127]])

class TestThreshold(unittest.TestCase):
    def test_threshold(self):
        np.testing.assert_array_equal(S.threshold(G, 127), [[False, True], [True, False]])

    def test_invert(self):
        np.testing.assert_array_equal(S.threshold(G, 127, invert=True), [[True, False], [False, True]])

    def test_fraction(self):
        self.assertEqual(S.foreground_fraction(S.threshold(G, 127)), 0.5)

    def test_apply_gray(self):
        np.testing.assert_array_equal(S.apply_mask(G, S.threshold(G, 127)), [[0, 200], [128, 0]])

    def test_apply_color(self):
        img = np.full((2, 2, 3), 9, dtype=np.uint8)
        out = S.apply_mask(img, np.array([[True, False], [False, True]]))
        np.testing.assert_array_equal(out[0, 1], [0, 0, 0])
        np.testing.assert_array_equal(out[1, 1], [9, 9, 9])
        self.assertEqual(out.dtype, np.uint8)

    def test_shape_mismatch(self):
        with self.assertRaises(ValueError):
            S.apply_mask(G, np.ones((3, 3), bool))

    def test_no_mutation(self):
        g = G.copy()
        S.apply_mask(g, np.zeros((2, 2), bool))
        np.testing.assert_array_equal(g, G)
''',
"feedback": [
    ("test_threshold", "Use strict > t (127 is not foreground at t = 127)."),
    ("test_apply_color", "Broadcast the mask over channels with mask[..., None]."),
    ("test_no_mutation", "Return a new array (np.where) instead of assigning into img."),
    ("test_shape_mismatch", "Compare img.shape[:2] with mask.shape."),
],
},
# ---------------------------------------------------------------- intensity-histogram
{
"slug": "intensity-histogram", "title": "Intensity Histogram", "optional": True,
"difficulty": "beginner", "prereqs": ["rgb-to-gray", "histogram-bins"], "packages": ["numpy"],
"objectives": ["Count pixel intensities with np.bincount", "Compute a cumulative distribution",
               "Apply histogram equalisation"],
"tags": ["histograms", "contrast", "equalisation", "cdf"],
"sources": ["S023", "S006"], "entry": "histogram256(gray); cdf(hist); equalize(gray)",
"article": r'''
# Intensity Histograms and Equalisation

## Intuition
A dark, low-contrast photo has all its pixel values bunched together. Histogram equalisation spreads
them across the full 0–255 range, like stretching a crumpled spring.

## Precise explanation
* For `uint8` images, `np.bincount(gray.ravel(), minlength=256)` gives exactly 256 counts.
* CDF: `np.cumsum(hist)` (counts) — normalised version divides by the number of pixels.
* **Equalisation** (classic formula, as in OpenCV's `equalizeHist` description): with $c$ the count
  CDF, $c_\min$ the smallest non-zero CDF value and $N$ pixels,
  $$v' = \operatorname{round}\!\left(\frac{c(v) - c_\min}{N - c_\min}\cdot 255\right).$$
  If all pixels share one value ($N = c_\min$), return the image unchanged.
The mapping is monotone (brighter stays brighter) and uses the image's own statistics.

## Worked example
gray values {50, 50, 51, 52}: hist[50]=2, hist[51]=1, hist[52]=1; CDF at 50/51/52 = 2/3/4;
c_min = 2, N = 4 → 50→0, 51→round(1/2·255)=128, 52→255.

## Common mistakes
* `np.histogram` with default bins (10, not 256).
* Using the CDF value at 0 instead of the first non-zero value.
* Forgetting to round/convert back to uint8.

## Why this matters
Contrast normalisation is a classic preprocessing step; histograms also summarise images for
retrieval and quality checks.
''',
"statement": r'''
For `uint8` grayscale images implement:
* `histogram256(gray)` → int array of length 256 (raise `ValueError` if dtype is not uint8).
* `cdf(hist)` → cumulative counts.
* `equalize(gray)` → uint8 image using the formula above (rounding with `np.rint`).

**Example**
```python
g = np.array([[50, 50], [51, 52]], dtype=np.uint8)
equalize(g)   # [[  0,   0], [128, 255]]
```
''',
"starter": r'''
import numpy as np


def histogram256(gray):
    pass


def cdf(hist):
    pass


def equalize(gray):
    pass
''',
"hints": [
    "`np.bincount(gray.ravel(), minlength=256)`.",
    "`c_min = c[c > 0].min()`; build a 256-entry lookup table.",
    "`lut[gray]` applies the mapping to every pixel at once.",
],
"solution": r'''
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
''',
"explanation": r'''
`bincount` counts each of the 256 intensities. The cumulative counts define a monotone lookup table
that maps the darkest present value to 0 and the brightest to 255; fancy indexing applies the table
to all pixels.
''',
"tests": r'''
import numpy as np

class TestHist(unittest.TestCase):
    def test_hist(self):
        h = S.histogram256(np.array([[0, 0], [255, 7]], dtype=np.uint8))
        self.assertEqual(len(h), 256)
        self.assertEqual((h[0], h[7], h[255], h.sum()), (2, 1, 1, 4))

    def test_dtype_check(self):
        with self.assertRaises(ValueError):
            S.histogram256(np.zeros((2, 2), dtype=float))

    def test_cdf(self):
        np.testing.assert_array_equal(S.cdf([1, 0, 2]), [1, 1, 3])

    def test_equalize(self):
        g = np.array([[50, 50], [51, 52]], dtype=np.uint8)
        np.testing.assert_array_equal(S.equalize(g), [[0, 0], [128, 255]])

    def test_full_range(self):
        g = np.array([[100, 101, 102, 103]], dtype=np.uint8)
        e = S.equalize(g)
        self.assertEqual((e.min(), e.max()), (0, 255))
        self.assertEqual(e.dtype, np.uint8)

    def test_monotone(self):
        rng = np.random.default_rng(0)
        g = rng.integers(60, 120, size=(16, 16)).astype(np.uint8)
        e = S.equalize(g)
        order = np.argsort(g.ravel(), kind="stable")
        self.assertTrue((np.diff(e.ravel()[order].astype(int)) >= 0).all())

    def test_constant(self):
        g = np.full((3, 3), 77, dtype=np.uint8)
        np.testing.assert_array_equal(S.equalize(g), g)
''',
"feedback": [
    ("test_hist", "Use np.bincount(..., minlength=256)."),
    ("test_equalize", "Use the first non-zero CDF value as c_min and N − c_min in the denominator."),
    ("test_constant", "If every pixel has the same value, return the image unchanged."),
    ("test_full_range", "Round the lookup table and cast to uint8."),
],
},
# ---------------------------------------------------------------- conv2d-filter
{
"slug": "conv2d-filter", "title": "2D Filtering (Blur)",
"difficulty": "intermediate", "prereqs": ["rgb-to-gray", "torch-conv1d"], "packages": ["numpy"],
"objectives": ["Implement 2-D cross-correlation with 'same' output size", "Choose border handling (zero vs edge)",
               "Build box and Gaussian kernels"],
"tags": ["filtering", "convolution", "blur", "kernels", "padding"],
"sources": ["S015", "S006", "S023"], "entry": "filter2d(img, kernel, mode='zero'); box_kernel(k); gaussian_kernel(k, sigma)",
"article": r'''
# 2-D Filtering

## Intuition
Blurring replaces each pixel by an average of its neighbourhood. Slide a small grid of weights
(kernel) over the image; at each position, multiply and add.

## Precise explanation
For an odd-sized kernel `(kh, kw)` with radius $r_h = kh//2$, $r_w = kw//2$:
$$\text{out}[i, j] = \sum_{u,v} \text{pad}(img)[i+u,\ j+v]\cdot K[u, v],$$
after padding by $(r_h, r_w)$ so the output has the **same** size as the input. This is
cross-correlation (no kernel flip), as in CNN layers ([[conv1d]]) and OpenCV's `filter2D`.
Border modes: **zero** padding (`np.pad(..., mode="constant")`) darkens edges; **edge** padding
(`mode="edge"`) repeats the border pixel.
* Box kernel: all entries $1/k^2$.
* Gaussian kernel: $G[u,v] \propto \exp(-(x^2+y^2)/(2\sigma^2))$ with $x, y \in \{-r..r\}$,
  normalised to sum to 1 (so overall brightness is preserved).

## Worked example
3×3 box blur on a 3×3 image of ones with zero padding: centre 1.0, edges 6/9, corners 4/9.
With edge padding every output is 1.0.

## Common mistakes
* Even-sized kernels (no centre) — reject them here.
* Using `np.convolve`/flipping the kernel.
* Not normalising blur kernels (image gets brighter).

## Why this matters
Every convolutional layer is this operation with learned kernels; smoothing is also a standard
pre-step before edge detection ([[sobel-edges]]).
''',
"statement": r'''
Implement for 2-D float images:
* `filter2d(img, kernel, mode="zero")` → same-size output; `mode` in {"zero", "edge"}. Kernel
  dimensions must be odd, else `ValueError`. Vectorise over the kernel (looping over kernel
  entries is fine; avoid looping over every pixel).
* `box_kernel(k)` → `(k, k)` with all entries `1/k²` (odd k ≥ 1).
* `gaussian_kernel(k, sigma)` → normalised Gaussian (odd k, sigma > 0).

**Example**
```python
filter2d(np.ones((3, 3)), box_kernel(3))           # [[4/9, 6/9, 4/9], [6/9, 1, 6/9], [4/9, 6/9, 4/9]]
filter2d(np.ones((3, 3)), box_kernel(3), "edge")   # all ones
```
''',
"starter": r'''
import numpy as np


def filter2d(img, kernel, mode="zero"):
    pass


def box_kernel(k):
    pass


def gaussian_kernel(k, sigma):
    pass
''',
"hints": [
    "`P = np.pad(img, ((rh, rh), (rw, rw)), mode='constant' or 'edge')`.",
    "Loop over kernel offsets: `out += K[u, v] * P[u:u+H, v:v+W]`.",
    "Gaussian: `ax = np.arange(k) - k // 2`; `g = np.exp(-(ax[:, None]**2 + ax[None, :]**2) / (2*sigma**2))`.",
],
"solution": r'''
import numpy as np


def filter2d(img, kernel, mode="zero"):
    img = np.asarray(img, dtype=float)
    K = np.asarray(kernel, dtype=float)
    if K.ndim != 2 or K.shape[0] % 2 == 0 or K.shape[1] % 2 == 0:
        raise ValueError("kernel dimensions must be odd")
    if mode not in ("zero", "edge"):
        raise ValueError("mode must be 'zero' or 'edge'")
    rh, rw = K.shape[0] // 2, K.shape[1] // 2
    P = np.pad(img, ((rh, rh), (rw, rw)), mode="constant" if mode == "zero" else "edge")
    H, W = img.shape
    out = np.zeros_like(img)
    for u in range(K.shape[0]):
        for v in range(K.shape[1]):
            out += K[u, v] * P[u:u + H, v:v + W]
    return out


def box_kernel(k):
    if k < 1 or k % 2 == 0:
        raise ValueError("k must be odd and >= 1")
    return np.full((k, k), 1.0 / (k * k))


def gaussian_kernel(k, sigma):
    if k < 1 or k % 2 == 0 or sigma <= 0:
        raise ValueError("odd k >= 1 and sigma > 0 required")
    ax = np.arange(k) - k // 2
    g = np.exp(-(ax[:, None] ** 2 + ax[None, :] ** 2) / (2 * sigma ** 2))
    return g / g.sum()
''',
"explanation": r'''
Padding by the kernel radius keeps the output size equal to the input. Instead of looping over
pixels, the code loops over the (few) kernel entries and adds a shifted copy of the padded image
weighted by that entry — a vectorised cross-correlation.
''',
"tests": r'''
import numpy as np

def naive(img, K, mode):
    rh, rw = K.shape[0] // 2, K.shape[1] // 2
    P = np.pad(img, ((rh, rh), (rw, rw)), mode="constant" if mode == "zero" else "edge")
    return np.array([[(P[i:i + K.shape[0], j:j + K.shape[1]] * K).sum() for j in range(img.shape[1])]
                     for i in range(img.shape[0])])

class TestFilter2d(unittest.TestCase):
    def test_box_zero(self):
        exp = np.array([[4, 6, 4], [6, 9, 6], [4, 6, 4]]) / 9
        np.testing.assert_allclose(S.filter2d(np.ones((3, 3)), S.box_kernel(3)), exp)

    def test_box_edge(self):
        np.testing.assert_allclose(S.filter2d(np.ones((3, 3)), S.box_kernel(3), "edge"), np.ones((3, 3)))

    def test_against_naive(self):
        rng = np.random.default_rng(0)
        img, K = rng.normal(size=(6, 7)), rng.normal(size=(3, 5))
        for mode in ("zero", "edge"):
            np.testing.assert_allclose(S.filter2d(img, K, mode), naive(img, K, mode), atol=1e-12)

    def test_no_flip(self):
        img = np.zeros((3, 3)); img[1, 1] = 1
        K = np.arange(9.).reshape(3, 3)
        np.testing.assert_allclose(S.filter2d(img, K), K[::-1, ::-1])

    def test_gaussian(self):
        g = S.gaussian_kernel(5, 1.0)
        self.assertAlmostEqual(g.sum(), 1.0)
        self.assertEqual(np.unravel_index(g.argmax(), g.shape), (2, 2))
        np.testing.assert_allclose(g, g.T)

    def test_identity_kernel(self):
        img = np.random.default_rng(1).normal(size=(4, 4))
        K = np.zeros((3, 3)); K[1, 1] = 1
        np.testing.assert_allclose(S.filter2d(img, K), img)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.filter2d(np.ones((3, 3)), np.ones((2, 2)))
        with self.assertRaises(ValueError):
            S.box_kernel(4)
''',
"feedback": [
    ("test_box_zero", "Zero padding: border outputs average in zeros."),
    ("test_no_flip", "Cross-correlation: an impulse reproduces the kernel flipped — don't flip it yourself."),
    ("test_against_naive", "Pad by kernel_size // 2 on each side; out[i, j] uses P[i:i+kh, j:j+kw]."),
    ("test_gaussian", "Normalise the Gaussian so it sums to 1."),
],
},
# ---------------------------------------------------------------- sobel-edges
{
"slug": "sobel-edges", "title": "Sobel Edge Magnitude", "optional": True,
"difficulty": "intermediate", "prereqs": ["conv2d-filter"], "packages": ["numpy"],
"objectives": ["Estimate image gradients with Sobel kernels", "Combine gradients into magnitude and direction",
               "Threshold edges"],
"tags": ["edge-detection", "sobel", "gradients"],
"sources": ["S023", "S006"], "entry": "sobel(gray); edges(gray, t)",
"article": r'''
# Sobel Edge Detection

## Intuition
An edge is where brightness changes quickly. The Sobel operator estimates the horizontal and
vertical brightness change at every pixel, smoothing slightly to resist noise.

## Precise explanation
Sobel kernels (applied as cross-correlation, [[conv2d-filter]]):
$$K_x = \begin{pmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{pmatrix},\qquad K_y = K_x^\top.$$
$G_x$ responds to vertical edges (left→right change), $G_y$ to horizontal edges (top→bottom).
Magnitude $\sqrt{G_x^2 + G_y^2}$; direction $\operatorname{atan2}(G_y, G_x)$.
We compute **valid** outputs only (no padding), so the result is `(H−2, W−2)` and border artefacts
are avoided.

## Worked example
Image with left half 0 and right half 10 (vertical edge): $G_x$ = 40 along the edge, $G_y$ = 0;
magnitude 40.

## Common mistakes
* Swapping $K_x$ and $K_y$.
* Using `uint8` (negative gradients wrap around).
* Expecting thin edges — Sobel gives thick responses; non-maximum suppression (Canny) thins them.

## Why this matters
Edge maps were the foundation of classical vision; CNNs' first layers learn Sobel-like filters.
''',
"statement": r'''
Implement:
* `sobel(gray)` → `(gx, gy, magnitude)` arrays of shape `(H-2, W-2)` (valid cross-correlation with
  the kernels above). Raise `ValueError` if the image is smaller than 3×3.
* `edges(gray, t)` → boolean `(H-2, W-2)` mask `magnitude > t`.

**Example**
```python
g = np.array([[0, 0, 10, 10]] * 4, float)
gx, gy, mag = sobel(g)
gx    # [[40., 40.], [40., 40.]]
gy    # [[0., 0.], [0., 0.]]
```
''',
"starter": r'''
import numpy as np

KX = np.array([[-1., 0., 1.], [-2., 0., 2.], [-1., 0., 1.]])
KY = KX.T


def sobel(gray):
    pass


def edges(gray, t):
    pass
''',
"hints": [
    "Valid output size `(H-2, W-2)`; for each kernel entry add `K[u, v] * g[u:u+H-2, v:v+W-2]`.",
    "Apply the same helper with KX and KY.",
    "`np.hypot(gx, gy)` is the magnitude.",
],
"solution": r'''
import numpy as np

KX = np.array([[-1., 0., 1.], [-2., 0., 2.], [-1., 0., 1.]])
KY = KX.T


def _valid(g, K):
    H, W = g.shape
    out = np.zeros((H - 2, W - 2))
    for u in range(3):
        for v in range(3):
            out += K[u, v] * g[u:u + H - 2, v:v + W - 2]
    return out


def sobel(gray):
    g = np.asarray(gray, dtype=float)
    if g.ndim != 2 or g.shape[0] < 3 or g.shape[1] < 3:
        raise ValueError("image must be at least 3x3")
    gx, gy = _valid(g, KX), _valid(g, KY)
    return gx, gy, np.hypot(gx, gy)


def edges(gray, t):
    return sobel(gray)[2] > t
''',
"explanation": r'''
A valid cross-correlation helper applies each 3×3 kernel; the two gradient maps combine into a
magnitude with `hypot`. Using floats preserves negative gradients.
''',
"tests": r'''
import numpy as np

class TestSobel(unittest.TestCase):
    def test_vertical_edge(self):
        g = np.array([[0, 0, 10, 10]] * 4, float)
        gx, gy, mag = S.sobel(g)
        np.testing.assert_allclose(gx, 40)
        np.testing.assert_allclose(gy, 0)
        np.testing.assert_allclose(mag, 40)

    def test_horizontal_edge(self):
        g = np.array([[0] * 4, [0] * 4, [10] * 4, [10] * 4], float)
        gx, gy, _ = S.sobel(g)
        np.testing.assert_allclose(gx, 0)
        np.testing.assert_allclose(gy, 40)

    def test_flat(self):
        _, _, mag = S.sobel(np.full((5, 5), 7.0))
        np.testing.assert_allclose(mag, 0)

    def test_ramp(self):
        g = np.tile(np.arange(6.0), (5, 1))
        gx, _, _ = S.sobel(g)
        np.testing.assert_allclose(gx, 8.0)

    def test_shape_and_uint8(self):
        g = np.array([[0, 255, 0]] * 3, dtype=np.uint8)
        gx, _, _ = S.sobel(g)
        self.assertEqual(gx.shape, (1, 1))
        self.assertEqual(gx[0, 0], 0.0)
        g2 = np.array([[255, 0, 0]] * 3, dtype=np.uint8)
        self.assertEqual(S.sobel(g2)[0][0, 0], -1020.0)

    def test_edges(self):
        g = np.array([[0, 0, 10, 10]] * 4, float)
        np.testing.assert_array_equal(S.edges(g, 39), True)
        np.testing.assert_array_equal(S.edges(g, 40), False)

    def test_small(self):
        with self.assertRaises(ValueError):
            S.sobel(np.zeros((2, 5)))
''',
"feedback": [
    ("test_vertical_edge", "Kx = [[-1,0,1],[-2,0,2],[-1,0,1]] responds to left→right change."),
    ("test_shape_and_uint8", "Convert to float first; uint8 cannot hold negative gradients."),
    ("test_ramp", "Use valid (unpadded) cross-correlation, output (H−2, W−2)."),
    ("test_edges", "edges uses strict magnitude > t."),
],
},
# ---------------------------------------------------------------- max-pool-2d
{
"slug": "max-pool-2d", "title": "2D Max Pooling", "optional": True,
"difficulty": "intermediate", "prereqs": ["conv2d-filter"], "packages": ["numpy"],
"objectives": ["Downsample with max and average pooling", "Compute pooled output sizes",
               "Vectorise non-overlapping pooling with reshape"],
"tags": ["pooling", "downsampling", "cnn"],
"sources": ["S015", "S013"], "entry": "pool2d(x, size=2, stride=None, mode='max')",
"article": r'''
# Pooling

## Intuition
Pooling summarises each small window by its maximum (or average), shrinking feature maps while
keeping the strongest responses — a bit of translation tolerance for free.

## Precise explanation
For window size $k$ and stride $s$ (default $s = k$, non-overlapping), output size per axis is
$\lfloor (n - k)/s \rfloor + 1$ (CS231n formula with no padding). Rows/columns that don't fit a
full window are dropped.
For the non-overlapping case a reshape trick avoids loops:
```python
x[:Ho*k, :Wo*k].reshape(Ho, k, Wo, k).max(axis=(1, 3))
```
Overlapping pooling (s < k) can use `sliding_window_view` ([[moving-average]]) or a loop over output cells.

## Worked example
4×4 [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], 2×2 max → [[6, 8], [14, 16]];
average → [[3.5, 5.5], [11.5, 13.5]].

## Common mistakes
* Reshaping `(H, W)` to `(Ho, Wo, k, k)` directly — mixes rows and columns.
* Forgetting to crop to a multiple of k.
* Off-by-one in the output size with strides.

## Why this matters
Pooling layers appear in classic CNNs (LeNet, VGG) and global average pooling feeds classifier heads.
''',
"statement": r'''
Write `pool2d(x, size=2, stride=None, mode="max")` for a 2-D array: `stride` defaults to `size`;
`mode` in {"max", "avg"}. Output shape `((H-size)//stride + 1, (W-size)//stride + 1)`. Raise
`ValueError` for invalid size/stride/mode or if the window is larger than the input.

**Example**
```python
x = np.arange(1, 17).reshape(4, 4)
pool2d(x)                 # [[ 6,  8], [14, 16]]
pool2d(x, mode="avg")     # [[ 3.5,  5.5], [11.5, 13.5]]
pool2d(x, size=3, stride=1)   # [[11, 12], [15, 16]]
```
''',
"starter": r'''
import numpy as np


def pool2d(x, size=2, stride=None, mode="max"):
    pass
''',
"hints": [
    "`Ho = (H - size) // stride + 1` (same for W).",
    "General case: `sliding_window_view(x, (size, size))[::stride, ::stride]` has shape `(Ho, Wo, size, size)`.",
    "Reduce with `.max(axis=(2, 3))` or `.mean(axis=(2, 3))`.",
],
"solution": r'''
import numpy as np


def pool2d(x, size=2, stride=None, mode="max"):
    x = np.asarray(x)
    stride = size if stride is None else stride
    if size < 1 or stride < 1 or mode not in ("max", "avg"):
        raise ValueError("invalid size, stride or mode")
    H, W = x.shape
    if size > H or size > W:
        raise ValueError("window larger than input")
    win = np.lib.stride_tricks.sliding_window_view(x, (size, size))[::stride, ::stride]
    return win.max(axis=(2, 3)) if mode == "max" else win.mean(axis=(2, 3))
''',
"explanation": r'''
`sliding_window_view` exposes every window; taking every `stride`-th window along both axes gives
exactly the pooled grid, whose shape matches the output-size formula. Reducing over the last two
axes computes the max or mean of each window.
''',
"tests": r'''
import numpy as np

X = np.arange(1, 17).reshape(4, 4)

class TestPool(unittest.TestCase):
    def test_max(self):
        np.testing.assert_array_equal(S.pool2d(X), [[6, 8], [14, 16]])

    def test_avg(self):
        np.testing.assert_allclose(S.pool2d(X, mode="avg"), [[3.5, 5.5], [11.5, 13.5]])

    def test_overlap(self):
        np.testing.assert_array_equal(S.pool2d(X, size=3, stride=1), [[11, 12], [15, 16]])

    def test_crop(self):
        x = np.arange(25).reshape(5, 5)
        out = S.pool2d(x, 2)
        self.assertEqual(out.shape, (2, 2))
        np.testing.assert_array_equal(out, [[6, 8], [16, 18]])

    def test_shape_formula(self):
        x = np.zeros((10, 7))
        self.assertEqual(S.pool2d(x, 3, 2).shape, ((10 - 3) // 2 + 1, (7 - 3) // 2 + 1))

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.pool2d(X, size=5)
        with self.assertRaises(ValueError):
            S.pool2d(X, mode="min")
''',
"feedback": [
    ("test_max", "Non-overlapping 2×2 windows: stride defaults to size."),
    ("test_crop", "Drop rows/columns that don't fill a whole window."),
    ("test_overlap", "With stride < size, windows overlap; take every stride-th window."),
    ("test_errors", "Reject windows larger than the input and unknown modes."),
],
},
# ---------------------------------------------------------------- psnr
{
"slug": "psnr", "title": "MSE and PSNR by Hand", "optional": True,
"difficulty": "intermediate", "prereqs": ["image-arrays", "sklearn-estimator-api"], "packages": ["numpy"],
"objectives": ["Compute image MSE without uint8 overflow", "Compute PSNR in decibels",
               "Interpret PSNR values"],
"tags": ["image-quality", "psnr", "mse", "metrics"],
"sources": ["S023"], "entry": "mse(a, b); psnr(a, b, max_val=255.0)",
"article": r'''
# Image Quality: MSE and PSNR

## Intuition
How close is a compressed or denoised image to the original? Average the squared pixel differences
(MSE). PSNR rescales this to a logarithmic decibel scale where higher is better.

## Precise explanation
$$\text{MSE} = \frac1N\sum (a_i - b_i)^2,\qquad \text{PSNR} = 10\log_{10}\frac{\text{MAX}^2}{\text{MSE}}\ \text{dB},$$
with MAX = 255 for 8-bit images (1.0 for images scaled to [0, 1]). Identical images → MSE 0 →
PSNR = ∞. Rough guide for 8-bit images: 30–50 dB is typical for good compression; each halving of the
RMSE adds ≈ 6 dB.
**Overflow trap:** `a - b` on `uint8` arrays wraps around (3 − 5 = 254). Convert to float first.

## Worked example
a = [[0, 0]], b = [[0, 255]]: MSE = 255²/2 = 32512.5 → PSNR = 10·log10(2) ≈ 3.01 dB.

## Common mistakes
* Computing on uint8.
* Wrong MAX for float images.
* Treating PSNR as perceptual quality (SSIM and learned metrics model perception better).

## Why this matters
PSNR is the standard sanity metric for denoising, super-resolution and compression.
''',
"statement": r'''
Implement:
* `mse(a, b)` → float; raise `ValueError` if shapes differ or arrays are empty.
* `psnr(a, b, max_val=255.0)` → float dB, `math.inf` for identical images.

**Examples**
```python
mse(np.array([[0, 0]], np.uint8), np.array([[0, 255]], np.uint8))    # 32512.5
psnr(np.array([[0, 0]], np.uint8), np.array([[0, 255]], np.uint8))   # 3.0103
mse(np.array([3], np.uint8), np.array([5], np.uint8))                # 4.0 (not 254**2)
```
''',
"starter": r'''
import math

import numpy as np


def mse(a, b):
    pass


def psnr(a, b, max_val=255.0):
    pass
''',
"hints": [
    "`a = np.asarray(a, dtype=float)` before subtracting.",
    "`float(np.mean((a - b) ** 2))`.",
    "`10 * math.log10(max_val ** 2 / m)`; return `math.inf` if `m == 0`.",
],
"solution": r'''
import math

import numpy as np


def mse(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape or a.size == 0:
        raise ValueError("images must be non-empty and the same shape")
    return float(np.mean((a - b) ** 2))


def psnr(a, b, max_val=255.0):
    m = mse(a, b)
    if m == 0:
        return math.inf
    return 10 * math.log10(max_val ** 2 / m)
''',
"explanation": r'''
Converting to float before subtraction avoids uint8 wrap-around. PSNR applies the logarithmic
formula, handling the zero-error case explicitly.
''',
"tests": r'''
import numpy as np

A = np.array([[0, 0]], np.uint8); B = np.array([[0, 255]], np.uint8)

class TestPSNR(unittest.TestCase):
    def test_mse(self):
        self.assertAlmostEqual(S.mse(A, B), 32512.5)

    def test_psnr(self):
        self.assertAlmostEqual(S.psnr(A, B), 10 * math.log10(2))

    def test_overflow(self):
        self.assertEqual(S.mse(np.array([3], np.uint8), np.array([5], np.uint8)), 4.0)

    def test_identical(self):
        self.assertEqual(S.psnr(A, A), math.inf)

    def test_max_val(self):
        a = np.zeros((2, 2)); b = np.full((2, 2), 0.1)
        self.assertAlmostEqual(S.psnr(a, b, max_val=1.0), 20.0)

    def test_six_db_rule(self):
        a = np.zeros(100); p1 = S.psnr(a, np.full(100, 4.0)); p2 = S.psnr(a, np.full(100, 2.0))
        self.assertAlmostEqual(p2 - p1, 20 * math.log10(2))

    def test_shape(self):
        with self.assertRaises(ValueError):
            S.mse(np.zeros(3), np.zeros(4))
''',
"feedback": [
    ("test_overflow", "Cast to float before subtracting uint8 arrays."),
    ("test_identical", "Return math.inf when MSE is 0."),
    ("test_max_val", "PSNR = 10·log10(MAX² / MSE)."),
    ("test_shape", "Raise ValueError if shapes differ."),
],
},
# ---------------------------------------------------------------- bilinear-resize
{
"slug": "bilinear-resize", "title": "Bilinear Resize", "optional": True,
"difficulty": "advanced", "prereqs": ["flip-rotate", "fancy-indexing"], "packages": ["numpy"],
"objectives": ["Map output pixels to input coordinates with half-pixel centres",
               "Interpolate bilinearly between four neighbours", "Vectorise with fancy indexing"],
"tags": ["resizing", "interpolation", "bilinear", "image-transforms"],
"sources": ["S023", "S006"], "entry": "resize_bilinear(img, out_h, out_w)",
"article": r'''
# Bilinear Resizing

## Intuition
To enlarge an image, each new pixel must be invented from nearby old pixels. Nearest-neighbour copies
the closest pixel (blocky). Bilinear blends the four surrounding pixels, weighted by distance
(smooth).

## Precise explanation
**Coordinate mapping (half-pixel centres, the convention OpenCV's `INTER_LINEAR` uses):** for output
row $i$ with scale $s_y = H_\text{in}/H_\text{out}$:
$$y = (i + 0.5)\,s_y - 0.5,$$
clamped to $[0, H_\text{in}-1]$ (same for columns). Let $y_0 = \lfloor y\rfloor$,
$y_1 = \min(y_0+1, H_\text{in}-1)$, $w_y = y - y_0$ (and similarly $x_0, x_1, w_x$). Then
$$\text{out} = (1-w_y)(1-w_x)\,I[y_0,x_0] + (1-w_y)w_x\,I[y_0,x_1] + w_y(1-w_x)\,I[y_1,x_0] + w_y w_x\,I[y_1,x_1].$$
Vectorise by computing row and column coordinate vectors once and using fancy indexing with
`np.ix_`-style broadcasting.

## Worked example
2×2 image [[0, 10], [20, 30]] → 4×4: output (0,0) maps to y = x = −0.25 → clamped 0 → 0;
output (1,1) maps to 0.25, 0.25 → 0.75·0.75·0 + 0.75·0.25·10 + 0.25·0.75·20 + 0.25·0.25·30 = 7.5.

## Common mistakes
* Using $y = i\cdot s_y$ (shifts the image by half a pixel).
* Forgetting to clamp, indexing out of bounds.
* Integer division in scale computation.

## Why this matters
Resizing to a fixed input size is the first step of almost every vision model; inconsistent
resizing between training and deployment is a known source of accuracy loss.
''',
"statement": r'''
Write `resize_bilinear(img, out_h, out_w)` for a 2-D float image using the mapping above. Return a
float array `(out_h, out_w)`. Raise `ValueError` for non-positive sizes or non-2-D input.

**Examples**
```python
img = np.array([[0., 10.], [20., 30.]])
resize_bilinear(img, 4, 4)[1, 1]   # 7.5
resize_bilinear(img, 2, 2)         # equals img (identity size)
resize_bilinear(img, 1, 1)         # [[15.]]  (centre of the image)
```
''',
"starter": r'''
import numpy as np


def resize_bilinear(img, out_h, out_w):
    pass
''',
"hints": [
    "`y = (np.arange(out_h) + 0.5) * (H / out_h) - 0.5`, then `np.clip(y, 0, H - 1)`.",
    "`y0 = np.floor(y).astype(int)`; `y1 = np.minimum(y0 + 1, H - 1)`; `wy = (y - y0)[:, None]`.",
    "Corner values: `img[y0][:, x0]`, `img[y0][:, x1]`, `img[y1][:, x0]`, `img[y1][:, x1]`.",
],
"solution": r'''
import numpy as np


def _coords(n_out, n_in):
    c = (np.arange(n_out) + 0.5) * (n_in / n_out) - 0.5
    c = np.clip(c, 0, n_in - 1)
    c0 = np.floor(c).astype(int)
    c1 = np.minimum(c0 + 1, n_in - 1)
    return c0, c1, c - c0


def resize_bilinear(img, out_h, out_w):
    img = np.asarray(img, dtype=float)
    if img.ndim != 2 or out_h < 1 or out_w < 1:
        raise ValueError("2-D image and positive sizes required")
    H, W = img.shape
    y0, y1, wy = _coords(out_h, H)
    x0, x1, wx = _coords(out_w, W)
    wy = wy[:, None]
    wx = wx[None, :]
    top = img[y0][:, x0] * (1 - wx) + img[y0][:, x1] * wx
    bottom = img[y1][:, x0] * (1 - wx) + img[y1][:, x1] * wx
    return top * (1 - wy) + bottom * wy
''',
"explanation": r'''
Row and column source coordinates are computed once with half-pixel centres and clamped. Fancy
indexing gathers the four neighbour grids, and broadcasting the fractional weights interpolates
horizontally and then vertically.
''',
"tests": r'''
import numpy as np

IMG = np.array([[0., 10.], [20., 30.]])

class TestResize(unittest.TestCase):
    def test_point(self):
        self.assertAlmostEqual(S.resize_bilinear(IMG, 4, 4)[1, 1], 7.5)

    def test_corners_clamped(self):
        out = S.resize_bilinear(IMG, 4, 4)
        self.assertEqual((out[0, 0], out[0, 3], out[3, 0], out[3, 3]), (0.0, 10.0, 20.0, 30.0))

    def test_identity(self):
        img = np.random.default_rng(0).normal(size=(5, 7))
        np.testing.assert_allclose(S.resize_bilinear(img, 5, 7), img)

    def test_center(self):
        np.testing.assert_allclose(S.resize_bilinear(IMG, 1, 1), [[15.0]])

    def test_constant(self):
        np.testing.assert_allclose(S.resize_bilinear(np.full((3, 4), 2.5), 7, 2), 2.5)

    def test_linear_ramp_interior(self):
        img = np.tile(np.arange(8.0), (4, 1))
        out = S.resize_bilinear(img, 4, 16)
        exp = np.clip((np.arange(16) + 0.5) * 0.5 - 0.5, 0, 7)
        np.testing.assert_allclose(out[0], exp)

    def test_downscale_average(self):
        img = np.array([[0., 2.], [4., 6.]])
        np.testing.assert_allclose(S.resize_bilinear(img, 1, 2), [[2., 4.]])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.resize_bilinear(IMG, 0, 3)
''',
"feedback": [
    ("test_point", "Map with (i + 0.5)·scale − 0.5 (half-pixel centres), not i·scale."),
    ("test_corners_clamped", "Clamp source coordinates to [0, n_in − 1]."),
    ("test_identity", "With equal sizes the mapping is the identity."),
    ("test_linear_ramp_interior", "Interpolate horizontally between x0 and x1 using weight x − x0."),
],
},
# ---------------------------------------------------------------- iou
{
"slug": "iou", "title": "Intersection over Union",
"difficulty": "advanced", "prereqs": ["image-arrays", "broadcast-center"], "packages": ["numpy"],
"objectives": ["Compute box areas and intersections", "Vectorise pairwise IoU with broadcasting",
               "Handle non-overlapping and degenerate boxes"],
"tags": ["object-detection", "iou", "bounding-boxes", "broadcasting"],
"sources": ["S013"], "entry": "box_area(boxes); iou_matrix(A, B)",
"article": r'''
# Intersection over Union (IoU)

## Intuition
How well does a predicted box match the true box? Divide the overlapping area by the total area
covered by either box. 1 = perfect match, 0 = no overlap.

## Precise explanation
Boxes as `[x1, y1, x2, y2]` with $x2 > x1$, $y2 > y1$ (continuous coordinates):
* area $= (x2-x1)(y2-y1)$;
* intersection corners: $\max(x1)$, $\max(y1)$, $\min(x2)$, $\min(y2)$; width/height clipped at 0;
* $\text{IoU} = \frac{|A\cap B|}{|A| + |B| - |A\cap B|}$.
Pairwise for $A$ `(m, 4)`, $B$ `(n, 4)`: broadcast `A[:, None, :]` against `B[None, :, :]` to get
`(m, n)` matrices. Detection benchmarks count a prediction as correct if IoU ≥ 0.5 (or several
thresholds).

## Worked example
A = [0, 0, 2, 2], B = [1, 1, 3, 3]: intersection 1×1 = 1; union 4 + 4 − 1 = 7 → IoU 1/7 ≈ 0.143.

## Common mistakes
* Forgetting to clip negative widths (non-overlapping boxes give negative "intersection").
* Mixing `[x, y, w, h]` and `[x1, y1, x2, y2]` formats.
* +1 pixel conventions from integer-pixel datasets (we use continuous coordinates).

## Why this matters
IoU drives detection evaluation (mAP), anchor matching during training and non-maximum suppression
([[non-max-suppression]]).
''',
"statement": r'''
Implement:
* `box_area(boxes)` → areas of `(n, 4)` boxes; raise `ValueError` if any box has `x2 <= x1` or
  `y2 <= y1`.
* `iou_matrix(A, B)` → `(m, n)` IoU matrix (vectorised).

**Example**
```python
iou_matrix(np.array([[0, 0, 2, 2]]), np.array([[1, 1, 3, 3], [5, 5, 6, 6], [0, 0, 2, 2]]))
# [[0.142857, 0.0, 1.0]]
```
''',
"starter": r'''
import numpy as np


def box_area(boxes):
    pass


def iou_matrix(A, B):
    pass
''',
"hints": [
    "`(b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])`.",
    "`ix1 = np.maximum(A[:, None, 0], B[None, :, 0])` … `iw = np.clip(ix2 - ix1, 0, None)`.",
    "`union = areaA[:, None] + areaB[None, :] - inter`.",
],
"solution": r'''
import numpy as np


def box_area(boxes):
    b = np.asarray(boxes, dtype=float).reshape(-1, 4)
    if ((b[:, 2] <= b[:, 0]) | (b[:, 3] <= b[:, 1])).any():
        raise ValueError("boxes must satisfy x2 > x1 and y2 > y1")
    return (b[:, 2] - b[:, 0]) * (b[:, 3] - b[:, 1])


def iou_matrix(A, B):
    A = np.asarray(A, dtype=float).reshape(-1, 4)
    B = np.asarray(B, dtype=float).reshape(-1, 4)
    area_a, area_b = box_area(A), box_area(B)
    ix1 = np.maximum(A[:, None, 0], B[None, :, 0])
    iy1 = np.maximum(A[:, None, 1], B[None, :, 1])
    ix2 = np.minimum(A[:, None, 2], B[None, :, 2])
    iy2 = np.minimum(A[:, None, 3], B[None, :, 3])
    inter = np.clip(ix2 - ix1, 0, None) * np.clip(iy2 - iy1, 0, None)
    return inter / (area_a[:, None] + area_b[None, :] - inter)
''',
"explanation": r'''
Broadcasting A against B produces all pairwise intersection rectangles at once; clipping makes
non-overlapping pairs contribute zero. Union follows from inclusion–exclusion.
''',
"tests": r'''
import numpy as np

class TestIoU(unittest.TestCase):
    def test_example(self):
        np.testing.assert_allclose(
            S.iou_matrix(np.array([[0, 0, 2, 2]]), np.array([[1, 1, 3, 3], [5, 5, 6, 6], [0, 0, 2, 2]])),
            [[1 / 7, 0.0, 1.0]])

    def test_area(self):
        np.testing.assert_allclose(S.box_area(np.array([[0, 0, 2, 3], [1, 1, 1.5, 2]])), [6, 0.5])

    def test_degenerate(self):
        with self.assertRaises(ValueError):
            S.box_area(np.array([[0, 0, 0, 1]]))

    def test_contained(self):
        np.testing.assert_allclose(S.iou_matrix(np.array([[0, 0, 4, 4]]), np.array([[1, 1, 3, 3]])), [[4 / 16]])

    def test_touching(self):
        np.testing.assert_allclose(S.iou_matrix(np.array([[0, 0, 1, 1]]), np.array([[1, 0, 2, 1]])), [[0.0]])

    def test_symmetric_shape(self):
        rng = np.random.default_rng(0)
        xy = rng.uniform(0, 10, (5, 2)); wh = rng.uniform(1, 3, (5, 2))
        boxes = np.hstack([xy, xy + wh])
        M = S.iou_matrix(boxes, boxes[:3])
        self.assertEqual(M.shape, (5, 3))
        np.testing.assert_allclose(M[:3], M[:3].T)
        np.testing.assert_allclose(np.diag(M[:3]), 1.0)
''',
"feedback": [
    ("test_example", "IoU = intersection / (areaA + areaB − intersection)."),
    ("test_touching", "Clip negative intersection widths/heights to 0."),
    ("test_contained", "Use max of the top-left corners and min of the bottom-right corners."),
    ("test_degenerate", "Reject boxes with x2 <= x1 or y2 <= y1."),
],
},
# ---------------------------------------------------------------- non-max-suppression
{
"slug": "non-max-suppression", "title": "Non-Maximum Suppression",
"difficulty": "advanced", "prereqs": ["iou"], "packages": ["numpy"],
"objectives": ["Implement greedy NMS", "Apply score and IoU thresholds",
               "Return kept indices in score order"],
"tags": ["object-detection", "nms", "greedy-algorithms"],
"sources": ["S013"], "entry": "nms(boxes, scores, iou_threshold=0.5, score_threshold=0.0)",
"article": r'''
# Non-Maximum Suppression (NMS)

## Intuition
Detectors fire many overlapping boxes around the same object. NMS keeps the most confident box and
removes others that overlap it too much, then repeats — one box per object.

## Precise explanation
Greedy NMS:
1. Discard boxes with score < `score_threshold`.
2. Sort remaining boxes by score descending (ties → lower index first).
3. While candidates remain: take the first (highest score), **keep** it, and remove every remaining
   candidate whose IoU with it is **> `iou_threshold`**.
4. Return kept indices (into the original arrays) in the order they were kept.
Standard NMS is class-agnostic within one class; for multiple classes run it per class.

```mermaid
flowchart TD
  S[sort by score] --> P[pick top box, keep it] --> R[remove boxes with IoU > t]
  R --> E{any left?}
  E -- yes --> P
  E -- no --> D[return kept]
```

## Worked example
Boxes A [0,0,2,2] s 0.9, B [0.1,0,2.1,2] s 0.8 (IoU ≈ 0.90 with A), C [5,5,6,6] s 0.7 →
keep A, drop B, keep C → [0, 2].

## Common mistakes
* Comparing every box only with the global best (must compare with each kept box as you go).
* Using ≥ vs > inconsistently.
* Returning sorted indices instead of keep order.

## Why this matters
Every classic detector (YOLO, SSD, Faster R-CNN) applies NMS at inference.
''',
"statement": r'''
Write `nms(boxes, scores, iou_threshold=0.5, score_threshold=0.0)` returning a list of kept indices
(ints) following the algorithm above. Boxes are `(n, 4)` `[x1, y1, x2, y2]`. Raise `ValueError` if
`len(scores) != len(boxes)`.

**Example**
```python
boxes = np.array([[0, 0, 2, 2], [0.1, 0, 2.1, 2], [5, 5, 6, 6]])
nms(boxes, np.array([0.9, 0.8, 0.7]))   # [0, 2]
```
''',
"starter": r'''
import numpy as np


def nms(boxes, scores, iou_threshold=0.5, score_threshold=0.0):
    # TODO
    return []
''',
"hints": [
    "Order: `idx = np.argsort(-scores, kind='stable')`, then filter by score threshold.",
    "Write an `_iou(box, many)` helper (or reuse [[iou]]).",
    "Loop: `i = order[0]`; keep it; `order = order[1:][iou(boxes[i], boxes[order[1:]]) <= t]`.",
],
"solution": r'''
import numpy as np


def _iou_one(b, many):
    x1 = np.maximum(b[0], many[:, 0]); y1 = np.maximum(b[1], many[:, 1])
    x2 = np.minimum(b[2], many[:, 2]); y2 = np.minimum(b[3], many[:, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    area_m = (many[:, 2] - many[:, 0]) * (many[:, 3] - many[:, 1])
    return inter / (area_b + area_m - inter)


def nms(boxes, scores, iou_threshold=0.5, score_threshold=0.0):
    boxes = np.asarray(boxes, dtype=float).reshape(-1, 4)
    scores = np.asarray(scores, dtype=float)
    if len(scores) != len(boxes):
        raise ValueError("boxes and scores must have the same length")
    order = np.argsort(-scores, kind="stable")
    order = order[scores[order] >= score_threshold]
    keep = []
    while order.size:
        i = int(order[0])
        keep.append(i)
        rest = order[1:]
        if rest.size == 0:
            break
        order = rest[_iou_one(boxes[i], boxes[rest]) <= iou_threshold]
    return keep
''',
"explanation": r'''
Candidates are processed in descending score order. Each iteration keeps the best remaining box
and filters out the rest that overlap it beyond the threshold, so every kept box suppresses its
own duplicates.
''',
"tests": r'''
import numpy as np

B = np.array([[0, 0, 2, 2], [0.1, 0, 2.1, 2], [5, 5, 6, 6]])

class TestNMS(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.nms(B, np.array([0.9, 0.8, 0.7])), [0, 2])

    def test_order_by_score(self):
        self.assertEqual(S.nms(B, np.array([0.5, 0.95, 0.99])), [2, 1])

    def test_threshold_high_keeps_all(self):
        self.assertEqual(S.nms(B, np.array([0.9, 0.8, 0.7]), iou_threshold=0.95), [0, 1, 2])

    def test_score_threshold(self):
        self.assertEqual(S.nms(B, np.array([0.9, 0.8, 0.1]), score_threshold=0.5), [0])

    def test_chain(self):
        boxes = np.array([[0, 0, 4, 4], [2, 0, 6, 4], [4, 0, 8, 4]])
        self.assertEqual(S.nms(boxes, np.array([0.9, 0.8, 0.7]), iou_threshold=0.3), [0, 2])

    def test_empty(self):
        self.assertEqual(S.nms(np.zeros((0, 4)), np.zeros(0)), [])

    def test_ties_lower_index(self):
        self.assertEqual(S.nms(np.array([[0, 0, 2, 2], [0, 0, 2, 2]]), np.array([0.5, 0.5])), [0])

    def test_mismatch(self):
        with self.assertRaises(ValueError):
            S.nms(B, np.array([0.1]))
''',
"feedback": [
    ("test_chain", "Compare remaining boxes with each newly kept box, not only with the first box."),
    ("test_order_by_score", "Return indices in the order they were kept (descending score)."),
    ("test_score_threshold", "Drop boxes below score_threshold before suppression."),
    ("test_ties_lower_index", "Use a stable sort so equal scores keep the lower index first."),
],
},
# ---------------------------------------------------------------- connected-components
{
"slug": "connected-components", "title": "Connected Components Labeling by Hand", "optional": True,
"difficulty": "advanced", "prereqs": ["threshold-binary"], "packages": ["numpy"],
"objectives": ["Label connected foreground regions with BFS", "Compare 4- and 8-connectivity",
               "Report component sizes deterministically"],
"tags": ["segmentation", "connected-components", "bfs", "graphs"],
"sources": ["S006", "S023"], "entry": "label_components(mask, connectivity=4)",
"article": r'''
# Connected-Component Labelling

## Intuition
After thresholding ([[threshold-binary]]) you have blobs of foreground pixels. Which pixels belong to the same blob?
Treat pixels as graph nodes connected to their neighbours and find connected groups.

## Precise explanation
* **4-connectivity:** neighbours up, down, left, right. **8-connectivity:** also diagonals.
* Algorithm: scan pixels in raster order (row by row, left to right). When an unlabelled foreground
  pixel is found, start a new label and flood-fill its component with breadth-first search (BFS)
  using a queue (`collections.deque`).
* Labels 1, 2, 3, … in order of the first pixel encountered; background stays 0.
* Return also the size (pixel count) of each component.
BFS visits each pixel once: $O(HW)$. Recursion (DFS) can exceed Python's recursion limit on large
blobs, so use an explicit queue.

## Worked example
```
1 1 0 0        1 1 0 0
0 1 0 1   →    0 1 0 2      (4-connectivity: 2 components, sizes [3, 2])
0 0 0 1        0 0 0 2
```
Diagonal pixels (0,0) and (1,1) would also join under 8-connectivity.

## Common mistakes
* Marking pixels visited only when popped (duplicates in the queue).
* Index errors at the image border.
* Recursive flood fill on large images.

## Why this matters
Component labelling counts objects (cells, characters), filters small noise blobs, and is a direct
application of graph search, which reappears in agent planning ([[bfs-planner]]).
''',
"statement": r'''
Write `label_components(mask, connectivity=4)` for a 2-D boolean array returning
`(labels, sizes)`: `labels` int array (0 = background, components 1..K in raster order of their first
pixel) and `sizes` a list of K pixel counts. `connectivity` in {4, 8}, else `ValueError`.

**Example**
```python
m = np.array([[1, 1, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1]], bool)
labels, sizes = label_components(m)
labels   # [[1,1,0,0],[0,1,0,2],[0,0,0,2]]
sizes    # [3, 2]
label_components(np.array([[1, 0], [0, 1]], bool), 8)[1]   # [2]
```
''',
"starter": r'''
from collections import deque

import numpy as np


def label_components(mask, connectivity=4):
    # TODO
    pass
''',
"hints": [
    "Offsets: 4 → `[(-1,0),(1,0),(0,-1),(0,1)]`; 8 adds the four diagonals.",
    "Raster scan; when `mask[r, c] and labels[r, c] == 0`, assign a new label and BFS.",
    "Set the label when *pushing* a pixel onto the queue to avoid duplicates.",
],
"solution": r'''
from collections import deque

import numpy as np

N4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
N8 = N4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def label_components(mask, connectivity=4):
    if connectivity not in (4, 8):
        raise ValueError("connectivity must be 4 or 8")
    mask = np.asarray(mask, dtype=bool)
    H, W = mask.shape
    labels = np.zeros((H, W), dtype=int)
    offsets = N4 if connectivity == 4 else N8
    sizes = []
    for r in range(H):
        for c in range(W):
            if mask[r, c] and labels[r, c] == 0:
                lab = len(sizes) + 1
                labels[r, c] = lab
                q = deque([(r, c)])
                count = 0
                while q:
                    y, x = q.popleft()
                    count += 1
                    for dy, dx in offsets:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and labels[ny, nx] == 0:
                            labels[ny, nx] = lab
                            q.append((ny, nx))
                sizes.append(count)
    return labels, sizes
''',
"explanation": r'''
A raster scan finds the first pixel of each new component, which fixes the label order. BFS with a
deque floods the component, labelling pixels as they are enqueued so none is visited twice, and
counts its size.
''',
"tests": r'''
import numpy as np

M = np.array([[1, 1, 0, 0], [0, 1, 0, 1], [0, 0, 0, 1]], bool)

class TestCC(unittest.TestCase):
    def test_example(self):
        labels, sizes = S.label_components(M)
        np.testing.assert_array_equal(labels, [[1, 1, 0, 0], [0, 1, 0, 2], [0, 0, 0, 2]])
        self.assertEqual(sizes, [3, 2])

    def test_diagonal(self):
        d = np.array([[1, 0], [0, 1]], bool)
        self.assertEqual(S.label_components(d, 4)[1], [1, 1])
        self.assertEqual(S.label_components(d, 8)[1], [2])

    def test_empty(self):
        labels, sizes = S.label_components(np.zeros((3, 3), bool))
        self.assertEqual(sizes, [])
        self.assertEqual(labels.sum(), 0)

    def test_full(self):
        labels, sizes = S.label_components(np.ones((4, 5), bool))
        self.assertEqual(sizes, [20])
        self.assertTrue((labels == 1).all())

    def test_raster_order(self):
        m = np.array([[0, 0, 1], [1, 0, 0]], bool)
        np.testing.assert_array_equal(S.label_components(m)[0], [[0, 0, 1], [2, 0, 0]])

    def test_large_no_recursion(self):
        m = np.ones((200, 200), bool)
        self.assertEqual(S.label_components(m)[1], [40000])

    def test_spiral(self):
        m = np.array([[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0]], bool)
        self.assertEqual(S.label_components(m)[1], [8])

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.label_components(M, 6)
''',
"feedback": [
    ("test_diagonal", "8-connectivity includes diagonal neighbours; 4 does not."),
    ("test_raster_order", "Assign labels in order of first pixel in a row-by-row scan."),
    ("test_large_no_recursion", "Use an explicit queue (deque) instead of recursion."),
    ("test_example", "Label pixels when pushing them so each is counted once."),
],
},
]
