# Deterministic Game Loops

## Learning outcomes

After this lesson you can:

- Write a loop with early termination
- Model game state deterministically
- Validate inputs and limits

## Intuition
An interactive guessing game ("too low", "too high", "correct!") is really a loop over guesses
with a stopping condition. If we pass the guesses in as a list instead of calling `input()`, the
game becomes **deterministic** and testable — the same idea used to test agents with scripted
model outputs (AG-06).

## Precise explanation
* Loop over guesses; compare each to the target; produce one feedback string per guess.
* **Early termination:** `break` leaves the loop as soon as the guess is correct; later guesses
  are ignored.
* **Attempt limit:** stop after `max_attempts` guesses even if not solved.
* The final status depends on *how* the loop ended. Python's `for ... else` runs the `else`
  block only if the loop was **not** broken — handy, but a boolean flag is often clearer.

State summary returned as a dict:
```python
{"feedback": [...], "attempts": k, "won": True/False}
```

## Worked example
target = 42, guesses = [50, 25, 42, 10]:
50 → "too high", 25 → "too low", 42 → "correct" → stop. attempts = 3, won = True;
the guess 10 is never examined.

## Common mistakes
* Forgetting to `break`, so guesses after the correct one add feedback.
* Counting attempts with `len(guesses)` instead of guesses actually used.
* Off-by-one with the attempt limit (`>` vs `>=`).
* Using `input()` — untestable and blocks automated runners.

## Why this matters
Every agent, simulator and RL environment is a loop of "observe, act, check if done, stop at a
step budget". This is the smallest version of that loop.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
