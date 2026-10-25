r"""Reference solution for PY-02 Variables and f-strings.

Four assignments create the variables with the requested types; `next_age` is computed from
`age`, so changing `age` and re-running the program would update it. Each f-string inserts one
variable into a fixed label.
"""
name = "Ada"
age = 19
height_m = 1.68
is_student = True
next_age = age + 1

print(f"Name: {name}")
print(f"Age next year: {next_age}")
print(f"Height: {height_m} m")
print(f"Student: {is_student}")
