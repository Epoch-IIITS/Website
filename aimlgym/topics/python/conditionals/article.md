# Conditionals

## Learning outcomes

After this lesson you can:

- Compare values with == != < <= > >=
- Branch with if / elif / else
- Combine conditions with and, or, not and chained comparisons

## Intuition
Programs make decisions: *if* the score is at least 90, the grade is A; *otherwise, if* it is at
least 80, B; and so on. Python checks the conditions from top to bottom and runs the first block
whose condition is true.

## Precise explanation
```python
if score < 0 or score > 100:
    print("Invalid score")
elif score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("F")
```
* Comparisons produce bools: `==` equal, `!=` not equal, `<`, `<=`, `>`, `>=`.
* `and` is true only if both sides are; `or` if at least one is; `not` flips a bool.
* Chained comparison: `0 <= score <= 100` means `0 <= score and score <= 100`.
* The **indented** lines (4 spaces) form the block. `elif` and `else` are optional; at most one
  branch runs.
* `=` assigns, `==` compares. `if score = 90:` is a `SyntaxError`.

## Worked example
`score = 85`: `85 < 0 or 85 > 100` is False → `85 >= 90` False → `85 >= 80` True → prints `B`;
the remaining branches are skipped.

## Common mistakes
* Wrong order: testing `score >= 60` before `score >= 90` gives every passing score a D.
* Writing `if 0 <= score and <= 100` — each side of `and` must be a full comparison.
* Forgetting the colon after the condition, or mixing tabs and spaces.

## Why this matters
Thresholds turn model scores into decisions (spam / not spam), and branches handle edge cases
such as empty data, which you will meet in every later topic.

## References

- [The Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html) — Python Software Foundation (`S042`)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — Python Software Foundation (`S049`)
