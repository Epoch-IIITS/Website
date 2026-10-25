# Files, CSV and JSON

## Learning outcomes

After this lesson you can:

- Read and write text files safely with with open(...)
- Build paths with pathlib.Path
- Read CSV rows with csv.DictReader
- Save and load structured data with json

## Intuition
Variables disappear when a program ends; files persist. A text file is a string stored on disk.
**CSV** stores a table as lines of comma-separated values, and **JSON** stores nested
dictionaries and lists as text — the format web APIs and configuration files use.

## Precise explanation
**Opening files**
```python
with open(path, "w", encoding="utf-8") as fh:   # "w" replaces, "a" appends, "r" reads
    fh.write("first line\n")
with open(path, encoding="utf-8") as fh:
    text = fh.read()                 # or: for line in fh: ...
```
`with` closes the file even if an error happens. Always give `encoding="utf-8"` so results do
not depend on the computer. `write` does not add newlines for you. Opening a missing file for
reading raises `FileNotFoundError`.

**Paths**: `from pathlib import Path`; `Path(folder) / "scores.csv"` joins parts correctly on
every operating system; `path.exists()`, `path.read_text(encoding="utf-8")`.

**CSV** (`import csv`): open with `newline=""` as the documentation requires, then
```python
for row in csv.DictReader(fh):   # each row is a dict keyed by the header line
    row["score"]                 # always a string: convert it yourself
```
The csv module handles quoted fields such as `"Lovelace, Ada"` that a plain `split(",")` breaks.

**JSON** (`import json`): `json.dump(data, fh, indent=2, sort_keys=True)` writes;
`json.load(fh)` reads. JSON has objects (dicts with string keys), arrays (lists), strings,
numbers, `true`/`false` and `null` (`None`). Tuples become lists and integer dict keys become
strings.

## Worked example
```python
rows = [{"name": "ada", "score": "91"}]          # what DictReader gives you
scores = {r["name"]: int(r["score"]) for r in rows}
json.dumps(scores)                                # '{"ada": 91}'
```

## Common mistakes
* Forgetting `"\n"` when writing lines, producing one long line.
* Reading CSV numbers and forgetting they are strings (`"9" > "10"` is True).
* Opening with `"w"` when you meant `"a"` and erasing the file.
* Splitting CSV lines by hand and breaking on commas inside quotes.

## Why this matters
Datasets arrive as CSV files, model settings and API messages are JSON, and agents
(AG-02) exchange tool calls as JSON.

## References

- [The Python Tutorial: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html) — Python Software Foundation (`S041`)
- [json — JSON encoder and decoder](https://docs.python.org/3/library/json.html) — Python Software Foundation (`S054`)
- [csv — CSV file reading and writing](https://docs.python.org/3/library/csv.html) — Python Software Foundation (`S055`)
- [pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html) — Python Software Foundation (`S056`)
