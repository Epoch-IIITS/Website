r"""Reference solution for PY-01 Hello, print().

Each `print` call writes its arguments joined by `sep` and then writes `end`. Changing `sep`
produces the date, an empty call produces the blank line, and `end="..."` replaces the newline
so that `done` continues the fifth line. Single quotes let the last string contain double quotes.
"""
# Line 1: a plain string
print("Hello, world!")
# Line 2: three arguments joined by the default separator " "
print("Python", "is", "fun")
# Line 3: a custom separator
print("2026", "10", "24", sep="-")
# Line 4: an empty line
print()
# Line 5: end="..." keeps the next print on the same line
print("Loading", end="...")
print("done")
# Line 6: single quotes around text that contains double quotes
print('She said "hi"')
