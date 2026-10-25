"""Render every AIML Gym pack from the topic modules and the learning path.

    python3 build/build.py            # render all topics (no tests are run)

Each topic module in build/topics/ defines PROBLEMS (a list of dicts). `path.py` fixes the
order; this script assigns IDs from that order, resolves [[slug]] references, and writes
    topics/<topic>/<slug>/{metadata.json,article.md,problem.md,starter.py,solution.py,tests.py}
plus topics/<topic>/overview.md. Run validate.py afterwards to execute the tests, then
reports.py to write the manifest, coverage reports and curriculum.

A step with `"optional": True` is a deep dive: graded as usual but not counted towards topic
completion. A dict with `"kind": "project"` is an ungraded project idea (PROJECT_REQUIRED
fields); it renders only metadata.json and project.md and gets an ID of the form PREFIX-P1.
"""
import ast
import csv
import importlib
import json
import os
import re
import shutil
import sys
import textwrap

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
sys.path.insert(0, BUILD)

from path import PATH, TOPICS  # noqa: E402
from overviews import OVERVIEWS  # noqa: E402
from library_comparisons import LIBRARY  # noqa: E402

REQUIRED = [
    "slug", "title", "difficulty", "prereqs", "objectives", "tags", "packages",
    "sources", "entry", "article", "statement", "starter", "hints", "solution",
    "explanation", "tests", "feedback",
]
PROJECT_REQUIRED = ["slug", "title", "brief", "uses", "milestones", "stretch", "data", "setup"]
DIFFICULTIES = ("beginner", "intermediate", "advanced")
PARTIAL = os.environ.get("AIMLGYM_PARTIAL") == "1"  # development only: skip unwritten steps
REF = re.compile(r"\[\[([a-z0-9-]+)\]\]")
BAD_REF = re.compile(r"\[\[[a-z][a-z0-9]*-[a-z0-9-]+\]\]")

FUNCTION_HEADER = '''"""Tests for {id} {title}.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import importlib
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = importlib.import_module(os.environ.get("AIMLGYM_TARGET", "solution"))
'''

# Programs written before functions are taught run top to bottom. The tests re-run the whole
# file with the given standard input and compare what it prints.
SCRIPT_HEADER = '''"""Tests for {id} {title}.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import contextlib
import importlib
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
TARGET = os.environ.get("AIMLGYM_TARGET", "solution")


def run_program(stdin_text=""):
    """Run the program from the top with stdin_text as its input; return (output, module)."""
    sys.modules.pop(TARGET, None)
    saved_stdin = sys.stdin
    sys.stdin = io.StringIO(stdin_text)
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            module = importlib.import_module(TARGET)
    finally:
        sys.stdin = saved_stdin
    return buffer.getvalue(), module
'''


def dedent(s):
    return textwrap.dedent(s).strip("\n") + "\n"


def load_sources():
    with open(os.path.join(ROOT, "sources.csv"), newline="", encoding="utf-8") as fh:
        return {row["source_id"]: row for row in csv.DictReader(fh)}


def load_path():
    """Return [(topic_tuple, [problem dicts in path order])] with IDs assigned."""
    out, seen_slugs = [], {}
    for topic in TOPICS:
        slug, name, prefix, _, modules, _ = topic
        by_slug = {}
        for modname in modules:
            try:
                mod = importlib.import_module(f"topics.{modname}")
            except ModuleNotFoundError:
                if PARTIAL:
                    continue
                raise
            for p in mod.PROBLEMS:
                if p["slug"] in by_slug or p["slug"] in seen_slugs:
                    raise ValueError(f"duplicate slug {p['slug']}")
                by_slug[p["slug"]] = p
        order = PATH[slug]
        if PARTIAL:
            order = [s for s in order if s in by_slug]
        missing = [s for s in order if s not in by_slug]
        orphans = [s for s in by_slug if s not in order]
        if missing or orphans:
            raise ValueError(f"{slug}: path lists missing problems {missing}; "
                             f"modules define problems not on the path {orphans}")
        problems, steps, projects = [], 0, 0
        for s in order:
            p = dict(by_slug[s])
            if s in LIBRARY:
                if "library" in p:
                    raise ValueError(f"{s} has a library section in two places")
                p["library"] = LIBRARY[s]
            # Project ideas are numbered separately, so adding one never renumbers graded steps.
            if p.get("kind") == "project":
                projects += 1
                p["id"] = f"{prefix}-P{projects}"
            else:
                steps += 1
                p["id"] = f"{prefix}-{steps:02d}"
            p["topic"] = slug
            problems.append(p)
            seen_slugs[s] = p
        out.append((topic, problems))
    unknown = sorted(set(LIBRARY) - set(seen_slugs))
    if unknown and not PARTIAL:
        raise ValueError(f"library comparisons for unknown slugs {unknown}")
    return out, seen_slugs


def resolver(index):
    """Replace [[slug]] with the step ID. Only known slugs are replaced, so nested-list code
    such as [[7]] is left alone; an unknown hyphenated reference is an error."""
    def resolve(text):
        text = REF.sub(lambda m: index[m.group(1)]["id"] if m.group(1) in index else m.group(0), text)
        bad = BAD_REF.findall(text)
        if bad and not PARTIAL:
            raise ValueError(f"unknown references {bad}")
        return text
    return resolve


def walk_strings(obj, fn):
    if isinstance(obj, str):
        return fn(obj)
    if isinstance(obj, list):
        return [walk_strings(x, fn) for x in obj]
    if isinstance(obj, tuple):
        return tuple(walk_strings(x, fn) for x in obj)
    if isinstance(obj, dict):
        return {k: walk_strings(v, fn) for k, v in obj.items()}
    return obj


def test_names(source):
    return [n.name for n in ast.walk(ast.parse(source))
            if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]


def check_project(p, index, position):
    missing = [k for k in PROJECT_REQUIRED if k not in p]
    if missing:
        raise ValueError(f"{p['slug']} missing fields {missing}")
    if not 4 <= len(p["milestones"]) <= 6:
        raise ValueError(f"{p['slug']} must have 4-6 milestones")
    if not p["uses"]:
        raise ValueError(f"{p['slug']} must link the steps it uses")
    for used in p["uses"]:
        if used not in index or index[used].get("kind") == "project":
            raise ValueError(f"{p['slug']} uses unknown step {used}")
        if position[used] >= position[p["slug"]]:
            raise ValueError(f"{p['slug']} uses {used}, which comes later in the path")


def check_problem(p, index, position, sources):
    if p.get("kind") == "project":
        return check_project(p, index, position)
    missing = [k for k in REQUIRED if k not in p]
    if missing:
        raise ValueError(f"{p['slug']} missing fields {missing}")
    if p["difficulty"] not in DIFFICULTIES:
        raise ValueError(f"{p['slug']} difficulty {p['difficulty']}")
    if len(p["hints"]) != 3:
        raise ValueError(f"{p['slug']} must have exactly 3 hints")
    for sid in p["sources"]:
        if sid not in sources:
            raise ValueError(f"{p['slug']} cites unknown source {sid}")
    for pre in p["prereqs"]:
        if PARTIAL and pre not in index:
            continue
        if pre not in index:
            raise ValueError(f"{p['slug']} has unknown prerequisite {pre}")
        if position[pre] >= position[p["slug"]]:
            if PARTIAL:
                print(f"WARNING {p['slug']} prerequisite {pre} is not earlier in the path")
                continue
            raise ValueError(f"{p['slug']} prerequisite {pre} is not earlier in the path")


def check_tables(slug, text):
    """A markdown table must end with a blank line, or the next paragraph is pulled into it."""
    lines, in_code = text.splitlines(), False
    for i, line in enumerate(lines[:-1]):
        if line.startswith("```"):
            in_code = not in_code
        nxt = lines[i + 1]
        if not in_code and line.lstrip().startswith("|") and nxt.strip() and not nxt.lstrip().startswith("|"):
            raise ValueError(f"{slug}: add a blank line after the table before {nxt[:40]!r}")


def render_project(topic, p, index):
    tslug, tname = topic[0], topic[1]
    d = os.path.join(ROOT, "topics", tslug, p["slug"])
    os.makedirs(d, exist_ok=True)
    for name in os.listdir(d):  # a step turned into a project idea keeps no stale files
        if name not in ("metadata.json", "project.md"):
            os.remove(os.path.join(d, name))
    uses = [{"slug": s, "id": index[s]["id"], "title": index[s]["title"]} for s in p["uses"]]
    brief, data, setup = dedent(p["brief"]), dedent(p["data"]), dedent(p["setup"])
    for text in (brief, data, setup):
        check_tables(p["slug"], text)
    project = (
        f"# {p['id']} · Project idea: {p['title']}\n\n**Topic:** {tname} · ungraded\n\n"
        f"## Brief\n\n{brief}\n"
        "## You will use\n\n" + "\n".join(f"- {u['id']} {u['title']}" for u in uses) + "\n\n"
        "## Milestones\n\n" + "\n".join(f"{n}. {m}" for n, m in enumerate(p["milestones"], 1)) + "\n\n"
        "## Stretch goals\n\n" + "\n".join(f"- {g}" for g in p["stretch"]) + "\n\n"
        f"## Data\n\n{data}\n## Run it yourself\n\n{setup}")
    write(d, "project.md", project)
    meta = {
        "id": p["id"], "slug": p["slug"], "title": p["title"], "topic": tslug, "kind": "project",
        "concept_tags": p.get("tags", []), "uses": uses, "brief": brief, "milestones": p["milestones"],
        "stretch": p["stretch"], "data": data, "setup": setup,
    }
    write(d, "metadata.json", json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    return meta


def render_problem(topic, p, index, sources):
    if p.get("kind") == "project":
        return render_project(topic, p, index)
    tslug, tname = topic[0], topic[1]
    d = os.path.join(ROOT, "topics", tslug, p["slug"])
    os.makedirs(d, exist_ok=True)
    if os.path.exists(os.path.join(d, "project.md")):
        os.remove(os.path.join(d, "project.md"))
    lib = p.get("library")

    refs = "\n".join(
        f"- [{sources[s]['title']}]({sources[s]['url']}) — {sources[s]['author_org']} (`{s}`)"
        for s in p["sources"])
    outcomes = "\n".join(f"- {o}" for o in p["objectives"])

    article = dedent(p["article"])
    for text in (article, dedent(p["statement"])):
        check_tables(p["slug"], text)
    lines = article.splitlines()
    if not lines[0].startswith("# "):
        raise ValueError(f"{p['slug']} article must start with an H1")
    article = (lines[0] + "\n\n## Learning outcomes\n\nAfter this lesson you can:\n\n"
               + outcomes + "\n" + "\n".join(lines[1:]).rstrip() + "\n")
    if lib:
        article += "\n## Library implementation\n\n" + dedent(lib["text"])
    article += "\n## References\n\n" + refs + "\n"
    write(d, "article.md", article)

    pre = ", ".join(f"{index[s]['id']} {index[s]['title']}" for s in p["prereqs"] if s in index) or "none"
    hints = "\n".join(
        f"<details><summary>Hint {i + 1}</summary>\n\n{h.strip()}\n\n</details>\n"
        for i, h in enumerate(p["hints"]))
    fb = "\n".join(f"| `{t}` | {a} |" for t, a in p["feedback"])
    packages = ", ".join(p["packages"]) or "standard library only"
    problem = (
        f"# {p['id']} · {p['title']}\n\n"
        f"**Topic:** {tname} · **Difficulty:** {p['difficulty']} · "
        f"**Allowed packages:** {packages}\n\n"
        f"**Builds on:** {pre}\n\n"
        f"Read the lesson first: [article.md](article.md)\n\n"
        f"## Task\n\n{dedent(p['statement'])}\n"
        f"## Hints\n\n{hints}\n"
        f"## If a test fails\n\n| Test | What to check |\n|---|---|\n{fb}\n\n"
        f"## Worked solution\n\nThe reference solution is in `solution.py`. "
        f"Explanation:\n\n{dedent(p['explanation'])}\n"
        f"## References\n\n{refs}\n")
    write(d, "problem.md", problem)

    write(d, "starter.py", dedent(p["starter"]))
    expl = dedent(p["explanation"]).replace('"""', "'''")
    write(d, "solution.py",
          f'r"""Reference solution for {p["id"]} {p["title"]}.\n\n{expl}"""\n' + dedent(p["solution"]))

    header = SCRIPT_HEADER if p.get("kind") == "script" else FUNCTION_HEADER
    tests = dedent(p["tests"])
    if lib and lib.get("tests"):
        tests += "\n\n" + dedent(lib["tests"])
    tests_src = (header.format(id=p["id"], title=p["title"]) + "\n" + p.get("test_prelude", "")
                 + "\n" + tests + '\n\nif __name__ == "__main__":\n    unittest.main()\n')
    write(d, "tests.py", tests_src)

    names = test_names(tests_src)
    if len(names) != len(set(names)):
        raise ValueError(f"{p['slug']} has duplicate test names")
    unknown_fb = [t for t, _ in p["feedback"] if t not in names]
    if unknown_fb:
        raise ValueError(f"{p['slug']} feedback names unknown tests {unknown_fb}")
    if len(names) < 6:
        raise ValueError(f"{p['slug']} has only {len(names)} tests")

    meta = {
        "id": p["id"], "slug": p["slug"], "title": p["title"], "topic": tslug,
        "difficulty": p["difficulty"], "kind": p.get("kind", "function"),
        "optional": bool(p.get("optional")),
        "prerequisites": [index[s]["id"] for s in p["prereqs"] if s in index],
        "prerequisite_slugs": list(p["prereqs"]),
        "learning_objectives": p["objectives"], "concept_tags": p["tags"],
        "permitted_packages": p["packages"],
        "optional_packages": (lib or {}).get("optional", []),
        "library_comparison": bool(lib),
        "source_ids": p["sources"], "entry_point": p["entry"], "hints": p["hints"],
        "failure_feedback": [{"test": t, "advice": a} for t, a in p["feedback"]],
        "test_count": len(names),
    }
    old = os.path.join(d, "metadata.json")
    if os.path.exists(old):
        with open(old, encoding="utf-8") as fh:
            prev = json.load(fh)
        if "validation" in prev:
            meta["validation"] = prev["validation"]
    write(d, "metadata.json", json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    return meta


def write(d, name, text):
    with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
        fh.write(text)


def render_overview(topic, problems, index):
    tslug, tname, prefix, tpre, _, outcome = topic
    pre = ", ".join(t[1] for t in TOPICS if t[0] in tpre) or "none"
    def row(n, p):
        if p.get("kind") == "project":
            return f"| {n} | {p['id']} | [Project idea: {p['title']}]({p['slug']}/project.md) | ungraded | " \
                   f"{', '.join(index[s]['id'] for s in p['uses'])} |"
        title = p["title"] + (" (optional deep dive)" if p.get("optional") else "")
        return f"| {n} | {p['id']} | [{title}]({p['slug']}/problem.md) | {p['difficulty']} | " \
               f"{', '.join(index[s]['id'] for s in p['prereqs'] if s in index) or '—'} |"
    rows = "\n".join(row(n, p) for n, p in enumerate(problems, 1))
    text = (f"# {tname}\n\n**You will be able to:** {outcome}\n\n"
            f"**Topic prerequisites:** {pre}\n\n{resolver(index)(dedent(OVERVIEWS[tslug]))}\n"
            f"## Learning path\n\nWork through the steps in order; each one uses only "
            f"what earlier steps (and the topic prerequisites) taught.\n\n"
            f"| Step | ID | Title | Difficulty | Builds on |\n|---|---|---|---|---|\n{rows}\n")
    write(os.path.join(ROOT, "topics", tslug), "overview.md", text)


def main():
    sources = load_sources()
    path, index = load_path()
    position = {}
    for topic, problems in path:
        for p in problems:
            position[p["slug"]] = len(position)
    resolve = resolver(index)
    metas = []
    for topic, problems in path:
        tdir = os.path.join(ROOT, "topics", topic[0])
        os.makedirs(tdir, exist_ok=True)
        keep = {p["slug"] for p in problems}
        for entry in os.listdir(tdir):
            full = os.path.join(tdir, entry)
            if os.path.isdir(full) and entry not in keep and \
                    os.path.exists(os.path.join(full, "metadata.json")):
                shutil.rmtree(full)
        for p in problems:
            check_problem(p, index, position, sources)
        for p in problems:
            q = walk_strings({k: v for k, v in p.items() if k not in ("id", "slug", "prereqs", "uses")}, resolve)
            q.update(id=p["id"], slug=p["slug"], prereqs=p.get("prereqs", []))
            if "uses" in p:
                q["uses"] = p["uses"]
            metas.append(render_problem(topic, q, index, sources))
        render_overview(topic, problems, index)
    projects = sum(m["kind"] == "project" for m in metas)
    print(f"rendered {len(metas) - projects} packs and {projects} project ideas in {len(path)} topics")


if __name__ == "__main__":
    main()
