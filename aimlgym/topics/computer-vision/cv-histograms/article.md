# Histograms and Equalisation

## Learning outcomes

After this lesson you can:

- Compute intensity histograms with cv2.calcHist
- Improve contrast with cv2.equalizeHist
- Explain equalisation as mapping intensities through the cumulative histogram

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
`calcHist` with 256 bins is `np.bincount` — your CV-09 (the optional deep dive
after this step). `equalizeHist` builds the cumulative histogram and applies it as a lookup table.

## Common mistakes
* Using `ranges=[0, 255]`, which drops the value 255.
* Equalising B, G and R separately and shifting colours.
* Expecting `calcHist` to return integers (it returns float32).

## Why this matters
Histograms drive Otsu thresholding, exposure correction and simple image-similarity features;
equalisation is a standard preprocessing step for low-light and medical images.

## References

- [Histogram Equalization (OpenCV 4.13)](https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html) — OpenCV team (`S118`)
- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
