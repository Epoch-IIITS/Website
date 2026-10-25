# PY-25 · Classes: A Bank Account

**Topic:** Python · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** PY-24 Text Statistics from stdin

Read the lesson first: [article.md](article.md)

## Task

Write `class BankAccount`:

* `BankAccount(owner, balance=0)` stores `owner` and `balance`; raise `ValueError` if the
  starting balance is negative. Each account has its own `history` list, initially empty.
* Class attribute `interest_rate = 0.02`.
* `deposit(amount)` — `amount` must be positive (else `ValueError`); adds it, appends
  `("deposit", amount)` to `history`, returns the new balance.
* `withdraw(amount)` — `amount` must be positive and at most the balance (else `ValueError`,
  and nothing changes); subtracts it, appends `("withdraw", amount)`, returns the new balance.
* `transfer_to(other, amount)` — withdraws from this account and deposits into `other`
  (if the withdrawal fails, `other` must not change).
* `apply_interest()` — adds `round(balance * interest_rate, 2)` as a deposit and returns the new
  balance (record it in history like a deposit).
* `__repr__` returns e.g. `BankAccount(owner='Ada', balance=120)` (use `{self.owner!r}`).

## Hints

<details><summary>Hint 1</summary>

Create `self.history = []` in `__init__` and check the start balance there.

</details>

<details><summary>Hint 2</summary>

In `withdraw`, raise before changing anything: `if amount <= 0 or amount > self.balance: raise ValueError(...)`.

</details>

<details><summary>Hint 3</summary>

`transfer_to` can call `self.withdraw(amount)` then `other.deposit(amount)`; `!r` in an f-string adds quotes.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_init_and_repr` | Create `self.history = []` in `__init__` and format `__repr__` with `{self.owner!r}`. |
| `test_invalid_amounts_change_nothing` | Raise ValueError before modifying balance or history. |
| `test_separate_histories` | Do not make `history` a class attribute; create it in `__init__`. |
| `test_transfer` | Withdraw first; if it raises, the deposit never happens. |
| `test_interest` | Define `interest_rate = 0.02` in the class body and deposit the rounded interest. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

All validation happens before any attribute changes, so a failed call leaves the object as it
was. `history` is created per object in `__init__`. `transfer_to` reuses `withdraw` and
`deposit`, so their checks apply and the withdrawal's exception stops the deposit. Interest is
looked up through `self`, which finds the class attribute.

## References

- [The Python Tutorial: Classes](https://docs.python.org/3/tutorial/classes.html) — Python Software Foundation (`S046`)
- [The Python Tutorial: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) — Python Software Foundation (`S044`)
