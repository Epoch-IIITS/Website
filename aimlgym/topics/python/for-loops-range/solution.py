r"""Reference solution for PY-09 For Loops and range: FizzBuzz.

`range(1, n + 1)` visits every number once. The combined case is tested first because a number
divisible by 15 also passes the single tests. The sum is a separate condition inside the same
loop, so no second pass is needed.
"""
n = int(input())
total = 0
for i in range(1, n + 1):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
    if i % 3 == 0 or i % 5 == 0:
        total += i
print(f"sum={total}")
