"""NLP step added in the 2026-10 revision: regular expressions, taught before the tokeniser
that depends on them."""

PROBLEMS = [
# ---------------------------------------------------------------- regex-text
{
"slug": "regex-text", "title": "Regular Expressions for Text",
"difficulty": "beginner", "prereqs": ["unique-words"], "packages": [],
"objectives": ["Write patterns with character classes, quantifiers and anchors",
               "Use re.findall, re.sub and re.fullmatch",
               "Capture parts of a match with named groups",
               "Compare a regex with the equivalent character loop"],
"tags": ["regex", "pattern-matching", "text-cleaning", "parsing"],
"sources": ["S059", "S060"], "entry": "collapse_spaces_manual(text); collapse_spaces(text); mask_digits(text); find_numbers(text); find_hashtags(text); parse_log(line)",
"article": r'''
# Regular Expressions for Text

## Intuition
A regular expression (regex) is a tiny language for describing text patterns: "one or more
digits", "a word starting with #", "a date like 2026-10-24". Python's `re` module searches,
extracts and replaces such patterns, replacing many lines of character-by-character loops.

## Precise explanation
Always write patterns as **raw strings** (`r"..."`) so backslashes reach `re` unchanged.

| Pattern | Matches |
|---|---|
| `a`, `cat` | those exact characters |
| `.` | any character except newline |
| `[abc]`, `[a-z0-9]`, `[^0-9]` | one character from a set / not from a set |
| `\d`, `\w`, `\s` | digit, word character (letter, digit, `_`), whitespace |
| `\D`, `\W`, `\S` | the opposites |
| `x*`, `x+`, `x?`, `x{2,4}` | 0+, 1+, 0 or 1, 2–4 repetitions of `x` |
| `^`, `$`, `\b` | start, end, word boundary |
| `(...)`, `(?P<name>...)`, `(?:...)` | capturing group, named group, non-capturing group |
| `a|b` | either |

* `re.findall(p, s)` → list of all matches (or of group values if the pattern has one group).
* `re.sub(p, repl, s)` → replace every match.
* `re.fullmatch(p, s)` → a match object only if the **whole** string matches, else `None`;
  `m.group("name")` reads a named group.
* Quantifiers are **greedy** (take as much as possible); add `?` (`.*?`) for the shortest match.

## Worked example
```python
re.sub(r"\s+", " ", "a   b\t\nc")              # 'a b c'
re.findall(r"-?\d+(?:\.\d+)?", "x=-3.5, y=2")   # ['-3.5', '2']
m = re.fullmatch(r"(?P<y>\d{4})-(?P<m>\d\d)", "2026-10")
m.group("y")                                  # '2026'
```

## Common mistakes
* Forgetting the `r` prefix: `"\b"` is a backspace character, `r"\b"` is a word boundary.
* Using `re.match` (anchored only at the start) when you meant `re.fullmatch`.
* A group inside a `findall` pattern changes what is returned; use `(?:...)` when you only need
  grouping.
* Writing one giant pattern instead of several small, tested ones.

## Why this matters
Tokenisers ([[tokenize-normalize]]), log parsers, data cleaning and parsing model output
([[parse-tool-call]]) all use regular expressions.
''',
"statement": r'''
Implement:

1. `collapse_spaces_manual(text)` — replace every run of whitespace with one space and strip both
   ends, **without** `re` (hint: `str.split` and `str.join`).
2. `collapse_spaces(text)` — the same with `re.sub`.
3. `mask_digits(text)` — replace every digit with `#`.
4. `find_numbers(text)` — list of numbers (as `float`) that appear in the text: an optional `-`,
   digits, and an optional decimal part such as `.5`.
5. `find_hashtags(text)` — list of hashtags without `#`, lowercased: `#` followed by one or more
   letters, digits or underscores, preceded by start-of-text or a non-word character.
6. `parse_log(line)` — for lines like `"2026-10-24 12:00:01 ERROR Disk full"`, return
   `{"date": ..., "time": ..., "level": ..., "message": ...}`; `level` is one of `DEBUG`, `INFO`,
   `WARNING`, `ERROR`. Return `None` if the whole line does not match.
''',
"starter": r'''
import re


def collapse_spaces_manual(text):
    # TODO: no re here
    return text


def collapse_spaces(text):
    # TODO
    return text


def mask_digits(text):
    # TODO
    return text


def find_numbers(text):
    # TODO
    return []


def find_hashtags(text):
    # TODO
    return []


LOG = re.compile(r"TODO")


def parse_log(line):
    # TODO: use LOG.fullmatch and named groups
    return None
''',
"hints": [
    "`\" \".join(text.split())` collapses whitespace without regex; with regex use `re.sub(r\"\\s+\", \" \", text).strip()`.",
    "Numbers: `r\"-?\\d+(?:\\.\\d+)?\"`; hashtags: `r\"(?<!\\w)#(\\w+)\"` (a negative look-behind for 'not preceded by a word character').",
    "Log: `r\"(?P<date>\\d{4}-\\d{2}-\\d{2}) (?P<time>\\d{2}:\\d{2}:\\d{2}) (?P<level>DEBUG|INFO|WARNING|ERROR) (?P<message>.+)\"`; return `m.groupdict()`.",
],
"solution": r'''
import re


def collapse_spaces_manual(text):
    return " ".join(text.split())


def collapse_spaces(text):
    return re.sub(r"\s+", " ", text).strip()


def mask_digits(text):
    return re.sub(r"\d", "#", text)


def find_numbers(text):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", text)]


def find_hashtags(text):
    return [tag.lower() for tag in re.findall(r"(?<!\w)#(\w+)", text)]


LOG = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) "
    r"(?P<level>DEBUG|INFO|WARNING|ERROR) (?P<message>.+)"
)


def parse_log(line):
    m = LOG.fullmatch(line)
    return m.groupdict() if m else None
''',
"explanation": r'''
Splitting on whitespace and re-joining is the loop-free manual equivalent of `\s+` → space. The
number pattern makes the sign and decimal part optional with a non-capturing group so `findall`
returns whole matches. A look-behind stops `email#tag` from counting as a hashtag. The compiled
log pattern with named groups turns a valid line into a dict in one call and `fullmatch` rejects
anything else.
''',
"tests": r'''
import re


class TestRegex(unittest.TestCase):
    def test_collapse_manual_matches_regex(self):
        for text in ["a   b\t\nc", "  lead and trail  ", "", "one"]:
            self.assertEqual(S.collapse_spaces_manual(text), S.collapse_spaces(text))
        self.assertEqual(S.collapse_spaces("a   b\t\nc "), "a b c")

    def test_mask_digits(self):
        self.assertEqual(S.mask_digits("Call 555-0199 at 9am"), "Call ###-#### at #am")

    def test_find_numbers(self):
        self.assertEqual(S.find_numbers("x=-3.5, y=2, z=10.25 and 7."), [-3.5, 2.0, 10.25, 7.0])
        self.assertEqual(S.find_numbers("no numbers"), [])

    def test_hashtags(self):
        self.assertEqual(S.find_hashtags("#AI rocks #ml_2026! email#notatag (#NLP)"), ["ai", "ml_2026", "nlp"])

    def test_parse_log(self):
        self.assertEqual(S.parse_log("2026-10-24 12:00:01 ERROR Disk full"),
                         {"date": "2026-10-24", "time": "12:00:01", "level": "ERROR", "message": "Disk full"})

    def test_parse_log_rejects(self):
        self.assertIsNone(S.parse_log("2026-10-24 12:00:01 FATAL Disk full"))
        self.assertIsNone(S.parse_log("garbage 2026-10-24 12:00:01 INFO x"))
        self.assertIsNone(S.parse_log("2026-10-24 12:00 INFO short time"))

    def test_message_keeps_spaces(self):
        out = S.parse_log("2026-01-02 03:04:05 INFO user  ada   logged in")
        self.assertEqual(out["message"], "user  ada   logged in")
''',
"feedback": [
    ("test_collapse_manual_matches_regex", "`\" \".join(text.split())` without regex; `re.sub(r\"\\s+\", \" \", text).strip()` with it."),
    ("test_find_numbers", "Use a non-capturing group for the decimal part so findall returns whole numbers."),
    ("test_hashtags", "Require that `#` is not preceded by a word character, and lowercase the result."),
    ("test_parse_log_rejects", "Use `fullmatch` so the whole line must match, and list only the four levels."),
    ("test_message_keeps_spaces", "The message group should be `.+` and must not be cleaned."),
],
},
]
