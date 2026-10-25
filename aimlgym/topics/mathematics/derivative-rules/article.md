# Derivative Rules and the Chain Rule

## Learning outcomes

After this lesson you can:

- Apply the power, sum, product and chain rules
- Represent a function together with its derivative as a pair
- Verify an analytic derivative against a central-difference estimate

## Intuition
MA-10 *estimates* a derivative by nudging the input. Rules give the *exact*
derivative of a formula built from simpler pieces. The most important is the **chain rule**:
when one function feeds another, their rates of change multiply — the idea behind
backpropagation.

## Precise explanation
| Rule | Function | Derivative |
|---|---|---|
| power | $x^n$ | $n x^{n-1}$ |
| sum | $f + g$ | $f' + g'$ |
| product | $f g$ | $f' g + f g'$ |
| chain | $f(g(x))$ | $f'(g(x))\, g'(x)$ |
| exp, log | $e^x$, $\ln x$ | $e^x$, $1/x$ |
| sigmoid | $\sigma(x)$ | $\sigma(x)(1-\sigma(x))$ |

In code, represent a differentiable function as a **pair** `(f, df)` of Python functions. Each
rule takes pairs and returns a new pair, so you can build derivatives of complicated formulas
from small, tested pieces.

```python
def chain_rule(f, df, g, dg):
    h = lambda x: f(g(x))
    dh = lambda x: df(g(x)) * dg(x)
    return h, dh
```

## Worked example
$h(x) = \sigma(3x + 1)$: outer $f = \sigma$, inner $g(x) = 3x + 1$ with $g' = 3$, so
$h'(x) = \sigma(3x+1)(1-\sigma(3x+1)) \cdot 3$. At $x = 0$: $\sigma(1) \approx 0.7311$ and
$h'(0) \approx 0.7311 \cdot 0.2689 \cdot 3 \approx 0.5898$.

## Common mistakes
* Forgetting the inner derivative: $\frac{d}{dx}\sigma(3x) \ne \sigma'(3x)$; multiply by 3.
* Evaluating the outer derivative at $x$ instead of at $g(x)$.
* Product rule as $f' g'$.

## Why this matters
Backpropagation (DL-10, DL-08) is the chain rule applied repeatedly,
and gradient descent (MA-13) needs these derivatives.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
