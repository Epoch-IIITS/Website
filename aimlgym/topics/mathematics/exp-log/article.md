# Exponentials and Logarithms

## Learning outcomes

After this lesson you can:

- Use the rules log(ab) = log a + log b and log_b x = ln x / ln b
- Avoid underflow by adding log-probabilities instead of multiplying probabilities
- Compute log-sum-exp stably by subtracting the maximum

## Intuition
The exponential $e^x$ grows by the same *factor* for each step in $x$; the natural logarithm
$\ln x$ undoes it, answering "what power of $e$ gives $x$?". Logs turn multiplication into
addition, which is why ML works with **log-probabilities**: multiplying hundreds of small
probabilities underflows to 0, but adding their logs is perfectly stable.

## Precise explanation
* $e \approx 2.71828$; `math.exp(x)` is $e^x$ and `math.log(x)` is $\ln x$ (only for $x > 0$).
* Rules: $\ln(ab) = \ln a + \ln b$, $\ln(a^k) = k\ln a$, $\ln 1 = 0$, $e^{\ln x} = x$.
* Change of base: $\log_b x = \dfrac{\ln x}{\ln b}$, e.g. $\log_2 8 = 3$.
* Compound growth: an amount growing by rate $r$ per step doubles after
  $t = \dfrac{\ln 2}{\ln(1+r)}$ steps.
* **Log-likelihood**: $\ln \prod_i p_i = \sum_i \ln p_i$.
* **Log-sum-exp**: $\mathrm{LSE}(v) = \ln \sum_i e^{v_i}$. Computing $e^{1000}$ overflows, so
  use $\mathrm{LSE}(v) = m + \ln\sum_i e^{v_i - m}$ with $m = \max_i v_i$; every exponent is then
  at most $e^0 = 1$.

## Worked example
Probabilities `[1e-5] * 1000`: the product is $10^{-5000}$, which a float stores as `0.0`, and
`math.log(0.0)` raises `ValueError`. The sum of logs is $1000 \ln 10^{-5} \approx -11512.9$.
`logsumexp([1000, 1000])` $= 1000 + \ln 2 \approx 1000.693$.

## Common mistakes
* `math.log(x, 10)` vs `math.log10(x)` — both work; `math.log(x)` alone is base $e$, not 10.
* Taking the log of 0 or a negative number.
* Implementing log-sum-exp directly, which overflows for large inputs or underflows to
  `log(0)` for very negative ones.

## Why this matters
Cross-entropy loss, perplexity, Naive Bayes and softmax (DL-02) all rely on these
identities, and MA-03 is built from $e^{-x}$.

## Library implementation

The `math` module already provides `math.log(x, base)`, `math.log2`, `math.log10` and
`math.log1p(r)` (an accurate $\ln(1 + r)$ for small $r$). For log-sum-exp, SciPy offers
`scipy.special.logsumexp`, which uses the same max-subtraction trick (it also handles arrays and
weights). The tests below compare your functions with these when they are available; the SciPy
comparison is skipped if SciPy is not installed.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)
