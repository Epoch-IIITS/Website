"""Static checks that every step uses only what earlier steps taught.

    python3 build/audit.py          # print violations for the rendered packs

`features(source)` lists the Python constructs, imports and selected library calls in a file.
`violations()` compares each pack's starter.py and solution.py with path.FEATURE_INTRO,
IMPORT_INTRO and LIBRARY_INTRO: a construct whose introducing step comes later in the path is a
violation. It also checks prerequisite order, cross-topic prerequisites and difficulty order.
Optional deep dives are side branches: required steps may not depend on them (as a prerequisite
or as the step that introduces a construct), and they are left out of the difficulty order.
"""
import ast
import json
import os
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
sys.path.insert(0, BUILD)
from path import FEATURE_INTRO, IMPORT_INTRO, LIBRARY_INTRO, PATH, TOPICS  # noqa: E402

LEVEL = {"beginner": 0, "intermediate": 1, "advanced": 2}


def features(source):
    found = set()
    tree = ast.parse(source)
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            if n.func.id in ("print", "input"):
                found.add(n.func.id)
            if n.func.id in ("int", "float", "str", "bool", "type"):
                found.add("conversion")
        if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            found.add("assignment")
        if isinstance(n, ast.AugAssign):
            found.add("arithmetic")
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.FloorDiv, ast.Mod, ast.Pow)):
            if not (isinstance(n.op, ast.Mod) and isinstance(n.left, ast.Constant)
                    and isinstance(n.left.value, str)):
                found.add("arithmetic")
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.MatMult):
            found.add("matmul")
        if isinstance(n, ast.JoinedStr):
            found.add("f-string")
        if isinstance(n, ast.Subscript):
            found.add("subscript")
        if isinstance(n, (ast.If, ast.IfExp)):
            found.add("if")
        if isinstance(n, ast.BoolOp):
            found.add("boolean-logic")
        if isinstance(n, ast.While):
            found.add("while")
        if isinstance(n, (ast.For, ast.AsyncFor)):
            found.add("for")
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found.add("def")
            a = n.args
            if a.vararg or a.kwarg:
                found.add("varargs")
            if a.kwonlyargs:
                found.add("keyword-only")
            if n.decorator_list:
                found.add("decorator")
        if isinstance(n, (ast.AsyncFunctionDef, ast.Await, ast.AsyncWith, ast.AsyncFor)):
            found.add("async")
        if isinstance(n, (ast.List, ast.ListComp)):
            found.add("list")
        if isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp)):
            found.add("comprehension")
        if isinstance(n, ast.GeneratorExp):
            found.add("generator-expression")
        if isinstance(n, (ast.Dict, ast.DictComp)):
            found.add("dict")
        if isinstance(n, (ast.Set, ast.SetComp)) or (
                isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("set", "frozenset")):
            found.add("set")
        if isinstance(n, (ast.Assign, ast.For, ast.comprehension)):
            targets = n.targets if isinstance(n, ast.Assign) else [n.target]
            if any(isinstance(t, (ast.Tuple, ast.List)) for t in targets):
                found.add("tuple-unpacking")
        if isinstance(n, ast.Lambda):
            found.add("lambda")
        if isinstance(n, (ast.Yield, ast.YieldFrom)):
            found.add("yield")
        if isinstance(n, ast.Raise):
            found.add("raise")
        if isinstance(n, ast.Try):
            found.add("try")
        if isinstance(n, (ast.With, ast.AsyncWith)):
            found.add("with")
        if isinstance(n, ast.ClassDef):
            found.add("class")
            if n.bases:
                found.add("inheritance")
        if isinstance(n, ast.Import):
            found.add("import")
            for a in n.names:
                found.add("import:" + a.name.split(".")[0])
        if isinstance(n, ast.ImportFrom) and n.module:
            found.add("import")
            found.add("import:" + n.module.split(".")[0])
        if isinstance(n, ast.Attribute) and n.attr in LIBRARY_INTRO:
            found.add("lib:" + n.attr)
    if _has_nested_function(tree):
        found.add("nested-function")
    return found


def _has_nested_function(tree):
    """True if a def appears inside another def (methods directly in a class do not count)."""
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for child in ast.walk(n):
                if child is not n and isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return True
    return False


def intro_of(feature):
    if feature.startswith("import:"):
        return IMPORT_INTRO.get(feature[7:], "UNREGISTERED")
    if feature.startswith("lib:"):
        return LIBRARY_INTRO[feature[4:]]
    if feature == "import":
        return FEATURE_INTRO["import"]
    return FEATURE_INTRO.get(feature)


def load():
    order, metas = [], {}
    for t in TOPICS:
        for slug in PATH[t[0]]:
            p = os.path.join(ROOT, "topics", t[0], slug)
            if not os.path.exists(os.path.join(p, "metadata.json")):
                continue
            m = json.load(open(os.path.join(p, "metadata.json"), encoding="utf-8"))
            if m["kind"] == "project":  # ungraded project ideas have no code to audit
                continue
            m["_dir"] = p
            order.append(slug)
            metas[slug] = m
    return order, metas


def violations():
    order, metas = load()
    pos = {s: i for i, s in enumerate(order)}
    topic_of = {s: metas[s]["topic"] for s in order}
    tprereq = {t[0]: set(t[3]) for t in TOPICS}

    def closure(t):
        seen, stack = set(), list(tprereq[t])
        while stack:
            x = stack.pop()
            if x not in seen:
                seen.add(x)
                stack.extend(tprereq[x])
        return seen

    out = {"feature": [], "prereq_order": [], "cross_topic": [], "cross_topic_count": [],
           "difficulty_order": [], "unregistered_import": [], "optional_dependency": []}
    feature_map = {}
    for s in order:
        m = metas[s]
        used = set()
        for f in ("starter.py", "solution.py"):
            used |= features(open(os.path.join(m["_dir"], f), encoding="utf-8").read())
        feature_map[s] = sorted(used)
        for f in sorted(used):
            intro = intro_of(f)
            if intro is None:
                continue
            if intro == "UNREGISTERED":
                out["unregistered_import"].append((m["id"], f))
            elif intro not in pos:
                out["feature"].append((m["id"], f, intro + " (not on path)"))
            elif pos[intro] > pos[s]:
                out["feature"].append((m["id"], f, metas[intro]["id"]))
            elif metas[intro].get("optional") and not m.get("optional"):
                out["optional_dependency"].append((m["id"], f, metas[intro]["id"]))
        cross = []
        for pre in m.get("prerequisite_slugs", []):
            if pre in pos and pos[pre] >= pos[s]:
                out["prereq_order"].append((m["id"], metas[pre]["id"]))
            if pre in metas and metas[pre].get("optional") and not m.get("optional"):
                out["optional_dependency"].append((m["id"], "prerequisite", metas[pre]["id"]))
            if pre in topic_of and topic_of[pre] != m["topic"]:
                cross.append(pre)
                if topic_of[pre] not in closure(m["topic"]):
                    out["cross_topic"].append((m["id"], metas[pre]["id"], topic_of[pre]))
        if len(cross) > 1:
            out["cross_topic_count"].append((m["id"], [metas[c]["id"] for c in cross]))
    for t in TOPICS:
        seq = [metas[s] for s in PATH[t[0]] if s in metas and not metas[s].get("optional")]
        for a, b in zip(seq, seq[1:]):
            if LEVEL[b["difficulty"]] < LEVEL[a["difficulty"]]:
                out["difficulty_order"].append((a["id"], a["difficulty"], b["id"], b["difficulty"]))
    return out, feature_map


if __name__ == "__main__":
    v, _ = violations()
    total = 0
    for k, items in v.items():
        print(f"{k}: {len(items)}")
        for it in items:
            print("   ", it)
        total += len(items)
    sys.exit(1 if total else 0)
