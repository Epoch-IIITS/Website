"""Tests for PY-25 Classes: A Bank Account.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import importlib
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = importlib.import_module(os.environ.get("AIMLGYM_TARGET", "solution"))


class TestBankAccount(unittest.TestCase):
    def test_init_and_repr(self):
        a = S.BankAccount("Ada", 100)
        self.assertEqual((a.owner, a.balance, a.history), ("Ada", 100, []))
        self.assertEqual(repr(a), "BankAccount(owner='Ada', balance=100)")
        self.assertEqual(S.BankAccount("Bo").balance, 0)

    def test_negative_start(self):
        with self.assertRaises(ValueError):
            S.BankAccount("X", -1)

    def test_deposit_withdraw(self):
        a = S.BankAccount("Ada", 100)
        self.assertEqual(a.deposit(50), 150)
        self.assertEqual(a.withdraw(30), 120)
        self.assertEqual(a.history, [("deposit", 50), ("withdraw", 30)])

    def test_invalid_amounts_change_nothing(self):
        a = S.BankAccount("Ada", 10)
        for bad in (lambda: a.deposit(0), lambda: a.deposit(-5),
                    lambda: a.withdraw(-1), lambda: a.withdraw(11)):
            with self.assertRaises(ValueError):
                bad()
        self.assertEqual((a.balance, a.history), (10, []))

    def test_separate_histories(self):
        a, b = S.BankAccount("A"), S.BankAccount("B")
        a.deposit(5)
        self.assertEqual(b.history, [])

    def test_transfer(self):
        a, b = S.BankAccount("A", 50), S.BankAccount("B", 5)
        a.transfer_to(b, 20)
        self.assertEqual((a.balance, b.balance), (30, 25))
        with self.assertRaises(ValueError):
            a.transfer_to(b, 100)
        self.assertEqual((a.balance, b.balance), (30, 25))

    def test_interest(self):
        self.assertEqual(S.BankAccount.interest_rate, 0.02)
        a = S.BankAccount("A", 1000)
        self.assertEqual(a.apply_interest(), 1020)
        self.assertEqual(a.history[-1], ("deposit", 20.0))


if __name__ == "__main__":
    unittest.main()
