# Arithmetic Operators

## Learning outcomes

After this lesson you can:

- Use //, % and ** alongside + - * /
- Apply operator precedence and parentheses
- Format numbers with :02d and :.2f

## Intuition
Converting 3725 seconds into hours, minutes and seconds is a division with remainders: how many
whole hours fit, and what is left over? Python has an operator for each part.

## Precise explanation
| Operator | Meaning | Example |
|---|---|---|
| `+ - *` | add, subtract, multiply | `7 * 2 == 14` |
| `/` | true division (always float) | `7 / 2 == 3.5` |
| `//` | floor division (round down) | `7 // 2 == 3`, `-7 // 2 == -4` |
| `%` | remainder (modulo) | `7 % 2 == 1` |
| `**` | power | `2 ** 10 == 1024` |

* For non-negative `a` and positive `b`: `a == (a // b) * b + a % b`.
* **Precedence**: `**` first, then `* / // %`, then `+ -`; use parentheses to be explicit:
  `2 + 3 * 4 == 14`, `(2 + 3) * 4 == 20`, `-2 ** 2 == -4`.
* **Augmented assignment**: `x += 5` means `x = x + 5` (also `-=`, `*=`, `//=`, ...).
* **Format specs** inside f-strings: `f"{5:02d}"` → `05` (at least 2 digits, zero-padded);
  `f"{62.0833:.2f}"` → `62.08` (two decimals).

## Worked example
`3725` seconds: hours = `3725 // 3600` = 1; remaining = `3725 % 3600` = 125;
minutes = `125 // 60` = 2; seconds = `125 % 60` = 5 → `1:02:05`.

## Common mistakes
* Using `/` where you want a whole number: `3725 / 3600` is `1.034...`.
* Forgetting zero-padding, producing `1:2:5`.
* Writing `x ^ 2` for a power — `^` is bitwise XOR in Python; use `x ** 2`.

## Why this matters
Integer division and remainders appear in batching (`n // batch_size` full batches), image
indexing (row = `i // width`, column = `i % width`) and time-series resampling.

## References

- [The Python Tutorial: An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — Python Software Foundation (`S040`)
- [Built-in Types](https://docs.python.org/3/library/stdtypes.html) — Python Software Foundation (`S049`)
