"""Computer Vision steps added in the 2026-10 revision: images as arrays (dtypes, ranges,
channels) and a multi-channel convolution layer."""

PROBLEMS = [
# ---------------------------------------------------------------- image-arrays
{
"slug": "image-arrays", "title": "Images as Arrays",
"difficulty": "beginner", "prereqs": ["torch-conv1d"], "packages": ["numpy"],
"objectives": ["Describe an image as an (H, W) or (H, W, C) array and index pixels by (row, column)",
               "Avoid uint8 overflow when changing brightness and contrast",
               "Convert between uint8 [0, 255] and float [0, 1]",
               "Convert between channels-last (H, W, C) and channels-first (C, H, W)"],
"tags": ["images", "uint8", "dtype", "channels", "normalisation"],
"sources": ["S023", "S007"], "entry": "image_info(img); adjust(img, brightness=0, contrast=1.0); to_float(img); to_uint8(x); channels_first(img); channels_last(x)",
"article": r'''
# Images as Arrays

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
([[conv2d-layer]]) expects channels-first float input.
''',
"statement": r'''
Implement:

1. `image_info(img)` → dict with `height`, `width`, `channels` (1 for a 2-D image) and `dtype`
   (as a string, e.g. `"uint8"`).
2. `adjust(img, brightness=0, contrast=1.0)` → `uint8` image computed in float as
   `(img - 128) * contrast + 128 + brightness`, rounded with `np.rint`, then clipped to [0, 255].
3. `to_float(img)` → `float64` array in [0, 1] (divide by 255).
4. `to_uint8(x)` → inverse of `to_float`: multiply by 255, round, clip, convert.
5. `channels_first(img)` (H, W, C) → (C, H, W) and `channels_last(x)` (C, H, W) → (H, W, C);
   raise `ValueError` if the input is not 3-D.
''',
"starter": r'''
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
''',
"hints": [
    "`channels = img.shape[2] if img.ndim == 3 else 1`; `str(img.dtype)` gives the dtype name.",
    "`out = (img.astype(float) - 128) * contrast + 128 + brightness`, then `np.clip(np.rint(out), 0, 255).astype(np.uint8)`.",
    "`np.transpose(img, (2, 0, 1))` and `np.transpose(x, (1, 2, 0))`.",
],
"solution": r'''
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
''',
"explanation": r'''
All arithmetic happens in float so nothing wraps around; one helper rounds, clips and converts
back to `uint8`. Normalisation is a division by 255 and its inverse a multiplication.
Transposing the axes moves the channel dimension without copying pixel values.
''',
"tests": r'''
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
''',
"feedback": [
    ("test_brightness_no_wraparound", "Convert to float before adding, then clip to [0, 255]."),
    ("test_contrast", "Scale around 128: `(img - 128) * contrast + 128`, round with np.rint, clip."),
    ("test_float_round_trip", "Divide by 255 for floats; multiply by 255 and round to go back."),
    ("test_to_uint8_rounds_and_clips", "Round with `np.rint` before converting; don't truncate."),
    ("test_channels", "Use `np.transpose` with axes (2, 0, 1) and (1, 2, 0)."),
],
"library": {
"text": r'''
Image libraries provide these conversions: Pillow's `ImageEnhance.Brightness`, OpenCV's
`cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)` (which also saturates instead of
wrapping), and torchvision's `transforms.ToTensor()` (uint8 `(H, W, C)` → float `(C, H, W)` in
[0, 1]). None of these are needed here; NumPy's `np.clip` gives the same saturating behaviour.
When PyTorch is installed, the test checks that your channels-first float conversion matches
`torch.from_numpy(...).permute(2, 0, 1) / 255`.
''',
"optional": ["torch"],
"tests": r'''
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
''',
},
},
# ---------------------------------------------------------------- conv2d-layer
{
"slug": "conv2d-layer", "title": "A Convolution Layer with Channels",
"difficulty": "intermediate", "prereqs": ["cv-pooling-torch", "conv2d-filter"], "packages": ["numpy"],
"objectives": ["Apply a bank of filters to a multi-channel input (C_in → C_out)",
               "Compute output sizes from kernel size, padding and stride",
               "Count a convolution layer's parameters",
               "Compare a loop implementation with PyTorch's conv2d"],
"tags": ["cnn", "convolution", "channels", "padding", "stride"],
"sources": ["S015", "S013", "S093"], "entry": "conv_output_size(n, k, padding, stride); conv2d(x, weight, bias, stride=1, padding=0); conv_params(c_in, c_out, k)",
"article": r'''
# A Convolution Layer with Channels

## Intuition
[[conv2d-filter]] slid one kernel over one greyscale image. A CNN layer does this with *many*
kernels over *many* input channels: each output channel has its own small 3-D filter that looks
at every input channel at once and sums the results. Early layers learn edge and colour
detectors; later layers combine them.

## Precise explanation
Shapes (channels-first, as in PyTorch, see [[image-arrays]]):
* input `x`: `(C_in, H, W)`; weights: `(C_out, C_in, k, k)`; bias: `(C_out,)`;
* output: `(C_out, H_out, W_out)` with
  $$H_{out} = \left\lfloor \frac{H + 2p - k}{s} \right\rfloor + 1$$
  for padding $p$ (zeros added on each side) and stride $s$ (same for $W$).

$$\text{out}[o, i, j] = b_o + \sum_{c=0}^{C_{in}-1}\sum_{u=0}^{k-1}\sum_{v=0}^{k-1}
  w[o, c, u, v]\; x_p[c,\; i s + u,\; j s + v]$$
where $x_p$ is the zero-padded input. This is **cross-correlation** (the kernel is not flipped),
which is what deep-learning libraries call convolution.

* Parameters: $C_{out}\,(C_{in} k^2 + 1)$ — independent of the image size, unlike a dense layer.
* A 1×1 convolution mixes channels without looking at neighbours.

## Worked example
Input `(2, 4, 4)`, 3 filters of size 3, padding 1, stride 2: $H_{out} = \lfloor (4 + 2 - 3)/2\rfloor + 1 = 2$,
so the output is `(3, 2, 2)`; the layer has $3(2\cdot 9 + 1) = 57$ parameters.

## Common mistakes
* Summing only over the kernel window and forgetting to sum over input channels.
* Using `H - k + 1` when there is padding or stride.
* Flipping the kernel (that is mathematical convolution; CNN layers do not flip).
* Mixing up `(C_out, C_in, k, k)` order.

## Why this matters
Stacks of convolution, ReLU and pooling ([[max-pool-2d]]) form the CNNs used for image
classification and detection.
''',
"statement": r'''
Implement with NumPy:

1. `conv_output_size(n, k, padding=0, stride=1)` → output length; raise `ValueError` if it would
   be less than 1.
2. `conv2d(x, weight, bias=None, stride=1, padding=0)` for `x` of shape `(C_in, H, W)` and
   `weight` of shape `(C_out, C_in, k, k)` (square kernels) → `(C_out, H_out, W_out)` using the
   formula above (zero padding, no kernel flip). `bias` defaults to zeros. Raise `ValueError` if
   the channel counts disagree.
3. `conv_params(c_in, c_out, k)` → number of weights plus biases.
''',
"starter": r'''
import numpy as np


def conv_output_size(n, k, padding=0, stride=1):
    # TODO
    return n - k + 1


def conv2d(x, weight, bias=None, stride=1, padding=0):
    x = np.asarray(x, dtype=float)
    weight = np.asarray(weight, dtype=float)
    # TODO: pad, then loop over output channels and positions
    return np.zeros((weight.shape[0], 1, 1))


def conv_params(c_in, c_out, k):
    # TODO
    return 0
''',
"hints": [
    "`(n + 2 * padding - k) // stride + 1`.",
    "`xp = np.pad(x, ((0, 0), (padding, padding), (padding, padding)))` pads only the spatial axes.",
    "For each output position, take `patch = xp[:, i*s:i*s+k, j*s:j*s+k]` (shape (C_in, k, k)) and compute `np.sum(weight[o] * patch) + bias[o]`.",
],
"solution": r'''
import numpy as np


def conv_output_size(n, k, padding=0, stride=1):
    out = (n + 2 * padding - k) // stride + 1
    if out < 1:
        raise ValueError("kernel larger than padded input")
    return out


def conv2d(x, weight, bias=None, stride=1, padding=0):
    x = np.asarray(x, dtype=float)
    weight = np.asarray(weight, dtype=float)
    c_out, c_in, k, _ = weight.shape
    if x.shape[0] != c_in:
        raise ValueError("input channels do not match the weights")
    bias = np.zeros(c_out) if bias is None else np.asarray(bias, dtype=float)
    h_out = conv_output_size(x.shape[1], k, padding, stride)
    w_out = conv_output_size(x.shape[2], k, padding, stride)
    xp = np.pad(x, ((0, 0), (padding, padding), (padding, padding)))
    out = np.zeros((c_out, h_out, w_out))
    for i in range(h_out):
        for j in range(w_out):
            patch = xp[:, i * stride:i * stride + k, j * stride:j * stride + k]
            out[:, i, j] = np.tensordot(weight, patch, axes=([1, 2, 3], [0, 1, 2])) + bias
    return out


def conv_params(c_in, c_out, k):
    return c_out * (c_in * k * k + 1)
''',
"explanation": r'''
Padding is applied once to the spatial axes. For each output position the input patch has shape
`(C_in, k, k)`; contracting it with all filters at once (`tensordot` over the channel and kernel
axes) yields one value per output channel, to which the bias is added. The output size follows
the floor formula, which also rejects impossible configurations.
''',
"tests": r'''
import numpy as np


def reference(x, w, b, s, p):
    c_out, c_in, k, _ = w.shape
    xp = np.pad(x, ((0, 0), (p, p), (p, p)))
    ho = (x.shape[1] + 2 * p - k) // s + 1
    wo = (x.shape[2] + 2 * p - k) // s + 1
    out = np.zeros((c_out, ho, wo))
    for o in range(c_out):
        for i in range(ho):
            for j in range(wo):
                total = b[o]
                for c in range(c_in):
                    for u in range(k):
                        for v in range(k):
                            total += w[o, c, u, v] * xp[c, i * s + u, j * s + v]
                out[o, i, j] = total
    return out


class TestConv2dLayer(unittest.TestCase):
    def test_output_size(self):
        self.assertEqual(S.conv_output_size(4, 3, 1, 2), 2)
        self.assertEqual(S.conv_output_size(28, 5), 24)
        self.assertEqual(S.conv_output_size(7, 3, 1, 1), 7)
        with self.assertRaises(ValueError):
            S.conv_output_size(2, 5)

    def test_single_channel_matches_filter(self):
        x = np.arange(16.0).reshape(1, 4, 4)
        w = np.ones((1, 1, 3, 3))
        out = S.conv2d(x, w)
        self.assertEqual(out.shape, (1, 2, 2))
        self.assertEqual(out[0, 0, 0], x[0, :3, :3].sum())

    def test_sums_over_channels(self):
        x = np.stack([np.ones((3, 3)), 2 * np.ones((3, 3))])
        w = np.ones((1, 2, 3, 3))
        self.assertEqual(S.conv2d(x, w)[0, 0, 0], 9 + 18)

    def test_matches_reference(self):
        rng = np.random.default_rng(0)
        x = rng.normal(size=(2, 5, 6))
        w = rng.normal(size=(3, 2, 3, 3))
        b = rng.normal(size=3)
        for s, p in [(1, 0), (2, 1), (1, 2)]:
            np.testing.assert_allclose(S.conv2d(x, w, b, stride=s, padding=p), reference(x, w, b, s, p), atol=1e-12)

    def test_no_flip(self):
        x = np.zeros((1, 3, 3)); x[0, 0, 0] = 1.0
        w = np.zeros((1, 1, 3, 3)); w[0, 0, 0, 0] = 5.0
        self.assertEqual(S.conv2d(x, w)[0, 0, 0], 5.0)

    def test_channel_mismatch(self):
        with self.assertRaises(ValueError):
            S.conv2d(np.zeros((3, 4, 4)), np.zeros((2, 1, 3, 3)))

    def test_params(self):
        self.assertEqual(S.conv_params(2, 3, 3), 57)
        self.assertEqual(S.conv_params(3, 16, 5), 16 * 76)
''',
"feedback": [
    ("test_output_size", "Use `(n + 2*padding - k) // stride + 1` and reject results below 1."),
    ("test_sums_over_channels", "Each output value sums over all input channels as well as the kernel window."),
    ("test_matches_reference", "Pad only the spatial axes and step the window by `stride`."),
    ("test_no_flip", "Do not flip the kernel; weight[u, v] multiplies the input at offset (u, v)."),
    ("test_params", "Each output channel has C_in*k*k weights plus one bias."),
],
"library": {
"text": r'''
`torch.nn.functional.conv2d(x, weight, bias, stride, padding)` (or the layer `torch.nn.Conv2d`)
computes exactly this, batched over a leading `N` axis and using fast algorithms instead of
loops. SciPy's `scipy.signal.correlate` handles a single channel. The tests compare your
function with PyTorch when it is installed.
''',
"optional": ["torch"],
"tests": r'''
try:
    import torch
    import torch.nn.functional as F
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_matches_torch_conv2d(self):
        rng = np.random.default_rng(1)
        x = rng.normal(size=(3, 7, 7))
        w = rng.normal(size=(4, 3, 3, 3))
        b = rng.normal(size=4)
        theirs = F.conv2d(torch.tensor(x)[None], torch.tensor(w), torch.tensor(b), stride=2, padding=1)[0].numpy()
        np.testing.assert_allclose(S.conv2d(x, w, b, stride=2, padding=1), theirs, atol=1e-10)
''',
},
},
]
