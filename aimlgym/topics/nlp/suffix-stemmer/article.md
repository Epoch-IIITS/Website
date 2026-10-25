# The Porter Stemmer (Steps 1a–1b)

## Learning outcomes

After this lesson you can:

- Implement Porter's consonant/vowel definition and measure m
- Apply Porter Step 1a and Step 1b rules in order
- Understand why naive suffix stripping fails

## Intuition
"connected", "connecting" and "connection" share a stem. Naively chopping "ing"/"ed" turns "sing"
into "s" and "bled" into "bl". The Porter stemmer (Porter, 1980) uses ordered rules with
conditions that look at the *shape* of the remaining stem.

## Precise explanation
**Consonants:** a letter other than a, e, i, o, u, and other than *y preceded by a consonant*. So
"y" in "toy" is a consonant (preceded by vowel o); in "syzygy" the middle y's are vowels.
Writing consonant runs as C and vowel runs as V, every word is $[C](VC)^m[V]$; $m$ is the
**measure**: tree → m = 0, trouble → 1, oaten → 2.

Conditions: `*v*` = stem contains a vowel; `*d` = ends in a double consonant; `*o` = ends
consonant-vowel-consonant where the last consonant is not w, x or y.

**Step 1a** (first matching suffix): SSES→SS, IES→I, SS→SS, S→"".
**Step 1b** (first matching suffix; a rule whose condition fails stops the step):
* (m > 0) EED → EE
* (*v*) ED → ""
* (*v*) ING → ""
If ED or ING was removed, tidy up: AT→ATE, BL→BLE, IZ→IZE; else if *d and not ending in l, s or
z → drop the last letter; else if m = 1 and *o → add E.

## Worked examples (from Porter's paper)
caresses→caress, ponies→poni, cats→cat, feed→feed, agreed→agree, plastered→plaster, bled→bled,
motoring→motor, sing→sing, conflated→conflate, hopping→hop, falling→fall, filing→file.

## Common mistakes
* Applying ED/ING without checking the remaining stem has a vowel ("bled" → "bl").
* Trying ED after an EED rule matched but failed its condition (feed must stay feed).
* Wrong y handling in the consonant test.

## Why this matters
Stemming reduces vocabulary size for search and classic text classification; implementing the
rules teaches careful, condition-driven string processing.

## References

- [Natural Language Processing with Python (NLTK Book)](https://www.nltk.org/book/) — Steven Bird, Ewan Klein, Edward Loper (`S018`)
- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
