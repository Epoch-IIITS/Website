# Classes and Objects

## Learning outcomes

After this lesson you can:

- Define a class with __init__, attributes and methods
- Protect an object's state by validating in methods
- Distinguish class attributes from instance attributes
- Give objects a readable __repr__

## Intuition
A class is a blueprint; an object is one thing built from it. Every bank account has an owner
and a balance (its **state**) and supports deposit and withdraw (its **behaviour**). A class
keeps the data and the functions that change it together, so the balance can only change in
ways the class allows.

## Precise explanation
```python
class Counter:
    step = 1                          # class attribute: shared by all counters

    def __init__(self, start=0):      # runs when you write Counter(...)
        self.value = start            # instance attribute: one per object

    def increment(self):              # a method; self is the object it is called on
        self.value += self.step
        return self.value

    def __repr__(self):               # what the object looks like when printed
        return f"Counter(value={self.value})"

c = Counter(5)
c.increment()      # 6;  same as Counter.increment(c)
```
* `self` is just the first parameter: the object the method was called on.
* Attributes set on `self` in `__init__` exist for every object.
* Methods validate input and raise exceptions (PY-19) rather than letting
  the object reach an invalid state.
* Objects are passed by reference: two names can refer to the same object.

## Worked example
```python
acct = BankAccount("Ada", 100)
acct.deposit(50)        # balance 150
acct.withdraw(30)       # balance 120
acct.history            # [('deposit', 50), ('withdraw', 30)]
acct                    # BankAccount(owner='Ada', balance=120)
```

## Common mistakes
* Forgetting `self` in a method definition, or writing `balance` instead of `self.balance`.
* Putting a mutable list as a *class* attribute (`history = []`), shared by every account —
  create it in `__init__`.
* Updating state before validating, so a failed withdrawal still changes the balance.
* Calling `BankAccount.deposit(50)` on the class instead of on an object.

## Why this matters
Later topics use classes everywhere: scikit-learn-style models with `fit`/`predict`
(ML-01), optimisers that keep momentum (DL-14), environments with
`reset`/`step` (RL-03) and agent tool registries.

## References

- [The Python Tutorial: Classes](https://docs.python.org/3/tutorial/classes.html) — Python Software Foundation (`S046`)
- [The Python Tutorial: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) — Python Software Foundation (`S044`)
