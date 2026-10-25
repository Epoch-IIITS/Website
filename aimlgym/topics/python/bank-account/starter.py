class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        # TODO: validate, update, record, return
        self.balance += amount
        return self.balance

    # TODO: withdraw, transfer_to, apply_interest, __repr__ and the class attribute
