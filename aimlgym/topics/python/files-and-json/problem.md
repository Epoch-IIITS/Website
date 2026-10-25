# PY-23 · Files, CSV and JSON

**Topic:** Python · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** PY-22 Guessing Game Feedback

Read the lesson first: [article.md](article.md)

## Task

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

## Hints

<details><summary>Hint 1</summary>

`with open(path, "w", encoding="utf-8") as fh:` then `fh.write(line + "\n")` in a loop.

</details>

<details><summary>Hint 2</summary>

`fh.read().splitlines()` drops newlines; open CSV files with `newline=""` and use `csv.DictReader(fh)`.

</details>

<details><summary>Hint 3</summary>

For `top`, keep the first maximum: loop and update only when `score > best_score`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_write_and_read_lines` | Write `line + "\n"` for each line and read with `splitlines()`. |
| `test_write_replaces` | Open with mode `"w"`, which replaces the file, not `"a"`. |
| `test_load_scores_csv` | Use `csv.DictReader` (it handles the quoted comma) and convert scores with `int`. |
| `test_json_roundtrip` | Pass `indent=2, sort_keys=True` to `json.dump`. |
| `test_summary` | Round the mean to 2 decimals and keep the first name with the highest score. |
| `test_summary_empty` | With no rows, mean and top are None. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Every file is opened in a `with` block with an explicit encoding. CSV parsing is delegated to
`csv.DictReader`, which handles quoting, and scores are converted to `int` immediately. The
summary reuses the loaders, handles the empty file explicitly and keeps the first maximum by using
a strict `>` comparison.

## References

- [The Python Tutorial: Input and Output](https://docs.python.org/3/tutorial/inputoutput.html) — Python Software Foundation (`S041`)
- [json — JSON encoder and decoder](https://docs.python.org/3/library/json.html) — Python Software Foundation (`S054`)
- [csv — CSV file reading and writing](https://docs.python.org/3/library/csv.html) — Python Software Foundation (`S055`)
- [pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html) — Python Software Foundation (`S056`)
