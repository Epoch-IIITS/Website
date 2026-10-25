r"""Reference solution for PY-12 Filter Even Numbers.

A conditional list comprehension iterates once, keeps elements whose remainder modulo 2 is zero,
and returns a new list, so the input is untouched and order is preserved. Python's `%` makes
the test correct for negative numbers.
"""
def evens(nums):
    return [x for x in nums if x % 2 == 0]
