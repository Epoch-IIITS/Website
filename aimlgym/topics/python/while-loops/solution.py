r"""Reference solution for PY-08 While Loops: Read Until Done.

The loop has no natural end, so `while True` with a `break` on the sentinel is clearest. Three
accumulators are updated per number; starting the maximum at `None` makes the first number win
regardless of sign, and lets the empty case print `None`.
"""
count = 0
total = 0
largest = None
while True:
    line = input().strip()
    if line == "done":
        break
    x = int(line)
    count += 1
    total += x
    if largest is None or x > largest:
        largest = x
print(f"count={count} total={total} max={largest}")
