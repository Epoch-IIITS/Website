# Grouping and Sorting Records

## Learning outcomes

After this lesson you can:

- Group records with dict.setdefault / defaultdict
- Sort with a key function and tie-breaking
- Round results correctly

## Intuition
Given a pile of (student, score) slips, you sort them into one stack per student, compute each
stack's average, then rank students. That is **group → aggregate → sort**, the same recipe as
SQL `GROUP BY` and pandas `groupby` (PD-08).

## Precise explanation
**Grouping** with a dict of lists:
```python
groups = {}
for name, score in records:
    groups.setdefault(name, []).append(score)
```
`setdefault(key, default)` returns the existing value or inserts `default` first.
`collections.defaultdict(list)` does the same automatically.

**Sorting with a key**: `sorted(items, key=f)` sorts by `f(item)`. To sort by average
descending and break ties by name ascending, use a tuple key with a negated number:
```python
sorted(rows, key=lambda r: (-r[1], r[0]))
```
Tuples compare element by element, so the name is consulted only when averages are equal.

**Rounding**: `round(x, 2)` rounds to 2 decimals (using round-half-to-even on the exact binary
value). Round only for the final output, never in intermediate steps.

## Worked example
records = [("ann", 90), ("bob", 70), ("ann", 80), ("cy", 85)]
groups: ann → [90, 80], bob → [70], cy → [85]; averages 85.0, 70.0, 85.0.
Sorted: (-85, "ann"), (-85, "cy"), (-70, "bob") → ann, cy, bob.

## Common mistakes
* `sorted(..., reverse=True)` with a tuple key reverses the name tie-break too.
* Rounding each score before averaging.
* Overwriting `groups[name] = [score]` instead of appending.

## Why this matters
Grouped statistics drive per-class metrics, per-client summaries in federated learning and
leaderboards; deterministic tie-breaking keeps outputs reproducible.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
