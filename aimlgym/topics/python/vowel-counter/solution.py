r"""Reference solution for PY-13 Vowel Counter.

Pre-filling the dictionary guarantees all five keys appear even when a vowel is absent. Lowering
the text once makes the comparison case-insensitive. Membership in a dict is an O(1) lookup, so
the whole function is a single linear pass.
"""
def count_vowels(text):
    counts = {v: 0 for v in "aeiou"}
    for ch in text.lower():
        if ch in counts:
            counts[ch] += 1
    return sum(counts.values()), counts
