# Normalisation and Tokenisation

## Learning outcomes

After this lesson you can:

- Normalise Unicode text (case, accents)
- Tokenise with a regular expression
- Keep contractions and numbers as single tokens

## Intuition
Computers see "Café", "cafe" and "CAFÉ" as three different strings. Before counting words we
normalise text and split it into **tokens** — the units a model will count or embed.

## Precise explanation
**Normalisation** (one common recipe):
1. `unicodedata.normalize("NFKD", s)` decomposes "é" into "e" + a combining accent mark.
2. Drop combining marks (`unicodedata.combining(ch)` is non-zero for them).
3. Lowercase.
This is a design choice: it helps search in English but destroys meaning in languages where
accents matter.

**Tokenisation with a regex:** `re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text)` returns runs of letters
and digits, optionally followed by an apostrophe part ("don't", "it's"). Everything else
(spaces, punctuation) separates tokens.

Real tokenisers (NLTK, spaCy, subword BPE in LM-06) make many more decisions; the point is that
tokenisation is a modelling choice with consequences.

## Worked example
"Café's menu: 2 croissants, NO coffee!" → normalise → "cafe's menu: 2 croissants, no coffee!" →
tokens [cafe's, menu, 2, croissants, no, coffee].

## Common mistakes
* `text.split()` keeps punctuation attached ("coffee!").
* Forgetting to normalise before tokenising, so accented letters are dropped by `[a-z]`.
* Using `\w`, which also matches underscores and non-Latin letters (sometimes desired, sometimes not).

## Why this matters
Every later NLP and LLM exercise starts from tokens; inconsistent tokenisation between training
and inference silently hurts models.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Natural Language Processing with Python (NLTK Book)](https://www.nltk.org/book/) — Steven Bird, Ewan Klein, Edward Loper (`S018`)
