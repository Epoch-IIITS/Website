r"""Reference solution for NL-13 Rule-Based Suffix Stemmer.

`is_consonant` encodes Porter's y-rule recursively. The measure collapses the C/V pattern into
alternating runs and counts VC pairs. Step 1a picks the first matching suffix. In Step 1b, an EED
match blocks the ED rule even when its m > 0 condition fails (so "feed" stays "feed"), and the
tidy-up rules run only after ED or ING was actually removed.
"""
def is_consonant(word, i):
    ch = word[i]
    if ch in "aeiou":
        return False
    if ch == "y":
        return i == 0 or not is_consonant(word, i - 1)
    return True


def measure(stem):
    pattern = "".join("C" if is_consonant(stem, i) else "V" for i in range(len(stem)))
    collapsed = ""
    for ch in pattern:
        if not collapsed or collapsed[-1] != ch:
            collapsed += ch
    return collapsed.count("VC")


def _has_vowel(stem):
    return any(not is_consonant(stem, i) for i in range(len(stem)))


def _ends_double_consonant(w):
    return len(w) >= 2 and w[-1] == w[-2] and is_consonant(w, len(w) - 1)


def _ends_cvc(w):
    if len(w) < 3:
        return False
    n = len(w)
    return (is_consonant(w, n - 3) and not is_consonant(w, n - 2)
            and is_consonant(w, n - 1) and w[-1] not in "wxy")


def step1ab(word):
    w = word
    # Step 1a
    if w.endswith("sses"):
        w = w[:-2]
    elif w.endswith("ies"):
        w = w[:-2]
    elif w.endswith("ss"):
        pass
    elif w.endswith("s"):
        w = w[:-1]
    # Step 1b
    removed = False
    if w.endswith("eed"):
        if measure(w[:-3]) > 0:
            w = w[:-1]
    elif w.endswith("ed") and _has_vowel(w[:-2]):
        w, removed = w[:-2], True
    elif w.endswith("ing") and _has_vowel(w[:-3]):
        w, removed = w[:-3], True
    if removed:
        if w.endswith(("at", "bl", "iz")):
            w = w + "e"
        elif _ends_double_consonant(w) and w[-1] not in "lsz":
            w = w[:-1]
        elif measure(w) == 1 and _ends_cvc(w):
            w = w + "e"
    return w
