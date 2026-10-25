r"""Reference solution for PY-05 Arithmetic Operators.

Floor division gives the number of whole hours; the remainder holds what is left, which is split
again into minutes and seconds. `:02d` pads minutes and seconds to two digits and `:.2f` shows
the true-division result with two decimals.
"""
total = int(input())
hours = total // 3600
rest = total % 3600
minutes = rest // 60
seconds = rest % 60
print(f"{hours}:{minutes:02d}:{seconds:02d}")
print(f"{total / 60:.2f} minutes")
