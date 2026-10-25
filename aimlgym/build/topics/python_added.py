"""Python steps added in the 2026-10 revision: modules, functions as values, files and JSON,
classes, inheritance and unit testing."""

PROBLEMS = [
# ---------------------------------------------------------------- standard-library
{
"slug": "standard-library", "title": "Importing the Standard Library",
"difficulty": "intermediate", "prereqs": ["fibonacci-sequence"], "packages": [],
"objectives": ["Import modules with import, from ... import and as",
               "Use math, random, collections, heapq and itertools for common tasks",
               "Make random results reproducible with random.Random(seed)",
               "Explain what each library function replaces"],
"tags": ["modules", "import", "math", "random", "collections", "heapq", "itertools"],
"sources": ["S045", "S047", "S050", "S051", "S052", "S053", "S004"],
"entry": "hypotenuse(a, b); pages_needed(items, per_page); most_common_letter(text); dice_rolls(seed, n); smallest_k(nums, k); all_pairs(items)",
"article": r'''
# Importing the Standard Library

## Intuition
Python ships with a large **standard library**: modules of tested code for maths, randomness,
counting, queues and combinations. Importing a module is like taking a toolbox off the shelf.
You already know how to write many of these tools as loops; now you can choose the shorter,
well-tested version and know what it does for you.

## Precise explanation
```python
import math                       # use as math.sqrt(...)
from collections import Counter   # use the name directly: Counter(...)
import itertools as it            # an alias: it.combinations(...)
```
* `import` runs the module once and binds its name. `dir(math)` lists what it contains and
  `help(math.ceil)` shows documentation.
* Avoid `from math import *`: it hides where names come from.

| Module / function | What it gives you | The loop it replaces |
|---|---|---|
| `math.sqrt`, `math.hypot`, `math.ceil`, `math.pi` | exact, fast numeric functions | `x ** 0.5`, `-(-a // b)` |
| `random.Random(seed)` | an independent random generator with its own seed | — |
| `collections.Counter(text)` | counts of each item; `.most_common()` | a dict of counts ([[vowel-counter]]) |
| `collections.defaultdict(list)` | a dict that creates missing values | `d.setdefault(k, [])` |
| `collections.deque` | a queue with fast `append` and `popleft` | `list.pop(0)` (slow) |
| `heapq.nsmallest(k, nums)` | the k smallest items without sorting everything | `sorted(nums)[:k]` |
| `itertools.combinations(items, 2)` | every unordered pair, in order | two nested `for` loops |

**Reproducible randomness.** `rng = random.Random(42)` creates a generator; calling
`rng.random()` gives floats in `[0, 1)` and the sequence is the same every time for the same seed.
Python documents that `random()` output is reproducible across versions; other methods such as
`randint` may change between versions, so graded tasks build integers from `random()`:
`int(rng.random() * 6) + 1` is a die roll from 1 to 6.

## Worked example
```python
from collections import Counter
Counter("banana").most_common(1)      # [('a', 3)]
import heapq
heapq.nsmallest(2, [5, 1, 4, 1])      # [1, 1]
import itertools
list(itertools.combinations("abc", 2))  # [('a','b'), ('a','c'), ('b','c')]
```

## Common mistakes
* Naming your own file `random.py` or `math.py`: `import random` then imports *your* file.
* Using the global `random.random()` in code that must be reproducible; create `Random(seed)`.
* Expecting `Counter.most_common` to break ties alphabetically — it keeps first-seen order, so
  sort yourself when ties must be deterministic.
* Forgetting that `itertools.combinations` returns an iterator; wrap it in `list(...)`.

## Why this matters
Later topics use `collections.Counter` for word counts, `deque` for breadth-first search,
`heapq` for planners and top-k results, and `itertools` for Shapley value subsets.
''',
"statement": r'''
Implement six small functions, each using the named module:

1. `hypotenuse(a, b)` → length of the hypotenuse, using `math.hypot` (or `math.sqrt`).
2. `pages_needed(items, per_page)` → how many pages are needed to show `items` items,
   using `math.ceil`. `pages_needed(0, 10) == 0`.
3. `most_common_letter(text)` → the most frequent **letter** (case-insensitive, ignore
   non-letters, use `collections.Counter`); break ties by alphabetical order; return `None` if
   there are no letters.
4. `dice_rolls(seed, n)` → a list of `n` die rolls from `rng = random.Random(seed)`, each
   `int(rng.random() * 6) + 1`.
5. `smallest_k(nums, k)` → the `k` smallest numbers in ascending order, using `heapq.nsmallest`.
6. `all_pairs(items)` → a list of all unordered pairs (as tuples) in input order, using
   `itertools.combinations`.

**Examples**
```python
hypotenuse(3, 4)                 # 5.0
pages_needed(21, 10)             # 3
most_common_letter("Hello, World")  # 'l'
smallest_k([5, 1, 4, 1], 2)      # [1, 1]
all_pairs(["a", "b", "c"])       # [('a', 'b'), ('a', 'c'), ('b', 'c')]
```
''',
"starter": r'''
import math
import random
from collections import Counter
import heapq
import itertools


def hypotenuse(a, b):
    return math.sqrt(a * a + b * b)


def pages_needed(items, per_page):
    # TODO: use math.ceil
    return 0


def most_common_letter(text):
    # TODO: count letters with Counter; break ties alphabetically; None if no letters
    return None


def dice_rolls(seed, n):
    # TODO: rng = random.Random(seed); build n rolls with int(rng.random() * 6) + 1
    return []


def smallest_k(nums, k):
    # TODO: heapq.nsmallest
    return []


def all_pairs(items):
    # TODO: itertools.combinations
    return []
''',
"hints": [
    "`math.ceil(items / per_page)` rounds up; `Counter(ch for ch in text.lower() if ch.isalpha())` counts letters.",
    "For ties, find the highest count, then return `min` of the letters that have it.",
    "`[int(rng.random() * 6) + 1 for _ in range(n)]`, `heapq.nsmallest(k, nums)`, `list(itertools.combinations(items, 2))`.",
],
"solution": r'''
import math
import random
from collections import Counter
import heapq
import itertools


def hypotenuse(a, b):
    return math.hypot(a, b)


def pages_needed(items, per_page):
    return math.ceil(items / per_page)


def most_common_letter(text):
    counts = Counter(ch for ch in text.lower() if ch.isalpha())
    if not counts:
        return None
    best = max(counts.values())
    return min(ch for ch, c in counts.items() if c == best)


def dice_rolls(seed, n):
    rng = random.Random(seed)
    return [int(rng.random() * 6) + 1 for _ in range(n)]


def smallest_k(nums, k):
    return heapq.nsmallest(k, nums)


def all_pairs(items):
    return list(itertools.combinations(items, 2))
''',
"explanation": r'''
Each function delegates the core work to a standard-library tool: `math.hypot` and `math.ceil`
for numerics, `Counter` for counting (with an explicit alphabetical tie-break, which
`most_common` does not provide), a seeded `random.Random` for reproducible rolls, `heapq` for a
partial sort and `itertools.combinations` for pairs.
''',
"tests": r'''
import heapq
import itertools
import random


class TestStandardLibrary(unittest.TestCase):
    def test_hypotenuse(self):
        self.assertAlmostEqual(S.hypotenuse(3, 4), 5.0)
        self.assertAlmostEqual(S.hypotenuse(1, 1), math.sqrt(2))

    def test_pages_needed(self):
        self.assertEqual(S.pages_needed(21, 10), 3)
        self.assertEqual(S.pages_needed(20, 10), 2)
        self.assertEqual(S.pages_needed(0, 10), 0)
        self.assertEqual(S.pages_needed(1, 10), 1)

    def test_most_common_letter(self):
        self.assertEqual(S.most_common_letter("Hello, World"), "l")

    def test_most_common_tie_and_case(self):
        self.assertEqual(S.most_common_letter("bBaA!"), "a")
        self.assertIsNone(S.most_common_letter("123 !?"))

    def test_dice_reproducible(self):
        rng = random.Random(7)
        expected = [int(rng.random() * 6) + 1 for _ in range(20)]
        self.assertEqual(S.dice_rolls(7, 20), expected)
        self.assertEqual(S.dice_rolls(7, 20), S.dice_rolls(7, 20))

    def test_dice_range(self):
        rolls = S.dice_rolls(1, 600)
        self.assertEqual(len(rolls), 600)
        self.assertEqual(set(rolls), {1, 2, 3, 4, 5, 6})

    def test_smallest_k(self):
        self.assertEqual(S.smallest_k([5, 1, 4, 1], 2), [1, 1])
        nums = [9, 3, 7, 3, 8, 1]
        self.assertEqual(S.smallest_k(nums, 3), sorted(nums)[:3])

    def test_all_pairs(self):
        self.assertEqual(S.all_pairs(["a", "b", "c"]), [("a", "b"), ("a", "c"), ("b", "c")])
        self.assertEqual(S.all_pairs([1]), [])
        self.assertEqual(len(S.all_pairs(list(range(6)))), 15)
''',
"feedback": [
    ("test_pages_needed", "Use `math.ceil(items / per_page)`; integer `//` rounds down."),
    ("test_most_common_tie_and_case", "Lowercase first, keep only `ch.isalpha()`, break ties with `min`, and return None when nothing is left."),
    ("test_dice_reproducible", "Create `random.Random(seed)` inside the function and use only `rng.random()`."),
    ("test_smallest_k", "`heapq.nsmallest(k, nums)` already returns ascending order."),
    ("test_all_pairs", "Convert the combinations iterator to a list of tuples."),
],
},
# ---------------------------------------------------------------- functions-as-values
{
"slug": "functions-as-values", "title": "Functions as Values",
"difficulty": "intermediate", "prereqs": ["unique-words"], "packages": [],
"objectives": ["Pass functions as arguments and return them from functions",
               "Write lambda expressions and sort with key=",
               "Accept *args, **kwargs and keyword-only parameters",
               "Write a simple decorator with functools.wraps"],
"tags": ["higher-order-functions", "lambda", "args-kwargs", "decorators", "closures"],
"sources": ["S042", "S048", "S001"],
"entry": "pipeline(*funcs); sort_words(words); format_record(name, *scores, sep=', ', **extra); count_calls(func)",
"article": r'''
# Functions as Values

## Intuition
In Python a function is a value like a number or a list. You can store it in a variable, pass
it to another function ("sort these words *using this rule*"), or build a new function from old
ones. This is how sorting keys, callbacks, tool registries and decorators work.

## Precise explanation
**Passing and returning functions**
```python
def apply_twice(f, x):
    return f(f(x))

def make_adder(n):
    def add(x):          # a nested function "remembers" n: a closure
        return x + n
    return add

apply_twice(make_adder(3), 10)   # 16
```
**lambda** creates a small unnamed function from one expression:
`square = lambda x: x * x`. It is most useful as a `key`:
`sorted(words, key=lambda w: (len(w), w))` sorts by length, then alphabetically.

**Flexible parameters**
```python
def report(name, *scores, sep=", ", **extra):
    # scores is a tuple of extra positional arguments
    # sep is keyword-only because it comes after *scores
    # extra is a dict of extra keyword arguments
```
`report("ada", 90, 85, sep="/", club="ai")` → `scores == (90, 85)`,
`extra == {"club": "ai"}`. Calling with `*list` or `**dict` unpacks them into arguments.

**Decorators** wrap a function to add behaviour. `@count_calls` above `def f` means
`f = count_calls(f)`.
```python
import functools

def count_calls(func):
    @functools.wraps(func)        # keep func's name and docstring
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper
```

## Worked example
`pipeline(str.strip, str.lower)("  Hi ")` applies `strip` then `lower` → `"hi"`.

## Common mistakes
* Calling instead of passing: `sorted(words, key=len())` is an error; pass `len`.
* Mutable default arguments: `def f(x, seen=[])` shares one list across calls.
* Forgetting to `return` the wrapper (or the wrapped function's result) in a decorator.
* Putting a keyword-only parameter before `*args` and expecting it to collect a positional value.

## Why this matters
`key=` functions sort model results, callbacks drive training loops, and agent tool registries
([[tool-registry]]) register Python functions with a decorator and call them with `**arguments`.
''',
"statement": r'''
Implement:

1. `pipeline(*funcs)` → returns a new function `run(x)` that applies each function in `funcs` in
   order and returns the final value. With no functions, `run(x)` returns `x`.
2. `sort_words(words)` → a new list sorted by length, then alphabetically (use `sorted` with a
   `lambda` key).
3. `format_record(name, *scores, sep=", ", **extra)` → a string:
   `"<name>: <scores joined by sep>"`, followed — if `extra` is not empty — by `" | "` and the
   extra items as `key=value`, sorted by key and joined by `", "`.
   With no scores the part after the colon is empty: `"ada: "`.
4. `count_calls(func)` → a decorator. The returned wrapper calls `func` with the same
   arguments, returns its result, has an attribute `calls` counting how many times it was
   called, and keeps `func`'s `__name__` (use `functools.wraps`).

**Examples**
```python
pipeline(str.strip, str.upper)("  hi ")             # 'HI'
sort_words(["pear", "fig", "apple", "kiwi"])        # ['fig', 'kiwi', 'pear', 'apple']
format_record("ada", 90, 85)                       # 'ada: 90, 85'
format_record("bob", 70, sep="/", year=2, club="ai")  # 'bob: 70 | club=ai, year=2'
```
''',
"starter": r'''
import functools


def pipeline(*funcs):
    def run(x):
        # TODO: apply each function in order
        return x
    return run


def sort_words(words):
    # TODO: sorted with key=lambda ...
    return list(words)


def format_record(name, *scores, sep=", ", **extra):
    # TODO
    return name


def count_calls(func):
    # TODO: return a wrapper with a .calls counter
    return func
''',
"hints": [
    "Inside `run`, loop `for f in funcs: x = f(x)`, then return x.",
    "`key=lambda w: (len(w), w)`; build the score text with `sep.join(str(s) for s in scores)`.",
    "For extras: `\", \".join(f\"{k}={v}\" for k, v in sorted(extra.items()))`. For the decorator, copy the pattern from the lesson.",
],
"solution": r'''
import functools


def pipeline(*funcs):
    def run(x):
        for f in funcs:
            x = f(x)
        return x
    return run


def sort_words(words):
    return sorted(words, key=lambda w: (len(w), w))


def format_record(name, *scores, sep=", ", **extra):
    text = f"{name}: " + sep.join(str(s) for s in scores)
    if extra:
        text += " | " + ", ".join(f"{k}={v}" for k, v in sorted(extra.items()))
    return text


def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper
''',
"explanation": r'''
`pipeline` returns a closure that remembers `funcs`. The sort key is a tuple, so ties in length
fall back to alphabetical order. `format_record` treats `*scores` as a tuple and `**extra` as a
dict, sorting the latter so the output is deterministic. The decorator stores its counter on the
wrapper itself and forwards every argument with `*args, **kwargs`.
''',
"tests": r'''
class TestFunctionsAsValues(unittest.TestCase):
    def test_pipeline_order(self):
        self.assertEqual(S.pipeline(str.strip, str.upper)("  hi "), "HI")
        self.assertEqual(S.pipeline(lambda x: x + 1, lambda x: x * 10)(2), 30)

    def test_pipeline_empty(self):
        self.assertEqual(S.pipeline()(5), 5)

    def test_sort_words(self):
        self.assertEqual(S.sort_words(["pear", "fig", "apple", "kiwi"]), ["fig", "kiwi", "pear", "apple"])
        data = ["b", "a"]
        S.sort_words(data)
        self.assertEqual(data, ["b", "a"])

    def test_format_scores(self):
        self.assertEqual(S.format_record("ada", 90, 85), "ada: 90, 85")
        self.assertEqual(S.format_record("ada"), "ada: ")

    def test_format_extra_sorted(self):
        self.assertEqual(S.format_record("bob", 70, sep="/", year=2, club="ai"), "bob: 70 | club=ai, year=2")
        self.assertEqual(S.format_record("cy", 1, 2, sep="-"), "cy: 1-2")

    def test_count_calls(self):
        @S.count_calls
        def add(a, b=0):
            return a + b
        self.assertEqual(add.calls, 0)
        self.assertEqual(add(2, b=3), 5)
        add(1)
        self.assertEqual(add.calls, 2)

    def test_wraps_keeps_name(self):
        @S.count_calls
        def greet():
            """Say hi."""
            return "hi"
        self.assertEqual(greet.__name__, "greet")
        self.assertEqual(greet.__doc__, "Say hi.")
''',
"feedback": [
    ("test_pipeline_order", "Apply the functions left to right, feeding each result into the next."),
    ("test_sort_words", "Use `sorted` (it returns a new list) with a tuple key `(len(w), w)`."),
    ("test_format_extra_sorted", "Sort `extra.items()` by key and join scores with the given `sep`."),
    ("test_count_calls", "Initialise `wrapper.calls = 0` and increment it inside the wrapper; return func's result."),
    ("test_wraps_keeps_name", "Decorate the wrapper with `@functools.wraps(func)`."),
],
},
# ---------------------------------------------------------------- files-and-json
{
"slug": "files-and-json", "title": "Files, CSV and JSON",
"difficulty": "advanced", "prereqs": ["guessing-game-feedback"], "packages": [],
"objectives": ["Read and write text files safely with with open(...)",
               "Build paths with pathlib.Path", "Read CSV rows with csv.DictReader",
               "Save and load structured data with json"],
"tags": ["files", "with", "pathlib", "csv", "json"],
"sources": ["S041", "S054", "S055", "S056"],
"entry": "write_lines(path, lines); read_lines(path); load_scores_csv(path); save_json(path, data); load_json(path); summarize_scores(csv_path, json_path)",
"article": r'''
# Files, CSV and JSON

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
([[parse-tool-call]]) exchange tool calls as JSON.
''',
"statement": r'''
Implement:

1. `write_lines(path, lines)` — write each string in `lines` followed by `"\n"` (UTF-8, replacing
   any existing file); return the number of lines written.
2. `read_lines(path)` — return the file's lines without their trailing newline.
3. `load_scores_csv(path)` — the CSV has a header `name,score`; return a list of
   `(name, score)` tuples with `score` converted to `int`, in file order.
4. `save_json(path, data)` — write `data` as JSON with `indent=2` and `sort_keys=True`.
5. `load_json(path)` — read JSON back.
6. `summarize_scores(csv_path, json_path)` — load the CSV, save a JSON summary
   `{"count": n, "mean": <mean rounded to 2 decimals or None>, "top": <name with the highest
   score, earliest in the file on ties, or None>}` to `json_path`, and return the summary dict.

Paths may be `str` or `pathlib.Path` objects.
''',
"starter": r'''
import csv
import json
from pathlib import Path


def write_lines(path, lines):
    # TODO
    return 0


def read_lines(path):
    # TODO
    return []


def load_scores_csv(path):
    # TODO: csv.DictReader; convert score to int
    return []


def save_json(path, data):
    # TODO: json.dump with indent=2, sort_keys=True
    pass


def load_json(path):
    # TODO
    return None


def summarize_scores(csv_path, json_path):
    # TODO
    return {}
''',
"hints": [
    "`with open(path, \"w\", encoding=\"utf-8\") as fh:` then `fh.write(line + \"\\n\")` in a loop.",
    "`fh.read().splitlines()` drops newlines; open CSV files with `newline=\"\"` and use `csv.DictReader(fh)`.",
    "For `top`, keep the first maximum: loop and update only when `score > best_score`.",
],
"solution": r'''
import csv
import json
from pathlib import Path


def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as fh:
        for line in lines:
            fh.write(line + "\n")
    return len(lines)


def read_lines(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read().splitlines()


def load_scores_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return [(row["name"], int(row["score"])) for row in csv.DictReader(fh)]


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def summarize_scores(csv_path, json_path):
    rows = load_scores_csv(csv_path)
    top, best = None, None
    for name, score in rows:
        if best is None or score > best:
            top, best = name, score
    mean = round(sum(s for _, s in rows) / len(rows), 2) if rows else None
    summary = {"count": len(rows), "mean": mean, "top": top}
    save_json(Path(json_path), summary)
    return summary
''',
"explanation": r'''
Every file is opened in a `with` block with an explicit encoding. CSV parsing is delegated to
`csv.DictReader`, which handles quoting, and scores are converted to `int` immediately. The
summary reuses the loaders, handles the empty file explicitly and keeps the first maximum by using
a strict `>` comparison.
''',
"tests": r'''
import json
import tempfile
from pathlib import Path


class TestFiles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_csv(self, text):
        p = self.dir / "scores.csv"
        p.write_text(text, encoding="utf-8")
        return p

    def test_write_and_read_lines(self):
        p = self.dir / "notes.txt"
        self.assertEqual(S.write_lines(p, ["alpha", "beta"]), 2)
        self.assertEqual(p.read_text(encoding="utf-8"), "alpha\nbeta\n")
        self.assertEqual(S.read_lines(p), ["alpha", "beta"])

    def test_write_replaces(self):
        p = self.dir / "notes.txt"
        S.write_lines(str(p), ["old", "old"])
        S.write_lines(str(p), ["new"])
        self.assertEqual(S.read_lines(str(p)), ["new"])

    def test_load_scores_csv(self):
        p = self.write_csv('name,score\nada,91\n"Lovelace, Ada",88\n')
        self.assertEqual(S.load_scores_csv(p), [("ada", 91), ("Lovelace, Ada", 88)])

    def test_json_roundtrip(self):
        p = self.dir / "data.json"
        data = {"b": [1, 2], "a": {"x": None, "y": True}}
        S.save_json(p, data)
        self.assertEqual(S.load_json(p), data)
        self.assertEqual(p.read_text(encoding="utf-8"), json.dumps(data, indent=2, sort_keys=True))

    def test_summary(self):
        p = self.write_csv("name,score\nada,90\nbob,95\ncy,95\n")
        out = self.dir / "summary.json"
        expected = {"count": 3, "mean": 93.33, "top": "bob"}
        self.assertEqual(S.summarize_scores(p, out), expected)
        self.assertEqual(json.loads(out.read_text(encoding="utf-8")), expected)

    def test_summary_empty(self):
        p = self.write_csv("name,score\n")
        out = self.dir / "summary.json"
        self.assertEqual(S.summarize_scores(p, out), {"count": 0, "mean": None, "top": None})

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            S.read_lines(self.dir / "missing.txt")
''',
"feedback": [
    ("test_write_and_read_lines", "Write `line + \"\\n\"` for each line and read with `splitlines()`."),
    ("test_write_replaces", "Open with mode `\"w\"`, which replaces the file, not `\"a\"`."),
    ("test_load_scores_csv", "Use `csv.DictReader` (it handles the quoted comma) and convert scores with `int`."),
    ("test_json_roundtrip", "Pass `indent=2, sort_keys=True` to `json.dump`."),
    ("test_summary", "Round the mean to 2 decimals and keep the first name with the highest score."),
    ("test_summary_empty", "With no rows, mean and top are None."),
],
},
# ---------------------------------------------------------------- bank-account
{
"slug": "bank-account", "title": "Classes: A Bank Account",
"difficulty": "advanced", "prereqs": ["text-stats-stdin"], "packages": [],
"objectives": ["Define a class with __init__, attributes and methods",
               "Protect an object's state by validating in methods",
               "Distinguish class attributes from instance attributes",
               "Give objects a readable __repr__"],
"tags": ["classes", "objects", "methods", "state", "repr"],
"sources": ["S046", "S044"], "entry": "class BankAccount(owner, balance=0)",
"article": r'''
# Classes and Objects

## Intuition
A class is a blueprint; an object is one thing built from it. Every bank account has an owner
and a balance (its **state**) and supports deposit and withdraw (its **behaviour**). A class
keeps the data and the functions that change it together, so the balance can only change in
ways the class allows.

## Precise explanation
```python
class Counter:
    step = 1                          # class attribute: shared by all counters

    def __init__(self, start=0):      # runs when you write Counter(...)
        self.value = start            # instance attribute: one per object

    def increment(self):              # a method; self is the object it is called on
        self.value += self.step
        return self.value

    def __repr__(self):               # what the object looks like when printed
        return f"Counter(value={self.value})"

c = Counter(5)
c.increment()      # 6;  same as Counter.increment(c)
```
* `self` is just the first parameter: the object the method was called on.
* Attributes set on `self` in `__init__` exist for every object.
* Methods validate input and raise exceptions ([[factorial-validated]]) rather than letting
  the object reach an invalid state.
* Objects are passed by reference: two names can refer to the same object.

## Worked example
```python
acct = BankAccount("Ada", 100)
acct.deposit(50)        # balance 150
acct.withdraw(30)       # balance 120
acct.history            # [('deposit', 50), ('withdraw', 30)]
acct                    # BankAccount(owner='Ada', balance=120)
```

## Common mistakes
* Forgetting `self` in a method definition, or writing `balance` instead of `self.balance`.
* Putting a mutable list as a *class* attribute (`history = []`), shared by every account —
  create it in `__init__`.
* Updating state before validating, so a failed withdrawal still changes the balance.
* Calling `BankAccount.deposit(50)` on the class instead of on an object.

## Why this matters
Later topics use classes everywhere: scikit-learn-style models with `fit`/`predict`
([[ml-baselines]]), optimisers that keep momentum ([[sgd-momentum]]), environments with
`reset`/`step` ([[env-interface]]) and agent tool registries.
''',
"statement": r'''
Write `class BankAccount`:

* `BankAccount(owner, balance=0)` stores `owner` and `balance`; raise `ValueError` if the
  starting balance is negative. Each account has its own `history` list, initially empty.
* Class attribute `interest_rate = 0.02`.
* `deposit(amount)` — `amount` must be positive (else `ValueError`); adds it, appends
  `("deposit", amount)` to `history`, returns the new balance.
* `withdraw(amount)` — `amount` must be positive and at most the balance (else `ValueError`,
  and nothing changes); subtracts it, appends `("withdraw", amount)`, returns the new balance.
* `transfer_to(other, amount)` — withdraws from this account and deposits into `other`
  (if the withdrawal fails, `other` must not change).
* `apply_interest()` — adds `round(balance * interest_rate, 2)` as a deposit and returns the new
  balance (record it in history like a deposit).
* `__repr__` returns e.g. `BankAccount(owner='Ada', balance=120)` (use `{self.owner!r}`).
''',
"starter": r'''
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        # TODO: validate, update, record, return
        self.balance += amount
        return self.balance

    # TODO: withdraw, transfer_to, apply_interest, __repr__ and the class attribute
''',
"hints": [
    "Create `self.history = []` in `__init__` and check the start balance there.",
    "In `withdraw`, raise before changing anything: `if amount <= 0 or amount > self.balance: raise ValueError(...)`.",
    "`transfer_to` can call `self.withdraw(amount)` then `other.deposit(amount)`; `!r` in an f-string adds quotes.",
],
"solution": r'''
class BankAccount:
    interest_rate = 0.02

    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("starting balance cannot be negative")
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount
        self.history.append(("deposit", amount))
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self.history.append(("withdraw", amount))
        return self.balance

    def transfer_to(self, other, amount):
        self.withdraw(amount)
        other.deposit(amount)

    def apply_interest(self):
        return self.deposit(round(self.balance * self.interest_rate, 2))

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance})"
''',
"explanation": r'''
All validation happens before any attribute changes, so a failed call leaves the object as it
was. `history` is created per object in `__init__`. `transfer_to` reuses `withdraw` and
`deposit`, so their checks apply and the withdrawal's exception stops the deposit. Interest is
looked up through `self`, which finds the class attribute.
''',
"tests": r'''
class TestBankAccount(unittest.TestCase):
    def test_init_and_repr(self):
        a = S.BankAccount("Ada", 100)
        self.assertEqual((a.owner, a.balance, a.history), ("Ada", 100, []))
        self.assertEqual(repr(a), "BankAccount(owner='Ada', balance=100)")
        self.assertEqual(S.BankAccount("Bo").balance, 0)

    def test_negative_start(self):
        with self.assertRaises(ValueError):
            S.BankAccount("X", -1)

    def test_deposit_withdraw(self):
        a = S.BankAccount("Ada", 100)
        self.assertEqual(a.deposit(50), 150)
        self.assertEqual(a.withdraw(30), 120)
        self.assertEqual(a.history, [("deposit", 50), ("withdraw", 30)])

    def test_invalid_amounts_change_nothing(self):
        a = S.BankAccount("Ada", 10)
        for bad in (lambda: a.deposit(0), lambda: a.deposit(-5),
                    lambda: a.withdraw(-1), lambda: a.withdraw(11)):
            with self.assertRaises(ValueError):
                bad()
        self.assertEqual((a.balance, a.history), (10, []))

    def test_separate_histories(self):
        a, b = S.BankAccount("A"), S.BankAccount("B")
        a.deposit(5)
        self.assertEqual(b.history, [])

    def test_transfer(self):
        a, b = S.BankAccount("A", 50), S.BankAccount("B", 5)
        a.transfer_to(b, 20)
        self.assertEqual((a.balance, b.balance), (30, 25))
        with self.assertRaises(ValueError):
            a.transfer_to(b, 100)
        self.assertEqual((a.balance, b.balance), (30, 25))

    def test_interest(self):
        self.assertEqual(S.BankAccount.interest_rate, 0.02)
        a = S.BankAccount("A", 1000)
        self.assertEqual(a.apply_interest(), 1020)
        self.assertEqual(a.history[-1], ("deposit", 20.0))
''',
"feedback": [
    ("test_init_and_repr", "Create `self.history = []` in `__init__` and format `__repr__` with `{self.owner!r}`."),
    ("test_invalid_amounts_change_nothing", "Raise ValueError before modifying balance or history."),
    ("test_separate_histories", "Do not make `history` a class attribute; create it in `__init__`."),
    ("test_transfer", "Withdraw first; if it raises, the deposit never happens."),
    ("test_interest", "Define `interest_rate = 0.02` in the class body and deposit the rounded interest."),
],
},
# ---------------------------------------------------------------- shapes-inheritance
{
"slug": "shapes-inheritance", "title": "Inheritance, Special Methods and Dataclasses",
"difficulty": "advanced", "prereqs": ["bank-account"], "packages": [],
"objectives": ["Create subclasses that reuse and override base-class methods",
               "Call the parent initialiser with super()",
               "Implement special methods such as __eq__ and __lt__",
               "Generate boilerplate with @dataclass"],
"tags": ["inheritance", "polymorphism", "super", "dunder-methods", "dataclasses"],
"sources": ["S046", "S057"], "entry": "Shape, Rectangle(width, height), Square(side), Circle(radius), total_area(shapes), Point(x, y)",
"article": r'''
# Inheritance, Special Methods and Dataclasses

## Intuition
Rectangles, squares and circles are all shapes: they all have an area and can describe
themselves. **Inheritance** lets you write the shared parts once in a base class and only the
differences in each subclass. A square is a rectangle with equal sides, so `Square` can inherit
almost everything from `Rectangle`.

## Precise explanation
```python
class Shape:
    name = "shape"
    def area(self):
        raise NotImplementedError("subclasses must implement area")
    def describe(self):                       # shared code, uses self.area()
        return f"{self.name} with area {self.area():.2f}"

class Rectangle(Shape):                       # Rectangle inherits from Shape
    name = "rectangle"
    def __init__(self, width, height):
        self.width, self.height = width, height
    def area(self):                           # overrides Shape.area
        return self.width * self.height

class Square(Rectangle):
    name = "square"
    def __init__(self, side):
        super().__init__(side, side)          # reuse the parent's initialiser
```
* Method lookup goes object → class → parent → ... (`Square` → `Rectangle` → `Shape`).
* `isinstance(Square(2), Rectangle)` is `True`. Code that calls `shape.area()` works for any
  subclass — this is **polymorphism**.
* **Special ("dunder") methods** customise operators: `__eq__` for `==`, `__lt__` for `<` (which
  makes `sorted` work), `__repr__` for display, `__add__` for `+`.
* `@dataclass` (from `dataclasses`) writes `__init__`, `__repr__` and `__eq__` from annotated
  fields:
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
Point(1, 2) == Point(1, 2)    # True; repr: Point(x=1, y=2)
```
`x: float` is a **type annotation**: documentation for readers and tools; Python does not convert
or check the value. (Pydantic, in [[pydantic-bodies]], does check.)

## Worked example
`[Square(2), Circle(1)]` → `describe()` gives `"square with area 4.00"` and
`"circle with area 3.14"`; `sorted` with `__lt__` comparing areas puts the circle first.

## Common mistakes
* Forgetting `super().__init__(...)`, so parent attributes are never set.
* Defining `__eq__` but comparing different types; return `NotImplemented` for unknown types.
* Deep inheritance trees: prefer a shallow hierarchy and small classes.

## Why this matters
Deep-learning frameworks are built on inheritance (every layer subclasses a base `Module`), and
FastAPI request models subclass Pydantic's `BaseModel`.
''',
"statement": r'''
Implement:

* `Shape` with class attribute `name = "shape"`, `area()` raising `NotImplementedError`,
  `describe()` returning `f"{self.name} with area {self.area():.2f}"`, `__eq__` (shapes are equal
  when both are `Shape` objects and their areas differ by less than `1e-9`; otherwise return
  `NotImplemented`) and `__lt__` (compare areas).
* `Rectangle(width, height)` (`name = "rectangle"`), with `area()` and `perimeter()`.
* `Square(side)` (`name = "square"`) — a subclass of `Rectangle` that calls `super().__init__`.
* `Circle(radius)` (`name = "circle"`) using `math.pi`; `perimeter()` is the circumference.
* `total_area(shapes)` — sum of areas.
* `@dataclass class Point` with fields `x` and `y` and a method `distance_to(other)`.

**Examples**
```python
Square(2).describe()            # 'square with area 4.00'
Rectangle(1, 4) == Square(2)    # True — same area
sorted([Square(2), Circle(1)])  # [Circle(1), Square(2)] by area
Point(0, 0).distance_to(Point(3, 4))   # 5.0
```
''',
"starter": r'''
import math
from dataclasses import dataclass


class Shape:
    name = "shape"

    def area(self):
        raise NotImplementedError("subclasses must implement area")

    def describe(self):
        return f"{self.name} with area {self.area():.2f}"


class Rectangle(Shape):
    name = "rectangle"

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# TODO: Shape.__eq__ / __lt__, Rectangle.perimeter, Square, Circle, total_area, Point
''',
"hints": [
    "`class Square(Rectangle):` with `def __init__(self, side): super().__init__(side, side)`.",
    "In `__eq__`, start with `if not isinstance(other, Shape): return NotImplemented`.",
    "`@dataclass` above `class Point:` with `x: float` and `y: float`; use `math.hypot` for the distance.",
],
"solution": r'''
import math
from dataclasses import dataclass


class Shape:
    name = "shape"

    def area(self):
        raise NotImplementedError("subclasses must implement area")

    def describe(self):
        return f"{self.name} with area {self.area():.2f}"

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        return abs(self.area() - other.area()) < 1e-9

    def __lt__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() < other.area()


class Rectangle(Shape):
    name = "rectangle"

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Square(Rectangle):
    name = "square"

    def __init__(self, side):
        super().__init__(side, side)


class Circle(Shape):
    name = "circle"

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius


def total_area(shapes):
    return sum(s.area() for s in shapes)


@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)
''',
"explanation": r'''
`Shape` holds behaviour shared by every shape and defines comparison in terms of `area()`, which
each subclass overrides. `Square` only changes how it is constructed and its name. Returning
`NotImplemented` lets Python report a proper error for unsupported comparisons. The dataclass
generates the initialiser, representation and equality for `Point`.
''',
"tests": r'''
class TestShapes(unittest.TestCase):
    def test_rectangle(self):
        r = S.Rectangle(2, 3)
        self.assertEqual((r.area(), r.perimeter()), (6, 10))
        self.assertEqual(r.describe(), "rectangle with area 6.00")

    def test_square_inherits(self):
        sq = S.Square(2)
        self.assertIsInstance(sq, S.Rectangle)
        self.assertIsInstance(sq, S.Shape)
        self.assertEqual((sq.width, sq.height, sq.perimeter()), (2, 2, 8))
        self.assertEqual(sq.describe(), "square with area 4.00")

    def test_circle(self):
        c = S.Circle(1)
        self.assertAlmostEqual(c.area(), math.pi)
        self.assertAlmostEqual(c.perimeter(), 2 * math.pi)
        self.assertEqual(c.describe(), "circle with area 3.14")

    def test_base_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            S.Shape().area()

    def test_equality_and_sorting(self):
        self.assertEqual(S.Rectangle(1, 4), S.Square(2))
        self.assertNotEqual(S.Square(1), S.Square(2))
        self.assertFalse(S.Square(1) == "square")
        shapes = sorted([S.Square(2), S.Circle(1), S.Rectangle(1, 1)])
        self.assertEqual([s.name for s in shapes], ["rectangle", "circle", "square"])

    def test_total_area(self):
        self.assertAlmostEqual(S.total_area([S.Square(1), S.Rectangle(2, 5)]), 11)
        self.assertEqual(S.total_area([]), 0)

    def test_point_dataclass(self):
        self.assertEqual(S.Point(1, 2), S.Point(1, 2))
        self.assertEqual(repr(S.Point(1, 2)), "Point(x=1, y=2)")
        self.assertAlmostEqual(S.Point(0, 0).distance_to(S.Point(3, 4)), 5.0)
''',
"feedback": [
    ("test_square_inherits", "Subclass `Rectangle` and call `super().__init__(side, side)`; set `name = \"square\"`."),
    ("test_circle", "Use `math.pi * r ** 2` for the area and `2 * math.pi * r` for the perimeter."),
    ("test_equality_and_sorting", "Define `__eq__` and `__lt__` on `Shape` using areas; return `NotImplemented` for non-shapes."),
    ("test_point_dataclass", "Decorate `Point` with `@dataclass` and declare `x: float` and `y: float`."),
    ("test_total_area", "Sum `s.area()` over the shapes; an empty list gives 0."),
],
},
# ---------------------------------------------------------------- unit-testing
{
"slug": "unit-testing", "title": "Writing Unit Tests",
"difficulty": "advanced", "prereqs": ["shapes-inheritance"], "packages": [],
"objectives": ["Write unittest.TestCase classes with assertEqual and assertRaises",
               "Choose test cases that cover normal, edge and error behaviour",
               "Explain how tests catch bugs, using deliberately broken versions (mutants)",
               "Know when to replace slow or external dependencies with fakes or mocks"],
"tags": ["testing", "unittest", "edge-cases", "mutation-testing", "mocks"],
"sources": ["S002", "S064"], "entry": "class SlugifyTests(unittest.TestCase)",
"article": r'''
# Writing Unit Tests

## Intuition
Every exercise so far was checked by tests someone else wrote. A **unit test** is a small
program that calls your code with chosen inputs and checks the outputs. Good tests are like a
safety net: when you change code later, they tell you immediately if you broke something.

## Precise explanation
```python
import unittest

def add(a, b):
    return a + b

class AddTests(unittest.TestCase):
    def test_small_numbers(self):            # methods starting with test_ are tests
        self.assertEqual(add(2, 3), 5)

    def test_floats(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            add(1, "x")
```
Run with `python -m unittest -v`. Useful assertions: `assertEqual`, `assertTrue`, `assertIn`,
`assertIsNone`, `assertAlmostEqual` (floats), `assertRaises`. `setUp(self)` runs before every
test.

**What to test**
* The normal case from the specification.
* **Edge cases**: empty input, one element, boundaries, repeated or unusual characters.
* **Error cases**: inputs that must raise.
* One idea per test, with a descriptive name, so a failure tells you what broke.

**How good are my tests?** Make a deliberately broken copy of the code — a **mutant** (for
example, forget to lowercase). If every test still passes, the tests missed that bug. This
exercise grades your tests exactly this way.

**Fakes and mocks.** Code that calls a web service, a clock or a language model is tested by
replacing that dependency with a predictable stand-in: a small fake function or class, or
`unittest.mock.Mock` / `patch`. Later topics use scripted models ([[react-loop]]) and fake
services ([[fastapi-dependencies]]) this way, so tests never need the network.

## Worked example
For `slugify("  Hello, World!  ")` → `"hello-world"`, good tests include:
`"ABC" → "abc"` (case), `"a b" → "a-b"` (spaces), `"a, b" → "a-b"` (punctuation runs collapse),
`"--a--" → "a"` (no leading/trailing dashes), `"" → ""` (empty), `"r2d2" → "r2d2"` (digits kept).

## Common mistakes
* Testing only the example from the statement.
* Asserting on `print` output instead of return values.
* Tests that depend on each other's order or on shared mutable state.
* Asserting floats with `assertEqual` instead of `assertAlmostEqual`.

## Why this matters
Every pack in this curriculum is graded by unit tests, and the FastAPI topic ends with
[[api-testing]], where you test a web API the same way.
''',
"statement": r'''
The starter contains a correct `slugify(text)`:

* lowercase ASCII letters and digits are kept;
* every run of other characters becomes a single `-`;
* there are no leading or trailing dashes; an input with no letters or digits gives `""`.

Write `class SlugifyTests(unittest.TestCase)` with **at least five** test methods. Every test
must call the function as `self.slugify(...)` (the grader swaps in other versions through that
attribute).

Your tests are graded by running them against:
* the correct `slugify` — all your tests must pass;
* six broken versions (mutants) — for each one, at least one of your tests must fail.

The mutants: (1) does not lowercase, (2) does not collapse runs of separators, (3) does not strip
leading/trailing dashes, (4) treats digits as separators, (5) only replaces spaces (keeps
punctuation), (6) crashes on an empty string.
''',
"starter": r'''
import unittest


def slugify(text):
    """Return a URL-friendly slug: 'Hello, World!' -> 'hello-world'."""
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


class SlugifyTests(unittest.TestCase):
    slugify = staticmethod(slugify)

    def test_example(self):
        self.assertEqual(self.slugify("Hello World"), "hello-world")

    # TODO: add tests for case, punctuation runs, leading/trailing separators,
    #       digits and the empty string
''',
"hints": [
    "Each mutant breaks one rule; write one test per rule from the statement.",
    "Examples: `\"ABC\"`→`\"abc\"`, `\"a,  b\"`→`\"a-b\"`, `\"--a--\"`→`\"a\"`, `\"r2d2\"`→`\"r2d2\"`.",
    "Include `self.assertEqual(self.slugify(\"\"), \"\")` and a punctuation case such as `\"a!b\"`→`\"a-b\"`.",
],
"solution": r'''
import unittest


def slugify(text):
    """Return a URL-friendly slug: 'Hello, World!' -> 'hello-world'."""
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


class SlugifyTests(unittest.TestCase):
    slugify = staticmethod(slugify)

    def test_example(self):
        self.assertEqual(self.slugify("Hello World"), "hello-world")

    def test_lowercases(self):
        self.assertEqual(self.slugify("ABC"), "abc")

    def test_punctuation_becomes_dash(self):
        self.assertEqual(self.slugify("a!b"), "a-b")

    def test_runs_collapse(self):
        self.assertEqual(self.slugify("a,  b"), "a-b")

    def test_no_leading_or_trailing_dash(self):
        self.assertEqual(self.slugify("  --a--  "), "a")

    def test_digits_kept(self):
        self.assertEqual(self.slugify("R2D2 v10"), "r2d2-v10")

    def test_empty(self):
        self.assertEqual(self.slugify(""), "")
        self.assertEqual(self.slugify("!!!"), "")
''',
"explanation": r'''
Each test targets one rule of the specification, so each mutant — which breaks exactly one
rule — fails at least one test, while the correct implementation passes them all. The empty
and punctuation-only inputs cover the edge cases that crash naive implementations.
''',
"tests": r'''
def correct(text):
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def no_lower(text):
    out = []
    for ch in text:
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def no_collapse(text):
    return "".join(ch if ch.isascii() and ch.isalnum() else "-" for ch in text.lower()).strip("-")


def no_strip(text):
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalnum():
            out.append(ch)
        elif not out or out[-1] != "-":
            out.append("-")
    return "".join(out)


def digits_split(text):
    out = []
    for ch in text.lower():
        if ch.isascii() and ch.isalpha():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def spaces_only(text):
    words = text.lower().split()
    return "-".join(words)


def crashes_on_empty(text):
    if text[0] == "":
        return ""
    return correct(text)


def run_learner_tests(impl):
    probe = type("Probe", (S.SlugifyTests,), {"slugify": staticmethod(impl)})
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(probe)
    result = unittest.TestResult()
    suite.run(result)
    return result


class TestYourTests(unittest.TestCase):
    def test_at_least_five_tests(self):
        names = unittest.defaultTestLoader.getTestCaseNames(S.SlugifyTests)
        self.assertGreaterEqual(len(names), 5)

    def test_pass_on_correct_version(self):
        result = run_learner_tests(correct)
        self.assertTrue(result.wasSuccessful(), result.failures + result.errors)

    def test_catches_missing_lowercase(self):
        self.assertFalse(run_learner_tests(no_lower).wasSuccessful())

    def test_catches_missing_collapse(self):
        self.assertFalse(run_learner_tests(no_collapse).wasSuccessful())

    def test_catches_missing_strip(self):
        self.assertFalse(run_learner_tests(no_strip).wasSuccessful())

    def test_catches_digit_bug(self):
        self.assertFalse(run_learner_tests(digits_split).wasSuccessful())

    def test_catches_punctuation_bug(self):
        self.assertFalse(run_learner_tests(spaces_only).wasSuccessful())

    def test_catches_empty_crash(self):
        self.assertFalse(run_learner_tests(crashes_on_empty).wasSuccessful())
''',
"feedback": [
    ("test_at_least_five_tests", "Add more `test_...` methods to `SlugifyTests`."),
    ("test_pass_on_correct_version", "One of your expected values is wrong: check it against the rules in the statement."),
    ("test_catches_missing_lowercase", "Add a test with upper-case input."),
    ("test_catches_missing_collapse", "Add a test with two or more separators in a row, e.g. `\"a,  b\"`."),
    ("test_catches_missing_strip", "Add a test whose input starts or ends with punctuation or spaces."),
    ("test_catches_digit_bug", "Add a test containing digits, which must be kept."),
    ("test_catches_punctuation_bug", "Add a test with punctuation between letters, such as `\"a!b\"`."),
    ("test_catches_empty_crash", "Add a test for the empty string."),
],
},
]
