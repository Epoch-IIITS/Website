# Mathematics for AI/ML

**You will be able to:** Use summation, exponentials, logarithms, the sigmoid, vectors, matrices, derivatives, the chain rule, integration, gradient descent, series and eigenvectors.

**Topic prerequisites:** Python

The mathematics that later topics use, each idea implemented in plain Python before NumPy
appears. It starts with notation (Σ and Π), exponentials and logarithms, and the sigmoid — the
pieces needed for probabilities and logistic regression — then moves through vectors and
matrices, counting, small linear systems, numerical and analytic derivatives (including the
chain rule used by backpropagation), integration, gradient descent, series and eigenvectors.

**Packages:** standard library only. Each lesson compares the hand-written version with the
`math` module where one exists; NP-02 and NP-06 later redo these
operations in NumPy and check that the answers agree.

**Project ideas:** ungraded briefs between steps suggest things to build with what you have learned so far.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | MA-01 | [Summation and Product Notation](summation/problem.md) | beginner | PY-17 |
| 2 | MA-02 | [Exponentials and Logarithms](exp-log/problem.md) | beginner | MA-01 |
| 3 | MA-03 | [The Sigmoid Function](sigmoid-function/problem.md) | beginner | MA-02 |
| 4 | MA-04 | [Dot Product](dot-product/problem.md) | beginner | MA-01 |
| 5 | MA-05 | [Vector Norm and Unit Vector](vector-norm-unit/problem.md) | beginner | MA-04 |
| 6 | MA-06 | [Matrix Multiplication](matrix-multiply/problem.md) | beginner | MA-04, PY-20 |
| 7 | MA-07 | [Binomial Coefficient](binomial-coefficient/problem.md) | intermediate | MA-01, PY-19 |
| 8 | MA-08 | [Solve a 2x2 System (Cramer's Rule)](solve-2x2-cramer/problem.md) | intermediate | MA-06 |
| 9 | MA-09 | [Inverse of a 2x2 Matrix](inverse-2x2/problem.md) | intermediate | MA-08 |
| 10 | MA-10 | [Numerical Derivative (Central Difference)](central-difference/problem.md) | intermediate | MA-02 |
| 11 | MA-11 | [Derivative Rules and the Chain Rule](derivative-rules/problem.md) | intermediate | MA-10, MA-03 |
| 12 | MA-12 | [Trapezoidal Integration](trapezoid-rule/problem.md) | intermediate | MA-10 |
| 13 | MA-13 | [Gradient Descent in 1D](gradient-descent-1d/problem.md) | advanced | MA-11 |
| 14 | MA-14 | [Numerical Gradient of f(x1..xn)](numerical-gradient/problem.md) | advanced | MA-10, MA-13 |
| 15 | MA-15 | [Taylor Series for exp(x)](taylor-exp/problem.md) | advanced | MA-11, MA-07 |
| 16 | MA-16 | [Dominant Eigenvalue by Power Iteration](power-iteration/problem.md) | advanced | MA-05, MA-06 |
| 17 | MA-P1 | [Project idea: Gradient-Descent Visualiser](gradient-descent-visualiser/project.md) | ungraded | MA-11, MA-13, MA-14, MA-15 |
