# Histograms

## Learning outcomes

After this lesson you can:

- Compute equal-width bin edges
- Assign values to bins including the right edge
- Handle values outside the range

## Intuition
A histogram groups numbers into bins (intervals) and counts how many fall in each — a quick
picture of a distribution's shape: where it peaks, how wide it is, whether it is skewed.

## Precise explanation
With range $[\text{lo}, \text{hi}]$ and $k$ bins, width $w = (\text{hi}-\text{lo})/k$ and edges
$e_j = \text{lo} + j w$ for $j = 0..k$. Bin $j$ is the half-open interval $[e_j, e_{j+1})$,
**except the last bin, which is closed** $[e_{k-1}, e_k]$ so the maximum value is counted.
This is the same convention NumPy's `np.histogram` uses.

Index of value $x$: $j = \lfloor (x - \text{lo})/w \rfloor$, then clamp $j = k$ to $k-1$.
Values below lo or above hi are ignored.

If lo/hi are not given, use the data's min and max. If they are equal, the width is zero; a
common convention (used here) is to widen the range to $[\text{lo}-0.5, \text{hi}+0.5]$.

<svg xmlns="http://www.w3.org/2000/svg" width="280" height="150" viewBox="0 0 280 150" role="img" aria-label="Histogram with four bins of heights 2, 5, 3 and 1">
<title>Four-bin histogram</title>
<line x1="20" y1="130" x2="270" y2="130" stroke="#333"/>
<rect x="30" y="90" width="55" height="40" fill="#9ecae1" stroke="#3182bd"/>
<rect x="90" y="30" width="55" height="100" fill="#9ecae1" stroke="#3182bd"/>
<rect x="150" y="70" width="55" height="60" fill="#9ecae1" stroke="#3182bd"/>
<rect x="210" y="110" width="55" height="20" fill="#9ecae1" stroke="#3182bd"/>
<text x="52" y="85" font-size="12">2</text><text x="112" y="25" font-size="12">5</text><text x="172" y="65" font-size="12">3</text><text x="232" y="105" font-size="12">1</text>
</svg>

*Figure (original): counts per bin; the last bin includes its right edge.*

## Worked example
data `[1, 2, 2, 3, 4, 5]`, 2 bins over [1, 5]: width 2, edges [1, 3, 5].
Bin 0 = [1, 3): 1, 2, 2 → 3. Bin 1 = [3, 5]: 3, 4, 5 → 3.

## Common mistakes
* Dropping the maximum value because every bin is half-open.
* Floating-point edges such as 0.1 + 0.2; compute edges as `lo + j*w`.
* Too few/too many bins hiding the shape.

## Why this matters
Histograms are the first look at any feature, the basis of intensity histograms in images
(CV-09), and the binning used in calibration plots.

## Library implementation

`np.histogram(data, bins=k, range=(lo, hi))` uses the same rule: equal-width bins, each
half-open `[a, b)` except the last, which also includes `hi`; when `lo == hi` it widens the range
by 0.5 on each side, exactly as this exercise specifies. It returns `(counts, edges)` — the
opposite order to your function.

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
