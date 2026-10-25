# While Loops

## Learning outcomes

After this lesson you can:

- Repeat work with while
- Stop a loop with a sentinel value and break
- Keep running totals, counts and maxima
- Use None for 'no value yet'

## Intuition
Sometimes you do not know in advance how many times to repeat something: "keep reading numbers
until the user types `done`". A `while` loop repeats its block for as long as its condition is
true.

## Precise explanation
```python
count = 0
while count < 3:      # checked before every repetition
    print(count)
    count += 1        # without this the loop never ends
```
* `while True:` loops forever until a `break` statement leaves it — a common pattern when the
  stopping condition is discovered *inside* the loop.
* `continue` skips the rest of the current repetition.
* A **sentinel** is a special input that means "stop", such as `done`.
* `None` represents "no value yet". Test it with `is None`.

```python
largest = None
while True:
    line = input().strip()
    if line == "done":
        break
    x = int(line)
    if largest is None or x > largest:
        largest = x
```

## Worked example
Lines `4`, `9`, `2`, `done`: count 1→2→3, total 4→13→15, largest 4→9→9. Output:
`count=3 total=15 max=9`.

## Common mistakes
* Infinite loops: the condition never becomes false and there is no `break`.
* Converting the sentinel: `int("done")` raises `ValueError`; check for it first.
* Starting `largest = 0`, which is wrong when every number is negative.

## Why this matters
Training loops run "until converged", agents loop "until the goal is reached or the step budget
runs out" (AG-05 later), and servers loop over incoming requests.

## References

- [The Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html) — Python Software Foundation (`S042`)
