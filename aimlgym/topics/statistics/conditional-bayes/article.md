# Conditional Probability and Bayes' Rule

## Learning outcomes

After this lesson you can:

- Compute P(A | B) by restricting the sample space
- Derive and apply Bayes' rule with the law of total probability
- Explain the base-rate effect
- Update a belief after several observations

## Intuition
Knowing something changes the odds. Among two-dice rolls, $P(\text{total} = 8)$ is 5/36, but if
you are told the first die shows 6, only the 6 outcomes starting with 6 remain and one of them
totals 8: the probability becomes 1/6. Conditioning means *shrinking the sample space* to the
outcomes consistent with what you know.

## Precise explanation
$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0.$$
**Bayes' rule** reverses a conditional:
$$P(D \mid +) = \frac{P(+ \mid D)\,P(D)}{P(+)}, \qquad
  P(+) = P(+ \mid D)P(D) + P(+ \mid \neg D)P(\neg D).$$
For a medical test: $P(D)$ is the **prior** (how common the disease is), $P(+ \mid D)$ the
**sensitivity**, $P(+ \mid \neg D)$ the **false-positive rate**, and $P(D \mid +)$ the
**posterior**. For a negative result use $P(- \mid D) = 1 - \text{sensitivity}$ and
$P(- \mid \neg D) = 1 - \text{false-positive rate}$.

**Sequential updating**: after one result, the posterior becomes the prior for the next
(assuming results are independent given the true state).

## Worked example
Prior 1%, sensitivity 90%, false-positive rate 5%:
$P(+) = 0.9 \cdot 0.01 + 0.05 \cdot 0.99 = 0.0585$, so $P(D \mid +) = 0.009 / 0.0585 \approx 0.154$.
A positive test raises the probability from 1% to only about 15% because healthy people vastly
outnumber sick ones — the **base-rate effect**.

## Common mistakes
* Confusing $P(+ \mid D)$ (90%) with $P(D \mid +)$ (15%).
* Forgetting the false positives in the denominator.
* Dividing by $P(B) = 0$.

## Why this matters
Naive Bayes text classification (NL-14) is Bayes' rule applied to words, and
reasoning about precision versus recall (ML-06) is reasoning about base rates.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
