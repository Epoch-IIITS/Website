# Intensity Histograms and Equalisation

## Learning outcomes

After this lesson you can:

- Count pixel intensities with np.bincount
- Compute a cumulative distribution
- Apply histogram equalisation

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

## References

- [OpenCV Tutorials (OpenCV 4.13.0)](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html) — OpenCV team (`S023`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
