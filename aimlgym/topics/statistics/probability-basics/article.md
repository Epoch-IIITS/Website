# Probability by Counting Outcomes

## Learning outcomes

After this lesson you can:

- Describe a sample space and events as Python data and predicates
- Compute exact probabilities with fractions.Fraction
- Apply the complement and inclusion–exclusion rules
- Test two events for independence

## Intuition
Roll two fair dice. There are 36 equally likely outcomes. The probability of an event such as
"the total is 7" is simply the fraction of outcomes in which it happens: 6 of 36, so 1/6.
When outcomes are equally likely, probability is counting.

## Precise explanation
* **Sample space** $\Omega$: the list of all outcomes, e.g. pairs `(d1, d2)`.
* **Event**: a set of outcomes — in code, a predicate function `lambda o: o[0] + o[1] == 7`.
* With equally likely outcomes, $P(A) = \dfrac{|A|}{|\Omega|}$.
* **Complement**: $P(\text{not } A) = 1 - P(A)$.
* **Union** (inclusion–exclusion): $P(A \cup B) = P(A) + P(B) - P(A \cap B)$ — outcomes in both
  would otherwise be counted twice.
* **Independence**: $A$ and $B$ are independent when $P(A \cap B) = P(A)\,P(B)$.

`fractions.Fraction(6, 36)` stores the exact value `Fraction(1, 6)`, so equality tests like
independence are exact; with floats, `0.1 * 3 == 0.3` is False.

## Worked example
$A$ = "first die is even" (18 outcomes), $B$ = "total is 7" (6 outcomes),
$A \cap B$ = {(2,5), (4,3), (6,1)} (3 outcomes). $P(A)P(B) = \frac12 \cdot \frac16 = \frac1{12}
= \frac{3}{36} = P(A \cap B)$, so they are independent. $P(A \cup B) = \frac{18 + 6 - 3}{36} = \frac{21}{36}$.

## Common mistakes
* Assuming outcomes are equally likely when they are not (the *totals* 2..12 are not).
* Adding $P(A) + P(B)$ for overlapping events.
* Confusing independent with mutually exclusive: exclusive events with non-zero probability are
  never independent.

## Why this matters
Probability is the language of classification ("70% spam"), of ST-07 and Naive
Bayes, and of every simulation in this topic.

## Library implementation

The nested comprehension in `two_dice` is what `itertools.product(range(1, 7), repeat=2)`
generates, and `Fraction` is the standard library's exact rational type. There is no library
function for "probability of a predicate" — counting is the method. The test below confirms
the `itertools` version gives the same space.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [fractions — Rational numbers](https://docs.python.org/3/library/fractions.html) — Python Software Foundation (`S058`)
