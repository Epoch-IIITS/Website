r"""Reference solution for PY-11 Sum and Mean of a List.

One pass over the data maintains two accumulators: the running total and the count. Counting
inside the loop means the function would also work for any iterable (not only lists). The empty
case is detected via `count == 0` before division, avoiding `ZeroDivisionError`.
"""
def sum_and_mean(nums):
    total = 0
    count = 0
    for x in nums:
        total += x
        count += 1
    if count == 0:
        return 0, None
    return total, total / count
