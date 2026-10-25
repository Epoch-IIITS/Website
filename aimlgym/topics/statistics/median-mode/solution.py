r"""Reference solution for ST-02 Median and Mode.

`sorted` returns a new list so the input is untouched; integer division picks the middle index
and the even case averages two values. `modes` counts frequencies with a dict and keeps every
value tied for the maximum count, sorted for a deterministic answer.
"""
def median(data):
    if not data:
        raise ValueError("median of empty data")
    s = sorted(data)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2


def modes(data):
    if not data:
        return []
    counts = {}
    for x in data:
        counts[x] = counts.get(x, 0) + 1
    top = max(counts.values())
    return sorted(k for k, c in counts.items() if c == top)
