# For Loops and range

## Learning outcomes

After this lesson you can:

- Loop a known number of times with for and range
- Use range(start, stop, step)
- Loop over the characters of a string
- Combine loops with conditionals and %

## Intuition
When you know what to repeat over — the numbers 1 to n, or the letters of a word — a `for` loop
is simpler than `while`: it hands you each item in turn and stops by itself.

## Precise explanation
```python
for i in range(5):        # 0, 1, 2, 3, 4   (stop is excluded)
    print(i)
for i in range(1, 6):     # 1, 2, 3, 4, 5
    ...
for i in range(10, 0, -3):  # 10, 7, 4, 1  (step may be negative)
    ...
for ch in "abc":          # 'a', 'b', 'c'
    ...
```
* `range(stop)`, `range(start, stop)`, `range(start, stop, step)` produce integers from `start`
  up to but not including `stop`. `range(0)` and `range(1, 1)` are empty.
* `break` and `continue` work as in while loops.
* Loops can be nested; the inner loop runs completely for each outer repetition.

## Worked example
Sum of multiples of 3 or 5 up to 10:
```python
total = 0
for i in range(1, 11):
    if i % 3 == 0 or i % 5 == 0:
        total += i          # 3 + 5 + 6 + 9 + 10 = 33
```

## Common mistakes
* `range(1, n)` stops at `n - 1`; use `range(1, n + 1)` to include n.
* Testing `% 3` before `% 15` in FizzBuzz, so 15 prints `Fizz` instead of `FizzBuzz`.
* Changing the loop variable inside the loop and expecting it to affect the next repetition.

## Why this matters
Epoch loops in training, sweeps over hyperparameters, and iteration over pixels, tokens and
episodes are all `for` loops.

## References

- [The Python Tutorial: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html) — Python Software Foundation (`S042`)
