# Partial Derivatives and the Gradient

## Learning outcomes

After this lesson you can:

- Define partial derivatives and the gradient
- Approximate each partial with central differences
- Use the gradient in multivariable descent

## Intuition
A function of several variables is a landscape. The **partial derivative** with respect to
$x_i$ is the slope if you walk only along the $x_i$ axis. Collecting all partials gives the
**gradient** — an arrow pointing in the direction of steepest ascent.

## Precise explanation
For $f: \mathbb{R}^n \to \mathbb{R}$,
$$\nabla f(x) = \left(\frac{\partial f}{\partial x_1}, \dots, \frac{\partial f}{\partial x_n}\right),\qquad
\frac{\partial f}{\partial x_i} \approx \frac{f(x + h e_i) - f(x - h e_i)}{2h},$$
where $e_i$ is the unit vector along axis $i$ (perturb one coordinate, keep the others fixed).
This needs $2n$ function evaluations.

Gradient descent in $n$ dimensions: $x \leftarrow x - \eta \nabla f(x)$.

## Worked example
$f(x, y) = x^2 + 3xy$. Exact: $\partial f/\partial x = 2x + 3y$, $\partial f/\partial y = 3x$.
At $(1, 2)$: $\nabla f = (8, 3)$.

## Common mistakes
* Perturbing the original list in place and forgetting to restore it — later partials are wrong.
* Perturbing all coordinates at once (that gives a directional derivative along (1,…,1)).
* Returning a tuple of tuples instead of a flat list of partials.

## Why this matters
Numerical gradients are how you *check* backpropagation (DL-13). Understanding "one coordinate at
a time" also explains why numerical gradients are too slow to train networks with millions of
parameters, motivating automatic differentiation.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
