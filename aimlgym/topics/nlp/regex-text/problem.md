# NL-01 · Regular Expressions for Text

**Topic:** Natural Language Processing · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** PY-16 Unique Words in Order

Read the lesson first: [article.md](article.md)

## Task

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

## Hints

<details><summary>Hint 1</summary>

`" ".join(text.split())` collapses whitespace without regex; with regex use `re.sub(r"\s+", " ", text).strip()`.

</details>

<details><summary>Hint 2</summary>

Numbers: `r"-?\d+(?:\.\d+)?"`; hashtags: `r"(?<!\w)#(\w+)"` (a negative look-behind for 'not preceded by a word character').

</details>

<details><summary>Hint 3</summary>

Log: `r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>DEBUG|INFO|WARNING|ERROR) (?P<message>.+)"`; return `m.groupdict()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_collapse_manual_matches_regex` | `" ".join(text.split())` without regex; `re.sub(r"\s+", " ", text).strip()` with it. |
| `test_find_numbers` | Use a non-capturing group for the decimal part so findall returns whole numbers. |
| `test_hashtags` | Require that `#` is not preceded by a word character, and lowercase the result. |
| `test_parse_log_rejects` | Use `fullmatch` so the whole line must match, and list only the four levels. |
| `test_message_keeps_spaces` | The message group should be `.+` and must not be cleaned. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Splitting on whitespace and re-joining is the loop-free manual equivalent of `\s+` → space. The
number pattern makes the sign and decimal part optional with a non-capturing group so `findall`
returns whole matches. A look-behind stops `email#tag` from counting as a hashtag. The compiled
log pattern with named groups turns a valid line into a dict in one call and `fullmatch` rejects
anything else.

## References

- [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) — Python Software Foundation (A.M. Kuchling) (`S059`)
- [re — Regular expression operations](https://docs.python.org/3/library/re.html) — Python Software Foundation (`S060`)
