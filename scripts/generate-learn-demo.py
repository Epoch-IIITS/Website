"""Build self-contained, typed UI fixtures from the attached learning packs."""

import csv
import ast
import textwrap
import importlib.util
import unittest
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "aimlgym"
OUTPUT = ROOT / "lib" / "learn"


def load_path():
    """Topic order, step order and outcomes come from the curriculum's single path file."""
    spec = importlib.util.spec_from_file_location("aimlgym_path", SOURCE / "build" / "path.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    topics = [(slug, title, prefix, prerequisites, outcome) for slug, title, prefix, prerequisites, _, outcome in module.TOPICS]
    return topics, module.PATH


TOPICS, PATH = load_path()

# Packages Pyodide 0.27.7 ships, by pack package name; the worker maps opencv-python-headless
# to Pyodide's opencv-python. Packs that need anything else (FastAPI, PyTorch, LangChain,
# LangGraph, Gymnasium) run on the VPS.
LOCAL_PACKAGES = {"numpy", "pandas", "scipy", "scikit-learn", "opencv-python", "opencv-python-headless"}
# Modules the in-browser (Pyodide) harness can import for visible tests.
LOCAL_MODULES = {"importlib", "math", "os", "sys", "unittest", "numpy", "pandas", "random", "statistics", "warnings",
                 "io", "contextlib", "copy", "json", "string", "collections", "itertools", "functools", "heapq",
                 "fractions", "re", "datetime", "unicodedata", "tempfile", "pathlib", "csv", "types",
                 "scipy", "sklearn", "cv2"}
# Lines the test header adds before the learner-specific helpers; they are rebuilt by the harness.
HEADER_NAMES = {"S", "TARGET", "run_program"}


def section(text, start, end=None):
    match = re.search(r"(?m)^## " + re.escape(start) + r"\s*$", text)
    if not match:
        return ""
    body = text[match.start():]
    if end:
        finish = re.search(r"(?m)^## " + re.escape(end) + r"\s*$", body)
        if finish:
            body = body[:finish.start()]
    return body.strip()


def visible_tests(text):
    matches = list(re.finditer(r"(?m)^    def (test_\w+)\(self\):", text))
    tests = []
    for match in matches[:3]:
        rest = text[match.end():]
        stop = re.search(r"(?m)^    (?:def |@)|^class |^if __name__", rest)
        body = rest[:stop.start() if stop else None]
        lines = [line[8:] if line.startswith("        ") else line for line in body.rstrip().splitlines()]
        tests.append({"name": match.group(1), "code": "\n".join(lines[:18]).strip()})
    return tests


def class_helpers(tests_source, visible):
    """Group the visible tests by the TestCase class that defines them.

    Returns (groups, helpers): groups[i] is the class index of visible test i, and helpers[g] is the
    dedented source of that class's non-test members (setUp, helper methods, class attributes), which
    the browser harness rebuilds around the visible test bodies.
    """
    tree = ast.parse(tests_source)
    lines = tests_source.splitlines()
    owner = {}
    for cls in (n for n in tree.body if _is_test_case(n)):
        for item in cls.body:
            if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                owner.setdefault(item.name, cls)
    classes, groups = [], []
    for test in visible:
        cls = owner.get(test["name"])
        if cls not in classes:
            classes.append(cls)
        groups.append(classes.index(cls))
    helpers = []
    for cls in classes:
        parts = []
        for item in cls.body if cls is not None else []:
            if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                continue
            if isinstance(item, ast.Expr) and isinstance(item.value, ast.Constant):
                continue
            first = min([item.lineno] + [d.lineno for d in getattr(item, "decorator_list", [])])
            parts.append(textwrap.dedent("\n".join(lines[first - 1:item.end_lineno])))
        helpers.append("\n\n".join(parts))
    return groups, helpers


def _defined_names(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {node.name}
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        return {name.id for target in targets for name in ast.walk(target) if isinstance(name, ast.Name)}
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return {(alias.asname or alias.name).split(".")[0] for alias in node.names}
    return set()


def _loaded_names(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _is_test_case(node):
    return isinstance(node, ast.ClassDef) and any(
        isinstance(base, ast.Attribute) and base.attr == "TestCase" for base in node.bases)


def local_prelude(tests_source, visible, helpers=()):
    """Module-level helpers (functions, constants, imports) that the visible tests use, in source order.

    The standard header (imports, sys.path, S/TARGET/run_program) is excluded because the harness
    provides its own versions; TestCase classes and guarded optional imports are excluded unless used.
    """
    tree = ast.parse(tests_source)
    body = [node for node in tree.body
            if not _is_test_case(node) and not isinstance(node, ast.If)
            and not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant))]
    candidates = [node for node in body if not (_defined_names(node) & HEADER_NAMES) and _defined_names(node)]
    needed = set()
    for code in [test["code"] for test in visible] + [h for h in helpers if h]:
        try:
            needed |= _loaded_names(ast.parse(code))
        except SyntaxError:
            pass
    chosen, changed = set(), True
    while changed:
        changed = False
        for index, node in enumerate(candidates):
            if index not in chosen and _defined_names(node) & needed:
                chosen.add(index)
                needed |= _loaded_names(node)
                changed = True
    nodes = [node for index, node in enumerate(candidates) if index in chosen]
    return "\n\n".join(ast.get_source_segment(tests_source, node) for node in nodes)


def locally_compatible(tests_source, packages, prelude, helpers=()):
    if not set(packages) <= LOCAL_PACKAGES:
        return False
    visible = visible_tests(tests_source)
    if not visible:
        return False
    try:
        snippets = [ast.parse("def case(self):\n" + "\n".join("    " + line for line in test["code"].splitlines())) for test in visible]
        prelude_tree = ast.parse(prelude)
        helper_trees = [ast.parse(h) for h in helpers if h]
    except SyntaxError:
        return False
    # Attributes the rebuilt class provides: its helper methods and anything assigned to self/cls.
    provided = set()
    for tree in helper_trees:
        provided |= {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        provided |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store)
                     and isinstance(n.value, ast.Name) and n.value.id in ("self", "cls")}
        provided |= _defined_names_in(tree)
    for tree in [prelude_tree, *helper_trees, *snippets]:
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports |= {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        if not imports <= LOCAL_MODULES:
            return False
    local_code = prelude + "\n" + "\n".join(test["code"] for test in visible)
    if "subprocess" in local_code or "asyncio" in local_code:
        return False
    defined = set().union(*(_defined_names(node) for node in prelude_tree.body)) | {"S", "run_program", "math", "unittest"}
    module_names = set().union(*(_defined_names(node) for node in ast.parse(tests_source).body))
    for snippet in snippets:
        if any(isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in module_names - defined for node in ast.walk(snippet)):
            return False
        if any(isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self"
               and not hasattr(unittest.TestCase, node.attr) and node.attr not in provided for node in ast.walk(snippet)):
            return False
    return True


def _defined_names_in(tree):
    """Class attributes assigned directly in a helper block (for example `space = ...`)."""
    return set().union(*(_defined_names(n) for n in tree.body if isinstance(n, (ast.Assign, ast.AnnAssign)))) if tree.body else set()


def plain_text(markdown):
    text = re.sub(r"\[\[([a-z0-9-]+)\]\]", r"\1", markdown)
    text = re.sub(r"(?m)^\s*\d+\.\s+", "", text)
    text = text.replace("**", "").replace("`", "")
    return " ".join(text.split())


def main():
    with (SOURCE / "sources.csv").open(newline="") as file:
        sources = {row["source_id"]: {"title": row["title"], "url": row["url"], "author": row["author_org"]} for row in csv.DictReader(file)}
    topics = []
    problems = []
    projects = []
    packs = {}
    project_pages = {}
    executor_tests = {}
    local_compat = {}
    for slug, title, prefix, prerequisites, outcome in TOPICS:
        folder = SOURCE / "topics" / slug
        overview = (folder / "overview.md").read_text()
        intro = overview.split("## Learning path")[0]
        intro = re.sub(r"^# .*\n", "", intro)
        intro = re.sub(r"(?m)^\*\*(You will be able to|Topic prerequisites):\*\*.*$", "", intro)
        intro = plain_text(intro).replace("AIML Gym", "this learning path")
        counts = Counter()
        topic_sources = Counter()
        topic_problems = []
        topic_projects = []
        for pack_slug in PATH[slug]:
            pack_dir = folder / pack_slug
            data = json.loads((pack_dir / "metadata.json").read_text())
            if data["kind"] == "project":
                # Ungraded: shown after the step before it, never sent to the executor or the browser harness.
                record = {"id": data["id"], "slug": data["slug"], "title": data["title"], "topicSlug": slug,
                          "after": topic_problems[-1]["slug"] if topic_problems else None, "tags": data["concept_tags"]}
                topic_projects.append(record)
                project_pages[data["slug"]] = {
                    **record, "uses": data["uses"], "brief": data["brief"], "milestones": data["milestones"],
                    "stretch": data["stretch"], "data": data["data"], "setup": data["setup"],
                }
                continue
            statement = (pack_dir / "problem.md").read_text()
            article = (pack_dir / "article.md").read_text()
            # The app shows learning outcomes in a dialog, so drop the lesson's own outcomes section.
            article = re.sub(r"(?ms)^## Learning outcomes\n.*?(?=^## )", "", article)
            source_ids = data["source_ids"]
            for source_id in source_ids:
                topic_sources[source_id] += 1
            counts[data["difficulty"]] += 1
            record = {
                "id": data["id"], "slug": data["slug"], "title": data["title"],
                "topicSlug": slug, "difficulty": data["difficulty"],
                "prerequisites": data["prerequisites"],
                "tags": data["concept_tags"], "entryPoint": data["entry_point"],
                "testCount": data["test_count"], "kind": data.get("kind", "function"),
                "optional": data.get("optional", False),
            }
            topic_problems.append(record)
            tests_source = (pack_dir / "tests.py").read_text()
            visible = visible_tests(tests_source)
            groups, helpers = class_helpers(tests_source, visible)
            for test, group in zip(visible, groups):
                test["group"] = group
            prelude = local_prelude(tests_source, visible, helpers)
            executor_tests[data["slug"]] = {"tests": tests_source, "packages": data["permitted_packages"], "testCount": data["test_count"], "visibleNames": [test["name"] for test in visible],
                                          "testNames": sorted({n.name for n in ast.walk(ast.parse(tests_source)) if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")})}
            local_compat[data["slug"]] = locally_compatible(tests_source, data["permitted_packages"], prelude, helpers)
            packs[data["slug"]] = {
                **record,
                "objectives": data["learning_objectives"],
                "allowedPackages": data["permitted_packages"],
                "optionalPackages": data.get("optional_packages", []),
                "article": article,
                "statement": section(statement, "Task", "Hints"),
                "starter": (pack_dir / "starter.py").read_text(),
                "solution": (pack_dir / "solution.py").read_text(),
                "solutionExplanation": section(statement, "Worked solution", "References"),
                "hints": data["hints"],
                "failureFeedback": data["failure_feedback"],
                "visibleTests": visible,
                "localPrelude": prelude if local_compat[data["slug"]] else "",
                "localClasses": helpers if local_compat[data["slug"]] else [],
                "resources": [{"id": source_id, **sources[source_id]} for source_id in source_ids],
            }
        problems.extend(topic_problems)
        projects.extend(topic_projects)
        topics.append({
            "slug": slug, "title": title, "prefix": prefix, "prerequisites": prerequisites,
            "outcome": outcome, "description": intro,
            # problemCount counts the required steps: optional deep dives do not count towards completion.
            "problemCount": sum(not problem["optional"] for problem in topic_problems),
            "optionalCount": sum(problem["optional"] for problem in topic_problems),
            "projectCount": len(topic_projects),
            "difficultyCounts": dict(counts),
            "resources": [{"id": source_id, **sources[source_id]} for source_id, _ in topic_sources.most_common(4)],
        })
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "catalogue.generated.json").write_text(json.dumps({"topics": topics, "problems": problems, "projects": projects}, ensure_ascii=False, indent=2) + "\n")
    (OUTPUT / "packs.generated.json").write_text(json.dumps(packs, ensure_ascii=False, indent=2) + "\n")
    (OUTPUT / "projects.generated.json").write_text(json.dumps(project_pages, ensure_ascii=False, indent=2) + "\n")
    (OUTPUT / "local-compat.generated.json").write_text(json.dumps(local_compat, indent=2) + "\n")
    executor_output = ROOT / "executor" / "tests.generated.json"
    executor_output.parent.mkdir(parents=True, exist_ok=True)
    executor_output.write_text(json.dumps(executor_tests, ensure_ascii=False) + "\n")
    print(f"Generated {len(topics)} topics, {len(problems)} problems ({sum(p['optional'] for p in problems)} optional) "
          f"and {len(projects)} project ideas; {sum(local_compat.values())} run visible tests in the browser")


if __name__ == "__main__":
    main()
