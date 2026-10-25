# The Sigmoid Function

## Learning outcomes

After this lesson you can:

- Compute σ(x) = 1 / (1 + e^(−x)) without overflow
- Use the derivative σ'(x) = σ(x)(1 − σ(x))
- Invert the sigmoid with the logit function

## Intuition
The sigmoid squashes any real number into the interval (0, 1): very negative inputs give values
near 0, very positive inputs give values near 1, and 0 gives exactly 0.5. That makes it a
natural way to turn a score into a probability.

## Precise explanation
$$\sigma(x) = \frac{1}{1 + e^{-x}}, \qquad \sigma(-x) = 1 - \sigma(x), \qquad
  \sigma'(x) = \sigma(x)\,(1 - \sigma(x)).$$
* The derivative is largest at $x = 0$ ($0.25$) and nearly 0 for large $|x|$ — the reason deep
  sigmoid networks learn slowly ("vanishing gradients").
* **Inverse (logit)**: $\operatorname{logit}(p) = \ln\dfrac{p}{1-p}$ for $0 < p < 1$, and
  $\sigma(\operatorname{logit}(p)) = p$.
* **Overflow**: Python's `math.exp(1000)` raises `OverflowError`. For $x < 0$ compute
  $\sigma(x) = \dfrac{e^{x}}{1 + e^{x}}$ instead (multiply top and bottom by $e^x$); then the
  exponent is always $\le 0$ and nothing overflows.

## Worked example
$\sigma(0) = 1/2$; $\sigma(2) = 1/(1 + e^{-2}) \approx 0.8808$; $\sigma(-2) \approx 0.1192 = 1 - 0.8808$;
$\sigma'(0) = 0.5 \cdot 0.5 = 0.25$; $\operatorname{logit}(0.8808) \approx 2$.

## Common mistakes
* Writing `1 / 1 + math.exp(-x)` — precedence makes it $1 + e^{-x}$.
* Using the one-line formula for $x = -1000$ and crashing with `OverflowError`.
* Calling `logit(0)` or `logit(1)`, which are infinite.

## Why this matters
Logistic regression (ML-11) predicts $\sigma(w\cdot x + b)$, the derivative
formula gives its gradient, and neural-network activations (DL-01) start here.

## Library implementation

SciPy implements both functions as `scipy.special.expit` (the sigmoid) and
`scipy.special.logit`, vectorised over NumPy arrays and stable for large inputs. In NumPy code
later on (DL-01) you will write the same branch with `np.where`. The comparison
below runs only when SciPy is installed.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)
