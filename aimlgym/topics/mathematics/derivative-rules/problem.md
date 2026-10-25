# MA-11 · Derivative Rules and the Chain Rule

**Topic:** Mathematics for AI/ML · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** MA-10 Numerical Derivative (Central Difference), MA-03 The Sigmoid Function

Read the lesson first: [article.md](article.md)

## Task

Each function below returns a pair `(h, dh)` of one-argument functions.

1. `power_rule(n)` → $(x^n,\; n x^{n-1})$.
2. `sum_rule(f, df, g, dg)` → $(f+g,\; f'+g')$.
3. `product_rule(f, df, g, dg)` → $(fg,\; f'g + fg')$.
4. `chain_rule(f, df, g, dg)` → $(f\circ g,\; (f'\circ g)\cdot g')$.
5. `sigmoid_of_linear(a, b)` → the pair for $\sigma(ax + b)$, built with `chain_rule` from the
   sigmoid pair and the linear pair $(ax+b,\; a)$. Use a stable sigmoid as in MA-03.

**Example**
```python
h, dh = sigmoid_of_linear(3, 1)
h(0)     # ≈ 0.7311
dh(0)    # ≈ 0.5898
```

## Hints

<details><summary>Hint 1</summary>

Each rule returns two lambdas, e.g. `(lambda x: f(x) + g(x)), (lambda x: df(x) + dg(x))`.

</details>

<details><summary>Hint 2</summary>

Chain rule: `dh = lambda x: df(g(x)) * dg(x)` — the outer derivative is evaluated at g(x).

</details>

<details><summary>Hint 3</summary>

The sigmoid's derivative is `lambda u: sigmoid(u) * (1 - sigmoid(u))`; the linear pair is `(lambda x: a * x + b, lambda x: a)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_sum` | Return the sum of the functions and the sum of their derivatives. |
| `test_product` | Product rule: `df(x) * g(x) + f(x) * dg(x)`. |
| `test_chain` | Evaluate the outer derivative at `g(x)` and multiply by `dg(x)`. |
| `test_sigmoid_of_linear` | Build the pair with `chain_rule(sigmoid, dsigmoid, linear, dlinear)`. |
| `test_sigmoid_of_linear_stable` | Use the stable sigmoid from the starter for both the value and the derivative. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Every rule is a direct translation of its formula into a pair of closures. Because rules accept
and return pairs, they compose: `sigmoid_of_linear` is one call to `chain_rule`, and the tests
build larger expressions (products of chains) the same way and confirm them numerically.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
