# Moving Averages

## Learning outcomes

After this lesson you can:

- Compute sliding-window means in O(n) with cumulative sums
- Relate moving averages to convolution
- Build sliding windows with sliding_window_view

## Intuition
A moving average smooths a noisy signal by replacing each point with the mean of the last *w*
points. Recomputing every window from scratch costs $O(nw)$; with a running total you add the
new value and subtract the one that left — $O(n)$.

## Precise explanation
Let $c_k = \sum_{i<k} x_i$ (with $c_0 = 0$). Then the sum of window $x_j..x_{j+w-1}$ is
$c_{j+w} - c_j$:
```python
c = np.concatenate([[0.0], np.cumsum(x)])
ma = (c[w:] - c[:-w]) / w          # length n - w + 1 ("valid" windows)
```
This equals `np.convolve(x, np.ones(w)/w, mode="valid")`: a moving average is convolution with a
box kernel — the 1-D version of image blurring (CV-10).

`np.lib.stride_tricks.sliding_window_view(x, w)` returns an `(n-w+1, w)` **read-only view** of all
windows (no copy), handy for other window statistics (max, median).

## Worked example
x = [1, 2, 3, 4, 5], w = 2 → c = [0, 1, 3, 6, 10, 15] → sums [3, 5, 7, 9] → means
[1.5, 2.5, 3.5, 4.5].

## Common mistakes
* Forgetting the leading 0 in the cumulative sum (first window wrong).
* Returning length n with partial windows when "valid" was asked.
* Cumsum on huge float series accumulates rounding error (fine at this scale).

## Why this matters
Rolling features in pandas (PD-16), smoothing training-loss curves, and 1-D convolutions in
neural networks (DL-25) share this structure.

## Library implementation

`np.convolve(x, np.ones(w) / w, mode="valid")` computes the same moving average as a
convolution, and pandas offers `Series.rolling(w).mean()` (PD-16). The cumulative-sum
trick costs O(n) regardless of `w`.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
