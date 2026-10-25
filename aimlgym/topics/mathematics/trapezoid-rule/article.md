# Area Under a Curve with Trapezoids

## Learning outcomes

After this lesson you can:

- Approximate a definite integral
- Implement the composite trapezoidal rule
- Observe error shrinking as n grows

## Intuition
To estimate the area under a curve, slice it into thin vertical strips and approximate each
strip by a trapezoid (straight top). More strips → better fit.

## Precise explanation
Split $[a, b]$ into $n$ equal pieces of width $h = (b-a)/n$ with points $x_i = a + ih$.
$$\int_a^b f(x)\,dx \approx h\left[\tfrac12 f(x_0) + f(x_1) + \dots + f(x_{n-1}) + \tfrac12 f(x_n)\right].$$
The ends get weight ½ because each interior point is shared by two trapezoids.
The error shrinks roughly like $h^2$: doubling $n$ cuts the error by about 4.
The rule is exact for straight lines. If $a > b$, the formula naturally gives a negative value,
matching $\int_a^b = -\int_b^a$.

<svg xmlns="http://www.w3.org/2000/svg" width="300" height="170" viewBox="0 0 300 170" role="img" aria-label="A curve over four trapezoids whose tops are straight chords of the curve">
<title>Composite trapezoidal rule with n = 4</title>
<line x1="20" y1="150" x2="290" y2="150" stroke="#999"/>
<polygon points="40,150 40,110 100,70 100,150" fill="#aec7e8" stroke="#1f77b4"/>
<polygon points="100,150 100,70 160,50 160,150" fill="#aec7e8" stroke="#1f77b4"/>
<polygon points="160,150 160,50 220,60 220,150" fill="#aec7e8" stroke="#1f77b4"/>
<polygon points="220,150 220,60 280,100 280,150" fill="#aec7e8" stroke="#1f77b4"/>
<path d="M 40 110 C 80 60, 140 35, 180 48 S 260 75, 280 100" fill="none" stroke="#d62728" stroke-width="2"/>
<text x="35" y="165" font-size="12">a</text><text x="276" y="165" font-size="12">b</text>
</svg>

*Figure (original): four trapezoids approximating the area under the red curve.*

## Worked example
$\int_0^1 x^2 dx = 1/3$. With $n=2$, $h=0.5$: $0.5[\tfrac12\cdot0 + 0.25 + \tfrac12\cdot1] = 0.375$.
With $n = 4$: $0.34375$. Errors 0.0417 → 0.0104 (≈4× smaller).

## Common mistakes
* Giving the endpoints weight 1.
* Using `range(n)` and missing $x_n = b$.
* Computing $x_i$ by repeated addition (`x += h`) — rounding drift; use `a + i*h`.

## Why this matters
Numerical integration computes probabilities from densities, areas under ROC curves, and the path
integral in integrated gradients (XA-14).

## Library implementation

NumPy implements the same rule for sampled data as `np.trapezoid(y, x)` (named `np.trapz` before
NumPy 2.0), and SciPy offers more accurate methods such as `scipy.integrate.quad`. You will meet
NumPy in NP-01; the comparison below evaluates your function and NumPy's on the same grid.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
