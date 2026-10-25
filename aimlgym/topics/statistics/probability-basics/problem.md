# ST-06 · Probability by Counting Outcomes

**Topic:** Statistics · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** ST-04 Histogram with Equal-Width Bins

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `two_dice()` → list of all 36 outcomes `(d1, d2)` with `d1, d2` in 1..6, ordered by `d1`
   then `d2`.
2. `probability(space, event)` → `Fraction` of outcomes where `event(outcome)` is true. Raise
   `ValueError` for an empty space.
3. `complement(space, event)` → probability that the event does **not** happen.
4. `union(space, a, b)` → $P(A \cup B)$ computed by inclusion–exclusion (call `probability`
   three times).
5. `independent(space, a, b)` → `True` if $P(A \cap B) = P(A)P(B)$ exactly.

**Examples**
```python
space = two_dice()
probability(space, lambda o: sum(o) == 7)          # Fraction(1, 6)
union(space, lambda o: o[0] == 6, lambda o: o[1] == 6)   # Fraction(11, 36)
independent(space, lambda o: o[0] % 2 == 0, lambda o: sum(o) == 7)   # True
```

## Hints

<details><summary>Hint 1</summary>

`[(d1, d2) for d1 in range(1, 7) for d2 in range(1, 7)]` builds the space in the right order.

</details>

<details><summary>Hint 2</summary>

`Fraction(sum(1 for o in space if event(o)), len(space))` is the probability.

</details>

<details><summary>Hint 3</summary>

The intersection event is `lambda o: a(o) and b(o)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_space` | Use two nested loops (or a nested comprehension) over 1..6, first die outer. |
| `test_probability_exact` | Return `Fraction(count, len(space))`, not a float. |
| `test_union_overlap` | Subtract the probability of both events, which inclusion–exclusion counts twice. |
| `test_independence` | Compare P(A and B) with P(A) * P(B) using Fractions. |
| `test_empty_space` | Raise ValueError when the sample space is empty. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Events are predicates, so intersections are built by combining predicates with `and`. Every
probability is an exact `Fraction`, which makes the independence test an exact equality, and the
union follows the inclusion–exclusion formula rather than counting directly.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [fractions — Rational numbers](https://docs.python.org/3/library/fractions.html) — Python Software Foundation (`S058`)
