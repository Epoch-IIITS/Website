r"""Reference solution for PY-25 Classes: A Bank Account.

All validation happens before any attribute changes, so a failed call leaves the object as it
was. `history` is created per object in `__init__`. `transfer_to` reuses `withdraw` and
`deposit`, so their checks apply and the withdrawal's exception stops the deposit. Interest is
looked up through `self`, which finds the class attribute.
"""
class BankAccount:
    interest_rate = 0.02

    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("starting balance cannot be negative")
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount
        self.history.append(("deposit", amount))
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self.history.append(("withdraw", amount))
        return self.balance

    def transfer_to(self, other, amount):
        self.withdraw(amount)
        other.deposit(amount)

    def apply_interest(self):
        return self.deposit(round(self.balance * self.interest_rate, 2))

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"
