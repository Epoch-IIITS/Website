# Cleaning Text Columns

## Learning outcomes

After this lesson you can:

- Use the .str accessor
- Normalise whitespace and case with regex
- Extract parts of strings and keep missing values missing

## Intuition
Typed-in data is messy: "  Ann   LEE ", "ann lee", "+91 98-765 43210". Before you can join or
count, normalise it. The `.str` accessor applies string methods to a whole column at once.

## Precise explanation
* `s.str.strip()`, `s.str.lower()`, `s.str.title()`.
* Regex replace: `s.str.replace(r"\s+", " ", regex=True)` collapses runs of whitespace;
  `s.str.replace(r"\D", "", regex=True)` removes every non-digit.
* `s.str.split("@").str[1]` takes the part after "@" (NaN if absent).
* `s.str.contains("@", na=False)` for validity checks.
* Missing values stay missing through `.str` methods (they return NaN/NA rather than raising).

## Worked example
"  Ann   LEE " → strip → "Ann   LEE" → collapse → "Ann LEE" → title → "Ann Lee".
"+91 98-765 43210" → digits "919876543210".

## Common mistakes
* Calling Python string methods on the Series itself (`s.lower()` → AttributeError).
* Forgetting `regex=True` for patterns.
* Converting NaN to the string "nan" with `astype(str)`.

## Why this matters
Text normalisation precedes deduplication, joining on names, and NLP tokenisation (NL-02).

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
