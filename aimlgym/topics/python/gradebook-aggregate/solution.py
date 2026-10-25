r"""Reference solution for PY-18 Gradebook Aggregation.

Invalid scores are filtered while grouping, so names that only have invalid scores never appear.
Averages are computed from raw scores and rounded once. The tuple sort key `(-average, name)`
gives descending averages with ascending-name tie-breaks in a single stable sort.
"""
def gradebook(records):
    groups = {}
    for name, score in records:
        if 0 <= score <= 100:
            groups.setdefault(name, []).append(score)
    rows = []
    for name, scores in groups.items():
        avg = sum(scores) / len(scores)
        rows.append((name, round(avg, 2), len(scores)))
    rows.sort(key=lambda r: (-r[1], r[0]))
    return rows
