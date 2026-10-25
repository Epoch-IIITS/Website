r"""Reference solution for PY-21 Safe Division with Exceptions.

`safe_divide` catches exactly one exception type, so programming errors such as dividing a
string still raise `TypeError`. `divide_pairs` reuses it, records `None` for failures and the
index of each failure. Indices come out sorted automatically because the loop visits them in order.
"""
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def divide_pairs(pairs):
    results = []
    failed = []
    for i, (a, b) in enumerate(pairs):
        r = safe_divide(a, b)
        results.append(r)
        if r is None:
            failed.append(i)
    return results, failed
