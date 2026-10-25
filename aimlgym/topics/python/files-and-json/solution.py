r"""Reference solution for PY-23 Files, CSV and JSON.

Every file is opened in a `with` block with an explicit encoding. CSV parsing is delegated to
`csv.DictReader`, which handles quoting, and scores are converted to `int` immediately. The
summary reuses the loaders, handles the empty file explicitly and keeps the first maximum by using
a strict `>` comparison.
"""
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
