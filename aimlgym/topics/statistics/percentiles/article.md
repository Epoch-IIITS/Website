# Percentiles and the IQR

## Learning outcomes

After this lesson you can:

- Compute percentiles with linear interpolation
- Compute the IQR
- Apply Tukey's fences for outliers

## Intuition
The 90th percentile is the value below which 90% of the data falls. Percentiles describe a
distribution without assuming it is bell-shaped, and they are robust to outliers.

## Precise explanation
There are several percentile definitions. We use **linear interpolation between order
statistics** (NumPy's default `method="linear"`): with sorted data $s_0..s_{n-1}$,
$$r = \frac{q}{100}(n-1),\quad i = \lfloor r\rfloor,\quad f = r - i,\quad
P_q = s_i + f\,(s_{i+1} - s_i)$$
(when $i = n-1$ just return $s_{n-1}$). $P_{50}$ is the median.

**IQR** = $P_{75} - P_{25}$, the width of the middle half.
**Tukey's fences:** values below $P_{25} - k\cdot\text{IQR}$ or above $P_{75} + k\cdot\text{IQR}$
($k = 1.5$) are flagged — the rule behind box-plot whiskers.

## Worked example
data [1, 2, 3, 4, 10]: $P_{25}$: r = 1 → 2; $P_{75}$: r = 3 → 4; IQR = 2; fences
[2 − 3, 4 + 3] = [−1, 7] → 10 is an outlier. $P_{40}$: r = 1.6 → 2 + 0.6·1 = 2.6.

## Common mistakes
* Using $q/100 \cdot n$ instead of $(n-1)$ (that is a different definition).
* Forgetting to sort.
* Comparing percentiles computed by different definitions across tools.

## Why this matters
Robust scaling, latency SLOs ("p99 < 200 ms"), box plots and clipping extreme gradient values all
use percentiles.

## Library implementation

Linear interpolation between order statistics is NumPy's default
(`np.percentile(data, q)`, method `"linear"`) and the `"inclusive"` method of
`statistics.quantiles(data, n=4, method="inclusive")`, which returns the three quartiles at once.
Other methods (such as the default `"exclusive"`) give slightly different answers for small
samples — always check which definition a library uses.

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
