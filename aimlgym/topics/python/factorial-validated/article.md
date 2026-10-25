# Validating Input and Raising Exceptions

## Learning outcomes

After this lesson you can:

- Raise exceptions for invalid input
- Use isinstance checks correctly
- Compute a product iteratively

## Intuition
A function has a *contract*: what it accepts and what it promises to return. When a caller
breaks the contract (e.g. asks for the factorial of −3), the function should fail **loudly**
with a clear error rather than return a wrong answer silently.

## Precise explanation
The factorial of a non-negative integer $n$ is $n! = 1 \cdot 2 \cdots n$, with $0! = 1$ (the
empty product).

```python
result = 1
for k in range(2, n + 1):
    result *= k
```
Python integers have arbitrary precision, so `factorial(50)` is exact.

**Raising exceptions**
* `TypeError` — the argument has the wrong *type* (e.g. `2.5`, `"5"`).
* `ValueError` — right type, unacceptable *value* (e.g. `-3`).
```python
if not isinstance(n, int) or isinstance(n, bool):
    raise TypeError("n must be an int")
if n < 0:
    raise ValueError("n must be >= 0")
```
`bool` is a subclass of `int` in Python (`True == 1`), so it must be excluded explicitly if you
want to reject it.

## Worked example
`factorial(5)`: result 1 → ×2 = 2 → ×3 = 6 → ×4 = 24 → ×5 = 120.

## Common mistakes
* Returning `-1` or `None` for bad input — the caller may not notice.
* `range(1, n)` — stops at n−1 (off-by-one).
* Recursion without a base case for 0 → infinite recursion.
* Accepting `5.0` because `5.0 == 5`; the contract asks for an `int`.

## Why this matters
ML code fails in confusing ways deep inside a pipeline when inputs are invalid. Early, specific
exceptions turn a mysterious NaN three steps later into an obvious message. Factorials also
power combinatorics (binomial coefficients, MA-07).

## Library implementation

`math.factorial(n)` computes the same value (and also raises `ValueError` for negative
numbers and `TypeError` for floats). It is implemented in C and uses a faster
divide-and-conquer product for large `n`, but the result is identical.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
