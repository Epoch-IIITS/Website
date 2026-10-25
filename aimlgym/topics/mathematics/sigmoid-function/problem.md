# MA-03 · The Sigmoid Function

**Topic:** Mathematics for AI/ML · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** MA-02 Exponentials and Logarithms

Read the lesson first: [article.md](article.md)

## Task

Implement with the `math` module:

1. `sigmoid(x)` — numerically stable for any float, including `±1000`: use
   $1/(1+e^{-x})$ for $x \ge 0$ and $e^{x}/(1+e^{x})$ for $x < 0$.
2. `sigmoid_derivative(x)` — $\sigma(x)(1-\sigma(x))$.
3. `logit(p)` — $\ln(p/(1-p))$; raise `ValueError` unless `0 < p < 1`.

**Examples**
```python
sigmoid(0)              # 0.5
sigmoid(-1000)          # 0.0 (no OverflowError)
sigmoid_derivative(0)   # 0.25
logit(0.5)              # 0.0
```

## Hints

<details><summary>Hint 1</summary>

Branch on the sign: `if x >= 0:` use the usual formula, else compute `z = math.exp(x)` and return `z / (1 + z)`.

</details>

<details><summary>Hint 2</summary>

`s = sigmoid(x); return s * (1 - s)`.

</details>

<details><summary>Hint 3</summary>

Validate with `if not 0 < p < 1: raise ValueError(...)`, then `math.log(p / (1 - p))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_extremes_no_overflow` | For negative x use `math.exp(x) / (1 + math.exp(x))` so the exponent never becomes huge. |
| `test_derivative` | Return `s * (1 - s)` where `s = sigmoid(x)`. |
| `test_logit_inverse` | logit(p) is `math.log(p / (1 - p))`. |
| `test_logit_domain` | Raise ValueError unless 0 < p < 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each branch of `sigmoid` only exponentiates a non-positive number, so `math.exp` never
overflows; the two formulas are algebraically equal. The derivative reuses the forward value,
which is how backpropagation computes it cheaply. `logit` validates its domain before the log.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)
