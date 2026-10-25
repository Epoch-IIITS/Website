# Numerical Derivatives

## Learning outcomes

After this lesson you can:

- Approximate derivatives with finite differences
- Compare forward and central differences
- Understand the role of the step size h

## Intuition
The derivative $f'(x)$ is the slope of the tangent line at $x$. We cannot draw a tangent with a
computer, but we can draw a **secant** through two nearby points and use its slope. The closer
the points, the better the approximation — up to the limits of floating-point arithmetic.

## Precise explanation
Definition: $f'(x) = \lim_{h\to 0} \frac{f(x+h) - f(x)}{h}$.
* **Forward difference:** $\frac{f(x+h)-f(x)}{h}$, error proportional to $h$ (first order).
* **Central difference:** $\frac{f(x+h)-f(x-h)}{2h}$, error proportional to $h^2$
  (second order), because the $f''$ terms in the Taylor expansions cancel.

Too-small $h$ causes **cancellation error**: $f(x+h)$ and $f(x-h)$ agree in most digits, so
their difference keeps few significant digits. With 64-bit floats, $h \approx 10^{-5}$ is a good
default for central differences.

<svg xmlns="http://www.w3.org/2000/svg" width="300" height="190" viewBox="0 0 300 190" role="img" aria-label="Curve with a tangent line at x and a secant line through x minus h and x plus h">
<title>Secant vs tangent</title>
<path d="M 20 170 Q 150 -40 280 120" fill="none" stroke="#333" stroke-width="2"/>
<line x1="60" y1="125" x2="250" y2="45" stroke="#2ca02c" stroke-width="2" stroke-dasharray="6 4"/>
<line x1="40" y1="128" x2="260" y2="52" stroke="#d62728" stroke-width="2"/>
<circle cx="110" cy="85" r="4" fill="#1f77b4"/><circle cx="205" cy="60" r="4" fill="#1f77b4"/>
<text x="95" y="105" font-size="12">x−h</text><text x="200" y="80" font-size="12">x+h</text>
<text x="220" y="40" font-size="12" fill="#2ca02c">secant</text><text x="235" y="70" font-size="12" fill="#d62728">tangent</text>
</svg>

*Figure (original): the central-difference secant through x−h and x+h is nearly parallel to the
tangent at x.*

## Worked example
$f(x) = x^3$ at $x=2$ (exact $f'(2)=12$), $h = 0.1$:
forward: $(2.1^3 - 8)/0.1 = 12.61$; central: $(2.1^3 - 1.9^3)/0.2 = 12.01$.

## Common mistakes
* Using $h = 10^{-15}$ "for accuracy" — rounding error dominates.
* Dividing the central difference by $h$ instead of $2h$.
* Expecting an exact match with the analytic derivative; always compare with a tolerance.

## Why this matters
Finite differences check that hand-written gradients are correct (DL-13) and power the numerical
gradient (MA-14) and integrated-gradients approximations (XA-14).

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
