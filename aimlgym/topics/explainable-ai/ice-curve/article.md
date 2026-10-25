# Individual Conditional Expectation (ICE)

## Learning outcomes

After this lesson you can:

- Vary one feature of one instance over a grid
- Query a black-box model in batch
- Read local effects from an ICE curve

## Intuition
"What would the model predict for *this* person if only their age changed?" Keep everything else
fixed, sweep one feature over a range, and plot the prediction. That curve is an ICE curve.

## Precise explanation
For a model `predict(X) -> (n,)`, an instance $x$, feature $j$ and grid values $g_1..g_m$:
build $m$ copies of $x$, set column $j$ to $g_k$ in copy $k$, and predict all copies in **one batch**.
Black-box: only predictions are needed, not model internals (**model-agnostic**). Caveat: if
features are correlated, some grid points create unrealistic inputs (e.g. 5 rooms in a 20 m² flat).

<svg xmlns="http://www.w3.org/2000/svg" width="260" height="150" viewBox="0 0 260 150" role="img" aria-label="Three ICE curves for three instances, one rising, one flat and one rising then falling">
<title>ICE curves</title>
<line x1="25" y1="130" x2="250" y2="130" stroke="#999"/><line x1="25" y1="130" x2="25" y2="10" stroke="#999"/>
<polyline points="30,110 80,95 130,70 180,50 230,30" fill="none" stroke="#1f77b4" stroke-width="2"/>
<polyline points="30,80 80,80 130,79 180,80 230,80" fill="none" stroke="#2ca02c" stroke-width="2"/>
<polyline points="30,120 80,90 130,60 180,85 230,110" fill="none" stroke="#d62728" stroke-width="2"/>
<text x="120" y="146" font-size="11">feature value</text>
</svg>

*Figure (original): each line is one instance; different shapes reveal interactions that an average
(PDP, XA-06) would hide.*

## Worked example
predict(X) = X[:,0]·X[:,1]; x = [2, 3]; vary feature 0 over [0, 1, 2] → [0, 3, 6]
(slope = 3 = this instance's x₁ value).

## Common mistakes
* Modifying the original instance in place.
* Calling the model once per grid point in a Python loop (slow for real models).
* Interpreting ICE as causal effects in the real world.

## Why this matters
ICE curves are the building block of partial dependence (XA-06) and a practical "what-if" tool.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
