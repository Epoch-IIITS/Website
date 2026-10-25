# The Dot Product

## Learning outcomes

After this lesson you can:

- Compute a dot product
- Validate equal lengths
- Interpret the sign of a dot product geometrically

## Intuition
The dot product measures how much two vectors point in the same direction. Large and positive:
they agree; zero: perpendicular; negative: they point away from each other. A linear model's
prediction $w \cdot x$ is exactly "how well does the input agree with the weights".

## Precise explanation
For $u, v \in \mathbb{R}^n$:
$$u \cdot v = \sum_{i=1}^{n} u_i v_i.$$
Geometrically $u \cdot v = \lVert u\rVert\,\lVert v\rVert \cos\theta$, where $\theta$ is the
angle between them. It is only defined when both vectors have the same length $n$.

Properties: symmetric ($u\cdot v = v\cdot u$), linear in each argument, and
$u \cdot u = \lVert u\rVert^2 \ge 0$.

```python
total = 0
for a, b in zip(u, v):
    total += a * b
```

## Worked example
$u = (1, 2, 3)$, $v = (4, -5, 6)$: $1\cdot4 + 2\cdot(-5) + 3\cdot6 = 4 - 10 + 18 = 12$.
$(1, 0)\cdot(0, 1) = 0$ — perpendicular axes.

<svg xmlns="http://www.w3.org/2000/svg" width="260" height="170" viewBox="0 0 260 170" role="img" aria-label="Two arrows from a common origin with the angle theta between them">
<title>Dot product and angle</title>
<line x1="30" y1="140" x2="230" y2="140" stroke="#999"/><line x1="30" y1="140" x2="30" y2="10" stroke="#999"/>
<line x1="30" y1="140" x2="210" y2="110" stroke="#1f77b4" stroke-width="3"/><text x="200" y="102" font-size="14" fill="#1f77b4">u</text>
<line x1="30" y1="140" x2="110" y2="30" stroke="#d62728" stroke-width="3"/><text x="112" y="28" font-size="14" fill="#d62728">v</text>
<path d="M 80 132 A 50 50 0 0 0 60 100" fill="none" stroke="#333"/><text x="70" y="118" font-size="13">θ</text>
</svg>

*Figure (original): u·v = ‖u‖‖v‖cos θ — positive here because θ < 90°.*

## Common mistakes
* Using `zip` without checking lengths: `zip` silently truncates to the shorter vector.
* Confusing the dot product (a number) with element-wise multiplication (a vector).
* Starting the accumulator from `u[0]*v[0]` and then looping over all elements again.

## Why this matters
Dot products are the core operation of linear regression, neural network layers, cosine
similarity in NLP retrieval and attention scores in transformers.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
