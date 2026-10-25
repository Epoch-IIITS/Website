r"""Reference solution for PY-14 Fibonacci Sequence.

Two variables hold the current and next Fibonacci numbers. Simultaneous tuple assignment advances
the window by one step. Because the loop runs exactly n times, the n = 0 and n = 1 cases need no
special handling.
"""
def fibonacci(n):
    out = []
    a, b = 0, 1
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out
