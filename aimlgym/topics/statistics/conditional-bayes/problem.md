# ST-07 · Conditional Probability and Bayes' Rule

**Topic:** Statistics · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** ST-06 Probability by Counting Outcomes

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `conditional(space, a, b)` → $P(A \mid B)$ as a `Fraction`, counting outcomes in a list of
   equally likely outcomes; raise `ValueError` if no outcome satisfies `b`.
2. `posterior(prior, sensitivity, false_positive_rate)` → $P(D \mid +)$ as a float.
3. `update(prior, sensitivity, false_positive_rate, results)` → the probability of $D$ after
   applying Bayes' rule once per result in `results` (a list of booleans: `True` = positive,
   `False` = negative), in order. An empty list returns the prior.

**Examples**
```python
dice = [(a, b) for a in range(1, 7) for b in range(1, 7)]
conditional(dice, lambda o: sum(o) == 8, lambda o: o[0] == 6)   # Fraction(1, 6)
posterior(0.01, 0.9, 0.05)                                     # ≈ 0.1538
update(0.01, 0.9, 0.05, [True, True])                          # ≈ 0.7660
```

## Hints

<details><summary>Hint 1</summary>

Count outcomes where `b` holds, and among those where `a` also holds; divide.

</details>

<details><summary>Hint 2</summary>

`evidence = sensitivity * prior + false_positive_rate * (1 - prior)`; posterior = numerator / evidence.

</details>

<details><summary>Hint 3</summary>

For a negative result use `1 - sensitivity` and `1 - false_positive_rate` as the likelihoods.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_conditional_dice` | Restrict to outcomes where `b` holds, then count `a` among them. |
| `test_conditional_zero` | Raise ValueError when no outcome satisfies the condition. |
| `test_posterior_base_rate` | The denominator must include false positives from the healthy group: `fpr * (1 - prior)`. |
| `test_update_two_positives` | Use each posterior as the prior for the next result. |
| `test_update_negative_and_empty` | For a negative result the likelihoods are `1 - sensitivity` and `1 - false_positive_rate`. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Conditioning keeps only the outcomes where `b` holds and counts `a` among them, which equals
$P(A\cap B)/P(B)$. The posterior divides the true-positive mass by all positive mass. `update`
reuses the same formula with likelihoods chosen by each result, feeding each posterior forward as
the next prior.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
