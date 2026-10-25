r"""Reference solution for AG-10 Conversation Memory Window by Hand.

The system message is always kept. Recent messages are added newest-first until the budget would be
exceeded, which yields a contiguous recent window. If history was dropped, a marker is inserted; when
the marker itself doesn't fit, the oldest kept message is sacrificed and the count updated.
"""
def count_tokens(text):
    return len(text.split())


def _cost(m):
    return count_tokens(m["content"]) + 4


def fit_context(messages, budget):
    head = messages[:1] if messages and messages[0]["role"] == "system" else []
    rest = messages[len(head):]
    used = sum(_cost(m) for m in head)
    if used > budget:
        raise ValueError("system message exceeds the budget")
    kept = []
    for m in reversed(rest):
        if used + _cost(m) > budget:
            break
        kept.append(m)
        used += _cost(m)
    kept.reverse()
    dropped = len(rest) - len(kept)
    while dropped > 0:
        marker = {"role": "system", "content": f"[{dropped} earlier messages omitted]"}
        if used + _cost(marker) <= budget:
            return head + [marker] + kept
        if len(kept) <= 1:
            return head + kept  # never sacrifice the newest message for the marker
        used -= _cost(kept.pop(0))
        dropped += 1
    return head + kept
