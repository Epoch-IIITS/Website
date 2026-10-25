r"""Reference solution for PY-04 Reading Input.

The first `input()` reads the name and `strip()` removes stray spaces. The second line is
converted to an `int` so that subtraction works. Both results are printed with f-strings.
"""
name = input().strip()
year = int(input())
print(f"Hello, {name}!")
print(f"In 2030 you will turn {2030 - year}.")
