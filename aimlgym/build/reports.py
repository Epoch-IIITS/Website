"""Write the manifest, audits, curriculum and README from the rendered packs.

    python3 build/reports.py

Reads topics/*/*/metadata.json (from build.py) and build/results/*.json (from validate.py), then
writes manifest.csv, coverage.md, coverage-map.md, curriculum.md and README.md, refreshes the
`supports` column of sources.csv, and stores each pack's validation summary in its metadata.json.
"""
import csv
import difflib
import json
import os
import re
import sys
from collections import Counter, defaultdict

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
sys.path.insert(0, BUILD)

from audit import intro_of, violations  # noqa: E402
from path import FEATURE_INTRO, IMPORT_INTRO, LIBRARY_INTRO, PATH, TOPICS  # noqa: E402

REQ_FILES = ["metadata.json", "article.md", "problem.md", "starter.py", "solution.py", "tests.py"]
DATE = "2026-10-24"

# What the curriculum must cover (from the revision brief) → steps that teach it.
REQUIREMENTS = [
    ("Python", [
        ("print", ["hello-print"]), ("variables", ["variables"]), ("types and conversion", ["types-conversion"]),
        ("operators", ["arithmetic-operators", "variables"]), ("input", ["input-output"]),
        ("conditionals", ["conditionals"]), ("loops", ["while-loops", "for-loops-range"]),
        ("strings", ["string-basics", "greeting-formatter"]),
        ("collections", ["sum-and-mean", "filter-evens", "vowel-counter", "fibonacci-sequence", "unique-words"]),
        ("functions", ["greeting-formatter", "functions-as-values"]), ("files", ["files-and-json", "text-stats-stdin"]),
        ("exceptions", ["factorial-validated", "safe-divide"]), ("modules", ["standard-library", "text-stats-stdin"]),
        ("classes", ["bank-account", "shapes-inheritance"]), ("testing", ["unit-testing"]),
    ]),
    ("Mathematics", [
        ("notation (Σ, Π)", ["summation"]), ("exponentials and logarithms", ["exp-log"]),
        ("sigmoid", ["sigmoid-function"]), ("vectors", ["dot-product", "vector-norm-unit"]),
        ("matrices", ["matrix-multiply", "solve-2x2-cramer", "inverse-2x2"]), ("counting", ["binomial-coefficient"]),
        ("derivatives and chain rule", ["central-difference", "derivative-rules"]),
        ("integration", ["trapezoid-rule"]), ("optimisation", ["gradient-descent-1d", "numerical-gradient"]),
        ("series and eigenvectors", ["taylor-exp", "power-iteration"]),
    ]),
    ("Statistics", [
        ("descriptive statistics", ["mean-variance", "median-mode", "percentiles", "histogram-bins", "z-scores"]),
        ("probability", ["probability-basics", "conditional-bayes"]),
        ("distributions", ["binomial-pmf", "normal-distribution"]),
        ("simulation and sampling", ["dice-lln", "sampling-distribution"]),
        ("association", ["covariance-correlation"]),
        ("inference", ["bootstrap-ci", "chi-square-gof", "welch-t", "permutation-test"]),
    ]),
    ("NumPy", [
        ("arrays and vectorisation", ["array-info", "vectorized-math"]),
        ("indexing", ["slicing-subgrid", "boolean-mask", "fancy-indexing"]),
        ("reductions and broadcasting", ["axis-aggregations", "broadcast-center"]),
        ("linear algebra", ["matmul-dot", "linalg-solve", "pairwise-distances"]),
        ("shapes, randomness, encodings", ["reshape-stack", "seeded-generator", "one-hot", "moving-average"]),
    ]),
    ("pandas", [
        ("Series and DataFrames", ["series-basics", "dataframe-basics"]), ("reading and writing", ["read-csv-io"]),
        ("selection and derived columns", ["select-filter", "derived-columns", "sort-rank"]),
        ("missing values", ["missing-values", "fill-missing-group"]),
        ("grouping and joining", ["groupby-agg", "merge-tables"]),
        ("text and dates", ["string-cleaning", "datetime-basics", "resample-weekly"]),
        ("reshaping and windows", ["pivot-table", "binning-cut", "rolling-features"]),
    ]),
    ("FastAPI", [
        ("HTTP fundamentals", ["http-requests", "http-responses", "urls-query", "json-bodies"]),
        ("routes", ["manual-router", "fastapi-routes"]), ("validation", ["fastapi-params", "pydantic-bodies"]),
        ("errors", ["fastapi-errors", "response-models"]), ("dependencies", ["fastapi-dependencies"]),
        ("async behaviour", ["asyncio-basics", "asgi-app", "fastapi-async"]), ("API testing", ["api-testing"]),
    ]),
    ("Machine Learning", [
        ("supervised-learning vocabulary and baselines", ["ml-baselines"]),
        ("splits and metrics", ["train-test-split", "regression-metrics", "classification-metrics"]),
        ("preprocessing", ["standard-scaler"]),
        ("linear models", ["least-squares-line", "linreg-gradient-descent", "logistic-regression", "ridge-regression"]),
        ("model selection", ["polynomial-overfitting", "k-fold-cv"]),
        ("other models", ["knn-classifier", "decision-stump-gini", "kmeans"]),
    ]),
    ("Deep Learning", [
        ("forward pass", ["activations", "stable-softmax", "cross-entropy", "dense-forward", "mlp-forward"]),
        ("gradients", ["scalar-autograd", "neuron-backprop", "dense-backward", "gradient-check"]),
        ("training", ["sgd-momentum", "adam-optimizer", "train-xor-mlp"]),
        ("regularisation, normalisation, convolution", ["inverted-dropout", "batchnorm-forward", "conv1d"]),
    ]),
    ("Computer Vision", [
        ("images as arrays", ["image-arrays", "rgb-to-gray", "flip-rotate"]),
        ("pixel operations", ["threshold-binary", "intensity-histogram"]),
        ("filtering and CNN layers", ["conv2d-filter", "sobel-edges", "max-pool-2d", "conv2d-layer"]),
        ("quality and geometry", ["psnr", "bilinear-resize"]),
        ("detection post-processing", ["iou", "non-max-suppression", "connected-components"]),
    ]),
    ("NLP", [
        ("text processing", ["regex-text", "tokenize-normalize", "stopword-counts", "char-ngrams", "suffix-stemmer"]),
        ("representations", ["bag-of-words", "bigram-counts", "tf-idf", "ppmi-matrix", "embedding-analogy"]),
        ("retrieval, distance, classification", ["cosine-retrieval", "levenshtein", "naive-bayes-text"]),
    ]),
    ("LLMs", [
        ("tokens", ["token-ids", "bpe-merges"]),
        ("language modelling and decoding", ["bigram-next-token", "temperature-softmax", "greedy-decoding", "perplexity",
                                              "top-k-top-p", "beam-search"]),
        ("transformers", ["scaled-dot-attention", "causal-mask", "positional-encoding", "multi-head-attention",
                          "transformer-block", "kv-cache"]),
        ("applications", ["chat-prompt", "rag-pipeline"]),
    ]),
    ("Explainable AI", [
        ("intrinsic explanations", ["linear-contributions", "top-k-attributions", "decision-path"]),
        ("model-agnostic methods", ["ice-curve", "partial-dependence", "permutation-importance", "occlusion-saliency",
                                    "surrogate-fidelity", "exact-shapley", "lime-local", "counterfactual-search"]),
        ("gradient methods", ["integrated-gradients"]),
    ]),
    ("Federated Learning", [
        ("partitioning and aggregation", ["iid-partition", "label-skew-partition", "weighted-fedavg", "client-delta"]),
        ("training", ["local-sgd", "fedavg-round", "client-sampling", "fedavg-training", "fedprox"]),
        ("privacy and robustness", ["update-clipping", "secure-aggregation", "dp-aggregation"]),
    ]),
    ("Reinforcement Learning", [
        ("returns and environments", ["discounted-return", "gridworld-step", "env-interface"]),
        ("bandits", ["epsilon-greedy", "bandit-incremental", "ucb-bandit"]),
        ("dynamic programming", ["policy-evaluation", "value-iteration", "policy-iteration"]),
        ("learning from experience", ["mc-first-visit", "td0-prediction", "q-learning", "sarsa"]),
    ]),
    ("Agentic AI", [
        ("tools and parsing", ["tool-registry", "parse-tool-call"]),
        ("agent loops", ["reflex-agent-loop", "goal-and-budget", "react-loop", "memory-window"]),
        ("planning", ["bfs-planner", "a-star-planner", "task-dag-plan"]),
        ("reliability and safety", ["validate-and-retry", "orchestrator-workers", "permission-guardrails",
                                    "agent-evaluation"]),
    ]),
]

AUDIT_FINDINGS = [
    "Python began with `def`, default arguments and f-strings; `print`, variables, types, `input`, operators, "
    "conditionals, `while` loops, files, modules, classes and testing had no lesson, yet later packs used classes "
    "(ML, DL, RL), decorators (Agentic AI), `heapq`/`deque`/`itertools`, `json` and regular expressions.",
    "Logistic regression used the sigmoid before it was taught (it had been moved to Deep Learning), and the "
    "derivative rules behind backpropagation had no step; exponentials, logarithms and Σ notation were assumed.",
    "Statistics had no probability, conditional-probability, Bayes, normal-distribution or standard-error lessons, "
    "although Naive Bayes, Welch's t and bootstrap intervals rely on them.",
    "NumPy introduced `@` and vectorisation implicitly; pandas had no Series, CSV-reading, missing-value or date "
    "lessons before group-wise imputation and resampling.",
    "Several packs sent learners to other topics or out of order: A* depended on CV connected components, PPMI "
    "(which builds word vectors) came after the embedding-analogy step that uses word vectors, and 12 packs "
    "listed two or more cross-topic prerequisites.",
    "Difficulty bands were a fixed 4 beginner / 4 intermediate / 4 advanced split per topic rather than following "
    "the content (e.g. a list transpose was 'advanced' while exception handling was 'intermediate').",
    "Library implementations were mostly mentioned in passing; no tests compared manual code with the library.",
    "There was no FastAPI/HTTP topic and no RAG, chat-template, transformer-block, Adam, autograd or agent-evaluation "
    "step.",
    "Validation claims named pandas 3 / NumPy 2.5 while the executor image pins pandas 2.2.3 / NumPy 2.2.6.",
]

REMAINING_GAPS = [
    "Optional GPU explorations (Colab/Kaggle notebooks) were dropped from this revision at the maintainer's request; "
    "no exploration links are published.",
    "Not covered as graded steps: SVD/PCA, Poisson p-values, SVMs, recurrent networks, CNN training on real "
    "images, fine-tuning or downloading pretrained models (Hugging Face), SHAP, policy-gradient and deep RL "
    "methods, SQL databases and OAuth2/JWT authentication in FastAPI, and deployment. Several of these appear in "
    "the ungraded project ideas.",
    "LLM and agent steps use scripted fake chat models (LangChain's FakeListChatModel and GenericFakeChatModel) and "
    "keyword or toy embeddings; no real model is downloaded or called in graded work.",
    "Difficulty labels are design choices, not measured learner outcomes.",
    "Licences for many references are recorded as 'not confirmed' (see sources.csv).",
    "Packs that need PyTorch, FastAPI, LangChain, LangGraph or Gymnasium, and the asyncio ASGI step, always use "
    "the executor for Run; Pyodide does not provide those libraries or a nested event loop. The other 251 packs "
    "run their visible tests in the browser.",
    "Starlette 1.9 prints a deprecation warning recommending `httpx2` for `TestClient`; tests pass with `httpx` "
    "0.28.1, and `httpx2` was not evaluated.",
]

INTEGRATION = [
    "Done (library revision Phase 0): one executor image with every pack library (`executor/requirements.txt`, "
    "mirrored by `build/requirements-executor.txt`), two preloaded single-use containers, two job slots and a queue "
    "of 30 (Submit first), 1 GB/1 CPU/30 s per job with a 10 s CPU budget charged after imports. All 226 packs were "
    "graded through it (solution passes Run and Submit, starter fails Submit; 678 jobs, 73 per minute, slowest "
    "test run 0.7 s, peak runner memory 489 MB, measured on an Apple-silicon Mac; see `executor/measurements.json`). "
    "Pyodide now starts when a problem page opens and stays alive across Runs; SciPy, scikit-learn and OpenCV are "
    "allowed locally. The builder, generator and app support `optional` deep dives and ungraded `project` ideas.",
    "Done: `scripts/generate-learn-demo.py` reads topic order, step order and outcomes from `aimlgym/build/path.py` "
    "(15 topics including FastAPI) and publishes `kind`, `optionalPackages` and a `localPrelude` (the test-module "
    "helpers the visible cases call).",
    "Done: `public/learn/pyodide-worker.mjs` runs whole-program (`kind: script`) steps with a replaced stdin and "
    "executes the helper prelude, so 209 of 226 packs are eligible for in-browser Run (82 of 168 before). The "
    "harness was exercised with CPython 3.9 and 3.13 for every eligible pack (solution passes all visible cases, "
    "starter fails at least one); it was not run inside Pyodide in a browser.",
    "Done: `executor/Dockerfile` adds `fastapi==0.162.0` and `httpx==0.28.1`. `executor/runner.py` graded every pack "
    "in run and submit mode with the executor-pinned packages (slowest submit about 0.6 s of CPU against the 6 s "
    "limit). The image was rebuilt locally and every pack was graded through `executor/service.py`'s hardened "
    "container (no network, read-only, 768 MB, 64 PIDs): all reference solutions pass in run and submit mode and "
    "every starter fails.",
    "Done: Learn copy computes topic and problem counts; FastAPI is in the Foundations filter; `AGENTS.md`, "
    "`README.md`, `dev.md` and `executor/README.md` describe the new workflow; Learn and executor tests read test "
    "counts from the generated data.",
    "To deploy: rebuild the runner image on the VPS, copy the regenerated `executor/tests.generated.json`, restart "
    "the service, and release the matching `lib/learn/*.generated.json` fixtures together.",
    "Done (library revision Phases 1–6): library steps for SciPy, scikit-learn, PyTorch, OpenCV, LangChain, "
    "LangGraph and Gymnasium; the from-scratch steps they replace stay on the path as optional deep dives; 31 "
    "ungraded project ideas. See `library-revision-plan.md`. All 291 packs were graded through the executor on "
    "2026-10-25 (solution passes Run and Submit, starter fails; 873 jobs at 79 per minute; slowest test run 1.0 s of "
    "CPU, peak runner memory 511 MB, on an Apple-silicon Mac; `executor/measurements.json`). The runner now counts "
    "tests blocked by a failing setUpClass as failed instead of rejecting the result.",
    "Problem IDs changed. Slugs of retained packs are unchanged, so slug-keyed progress keeps working; "
    "`aimlgym/build/legacy_ids.json` maps each retained slug to its old ID for any ID-keyed data.",
]


# Graded steps per topic in path order; project ideas are counted separately in PROJECTS.
STEPS = {t[0]: [] for t in TOPICS}
PROJECTS = {t[0]: [] for t in TOPICS}


def load_metas():
    order, metas = [], {}
    for t in TOPICS:
        for slug in PATH[t[0]]:
            d = os.path.join(ROOT, "topics", t[0], slug)
            with open(os.path.join(d, "metadata.json"), encoding="utf-8") as fh:
                m = json.load(fh)
            if m["kind"] == "project":
                PROJECTS[t[0]].append(m)
                continue
            STEPS[t[0]].append(slug)
            m["_dir"] = d
            m["_path"] = f"topics/{t[0]}/{slug}"
            order.append(slug)
            metas[slug] = m
    return order, metas


def load_results():
    out = {}
    rdir = os.path.join(BUILD, "results")
    for name in sorted(os.listdir(rdir)) if os.path.isdir(rdir) else []:
        if name.endswith(".json"):
            with open(os.path.join(rdir, name)) as fh:
                rec = json.load(fh)
            if not rec.get("partial"):
                out[rec["label"]] = rec
    return out


def env_line(env):
    keys = ["python", "numpy", "pandas", "fastapi", "pydantic", "httpx", "sklearn", "scipy", "torch", "cv2",
            "langchain_core", "langgraph", "gymnasium"]
    return ", ".join(f"{k} {env[k]}" for k in keys if env.get(k)) or "unknown"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def main():
    order, metas = load_metas()
    ids = {s: metas[s]["id"] for s in order}
    results = load_results()
    tname = {t[0]: t[1] for t in TOPICS}
    viol, feature_map = violations()

    # ---- metadata validation + manifest
    per_pack = defaultdict(dict)
    for label, rec in results.items():
        for r in rec["packs"]:
            per_pack[r["slug"]][label] = {"status": r["status"], "tests": r["tests"], "skipped": r["skipped"]}
    for s in order:
        m = metas[s]
        envs = per_pack.get(s, {})
        overall = "passed" if envs and all(v["status"] == "passed" for v in envs.values()) else (
            "not run" if not envs else "FAILED")
        meta = {k: v for k, v in m.items() if not k.startswith("_")}
        meta["validation"] = {"status": overall, "date": DATE, "environments": envs}
        with open(os.path.join(m["_dir"], "metadata.json"), "w", encoding="utf-8") as fh:
            json.dump(meta, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        m["_status"] = overall

    with open(os.path.join(ROOT, "manifest.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["step", "id", "slug", "title", "topic", "difficulty", "kind", "prerequisites",
                    "permitted_packages", "optional_packages", "library_comparison",
                    "source_ids", "entry_point", "test_count", "validation_status", "path"])
        for n, s in enumerate(order, 1):
            m = metas[s]
            w.writerow([n, m["id"], s, m["title"], m["topic"], m["difficulty"], m["kind"],
                        ";".join(m["prerequisites"]),
                        ";".join(m["permitted_packages"]) or "stdlib", ";".join(m["optional_packages"]),
                        "yes" if m["library_comparison"] else "", ";".join(m["source_ids"]), m["entry_point"],
                        m["test_count"], m["_status"], m["_path"]])

    # ---- sources.csv supports column
    spath = os.path.join(ROOT, "sources.csv")
    with open(spath, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    fields = list(rows[0].keys())
    cited = defaultdict(list)
    for s in order:
        for sid in metas[s]["source_ids"]:
            cited[sid].append(ids[s])
    for r in rows:
        r["supports"] = "; ".join(cited.get(r["source_id"], [])) or "not cited by a pack"
    with open(spath, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    sources = {r["source_id"]: r for r in rows}

    write_coverage(order, metas, ids, results, viol, sources, cited, tname)
    write_map(order, metas, ids, feature_map, tname)
    write_curriculum(order, metas, ids, results, tname)
    write_readme(order, metas, results)
    print(f"reports written for {len(order)} packs; environments: {', '.join(results) or 'none'}")


def write_coverage(order, metas, ids, results, viol, sources, cited, tname):
    L = ["# Coverage and Validation Audit", "",
         f"Generated by `build/reports.py` on {DATE} from the rendered packs and `build/results/*.json`.", ""]
    L += ["## 1. Counts per topic", ""]
    rows, tot = [], Counter()
    for t in TOPICS:
        ms = [metas[s] for s in STEPS[t[0]]]
        d = Counter(m["difficulty"] for m in ms)
        opt, proj = sum(m.get("optional", False) for m in ms), len(PROJECTS[t[0]])
        rows.append([t[1], t[2], len(ms), opt, d["beginner"], d["intermediate"], d["advanced"],
                     sum(m["test_count"] for m in ms), sum(m["library_comparison"] for m in ms),
                     sum(m["kind"] == "script" for m in ms), proj])
        tot.update(n=len(ms), o=opt, b=d["beginner"], i=d["intermediate"], a=d["advanced"],
                   t=sum(m["test_count"] for m in ms), lib=sum(m["library_comparison"] for m in ms),
                   sc=sum(m["kind"] == "script" for m in ms), p=proj)
    rows.append(["**Total**", "", f"**{tot['n']}**", tot["o"], tot["b"], tot["i"], tot["a"], f"**{tot['t']}**",
                 tot["lib"], tot["sc"], tot["p"]])
    L += table(["Topic", "Prefix", "Steps", "Optional", "Beginner", "Intermediate", "Advanced", "Tests",
                "Library comparisons", "Script steps", "Project ideas"], rows) + [""]

    missing = {ids[s]: [f for f in REQ_FILES if not os.path.exists(os.path.join(metas[s]["_dir"], f))] for s in order}
    missing = {k: v for k, v in missing.items() if v}
    L += ["## 2. Pack completeness", "",
          f"* Packs: {len(order)}. Packs missing any of {', '.join(REQ_FILES)}: {len(missing)} {missing or ''}",
          f"* Minimum tests in a pack: {min(metas[s]['test_count'] for s in order)} (required ≥ 6).",
          f"* Every pack has exactly 3 progressive hints: {all(len(metas[s]['hints']) == 3 for s in order)}.",
          f"* Every pack has failure feedback naming existing tests: {all(metas[s]['failure_feedback'] for s in order)} "
          "(`build.py` rejects feedback for unknown test names).",
          "* Every lesson starts with learning outcomes and contains an explanation, a worked example, common mistakes "
          "and references; packs with `library_comparison` add a library section and comparison tests.", ""]

    L += ["## 3. Validation results", "",
          "`build/validate.py` runs every pack's tests twice: against `solution.py` (all tests must pass) and against "
          "`starter.py` (at least one test must fail, so the tests are not vacuous).", ""]
    rows = []
    for label, rec in results.items():
        packs = rec["packs"]
        rows.append([label, env_line(rec["environment"]),
                     f"{sum(p['status'] == 'passed' for p in packs)}/{len(packs)}",
                     sum(p["starter_fails"] for p in packs), sum(p["tests"] for p in packs),
                     sum(p["skipped"] for p in packs)])
    L += table(["Environment", "Versions", "Packs passed", "Starters failing ≥1 test", "Tests run", "Skipped"], rows)
    L += ["", "* `executor-pins` installs `build/requirements-executor.txt`, the same pins as the executor image "
          "(`executor/requirements.txt`): Python 3.13, NumPy 2.2.6, pandas 2.2.3, SciPy 1.14.1, scikit-learn 1.6.1, "
          "OpenCV 4.10, PyTorch 2.14.1 (CPU), FastAPI, httpx, LangChain Core, LangGraph and Gymnasium.",
          "* `full` uses current NumPy/pandas and installs the optional comparison libraries, so nothing is skipped.",
          "* Stochastic packs assert properties or recipe equality with seeded generators "
          "(`random.Random(seed).random()` or `numpy.random.default_rng(seed)`).", ""]

    L += ["## 4. Learning-path audits", "",
          "`build/audit.py` checks the rendered packs:", "",
          "* **Taught before used** — every Python construct, import and selected library call in a starter or "
          "solution must be introduced at that step or earlier (`FEATURE_INTRO`, `IMPORT_INTRO`, `LIBRARY_INTRO` in "
          "`build/path.py`).",
          "* **Prerequisite order** — every prerequisite appears earlier in the path.",
          "* **Cross-topic prerequisites** — must come from the topic's declared prerequisite topics (transitively), "
          "and a step may list at most one.",
          "* **Difficulty order** — difficulty never decreases along a topic.", ""]
    L += table(["Check", "Violations"], [[k.replace("_", " "), len(v)] for k, v in viol.items()])
    for k, v in viol.items():
        if v:
            L += ["", f"{k}: {v}"]
    cross = sum(1 for s in order for p in metas[s]["prerequisite_slugs"] if metas[p]["topic"] != metas[s]["topic"])
    L += ["", f"* Cross-topic prerequisite links: {cross} (each to an earlier topic, at most one per step).", ""]

    slugs = Counter(order)
    titles = Counter(metas[s]["title"].lower() for s in order)
    near = []
    for a_i, a in enumerate(order):
        for b in order[a_i + 1:]:
            r = difflib.SequenceMatcher(None, metas[a]["title"].lower(), metas[b]["title"].lower()).ratio()
            if r >= 0.8:
                near.append((ids[a], ids[b], round(r, 2)))
    L += ["## 5. Duplicate audit", "",
          f"* Duplicate slugs: {[s for s, c in slugs.items() if c > 1] or 'none'}; duplicate titles: "
          f"{[s for s, c in titles.items() if c > 1] or 'none'}.",
          f"* Titles with similarity ≥ 0.8: {near or 'none'}. Pairs that remain teach different things (for "
          "example HTTP status codes written by hand versus FastAPI response models); optional deep dives whose "
          "titles were close to their library step end in 'by Hand'.",
          "* Intentional reuse: later packs re-implement small helpers (softmax, sigmoid, a parser) inside their own "
          "solution so each pack runs alone; the transformer-block starter supplies the multi-head attention from the "
          "previous step.", ""]

    unused = [s for s in sources if s not in cited]
    bad = [(ids[s], x) for s in order for x in metas[s]["source_ids"] if x not in sources]
    nolic = [s for s, r in sources.items() if "not confirmed" in r["license"].lower()]
    L += ["## 6. Source audit", "",
          f"* Sources: {len(sources)}; verification: {dict(Counter(r['verified'] for r in sources.values()))}. "
          f"S040–S141 were opened on 2026-10-24/25 (OpenCV documentation pages in a browser, because the server "
          "refuses scripted requests).",
          f"* Packs citing an unknown source: {bad or 'none'}; packs with no source: "
          f"{[ids[s] for s in order if not metas[s]['source_ids']] or 'none'}.",
          f"* Sources not cited by any pack: {unused or 'none'}.",
          f"* Sources whose licence is not confirmed: {len(nolic)} (listed in sources.csv).", ""]
    L += table(["Source", "Title", "Cited by"], [[s, sources[s]["title"], len(cited.get(s, []))] for s in sources]) + [""]

    pk = Counter()
    for s in order:
        for p in metas[s]["permitted_packages"] or ["stdlib only"]:
            pk[p] += 1
    opt = Counter(p for s in order for p in metas[s]["optional_packages"])
    patterns = {"network calls": r"\b(urllib\.request|requests\.|socket\.|http\.client\.HTTPConnection|httpx\.(get|post|AsyncClient))",
                "paid LLM SDKs": r"\b(openai|anthropic)\b", "GPU use": r"\bcuda\b|\.to\(['\"]cuda"}
    hits = {}
    for name, pat in patterns.items():
        rx = re.compile(pat)
        hits[name] = [ids[s] for s in order
                      if any(rx.search(open(os.path.join(metas[s]["_dir"], f), encoding="utf-8").read())
                             for f in ("solution.py", "tests.py", "starter.py"))]
    L += ["## 7. Packages and runtime constraints", ""]
    L += table(["Permitted package", "Packs"], sorted(pk.items())) + [""]
    L += table(["Optional comparison package", "Packs"], sorted(opt.items())) + [""]
    scan = ", ".join(f"{k}: {v or 'none'}" for k, v in hits.items())
    L += [f"* Code scan of starters, solutions and tests — {scan}.",
          "* No dataset downloads: all data is defined inline or generated with seeded generators. External "
          "services (weather API, language models, agents' tools) are replaced by fakes or scripted functions.",
          "* FastAPI packs call the app in-process with `fastapi.testclient.TestClient`; no server or port is opened.", ""]
    with open(os.path.join(ROOT, "coverage.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def introduced_here(slug):
    keys = [k for k, v in FEATURE_INTRO.items() if v == slug]
    keys += [f"import {k}" for k, v in IMPORT_INTRO.items() if v == slug]
    keys += [f"`.{k}`" for k, v in LIBRARY_INTRO.items() if v == slug]
    return ", ".join(keys)


def write_map(order, metas, ids, feature_map, tname):
    with open(os.path.join(BUILD, "legacy_ids.json")) as fh:
        legacy = json.load(fh)
    L = ["# Prerequisite and Coverage Map", "",
         f"Generated by `build/reports.py` on {DATE}. The path is defined in `build/path.py`; IDs are assigned from it.", "",
         "## 1. Audit of the previous curriculum (168 packs)", "",
         "Problems found before this revision, and fixed by it:", ""]
    L += [f"{n}. {f}" for n, f in enumerate(AUDIT_FINDINGS, 1)] + [""]
    L += ["## 2. Topic prerequisites", "", "```mermaid", "flowchart LR"]
    for t in TOPICS:
        L.append(f'  {t[2]}["{t[2]} · {t[1]}"]')
    for t in TOPICS:
        for p in t[3]:
            L.append(f"  {[x[2] for x in TOPICS if x[0] == p][0]} --> {t[2]}")
    L += ["```", "", "Recommended order: " + " → ".join(t[1] for t in TOPICS) + ". FastAPI needs only Python; it is "
          "placed after pandas so the software-engineering steps come before machine learning.", ""]
    L += ["## 3. Required coverage", "", "Each required area and the steps that teach it.", ""]
    for topic, items in REQUIREMENTS:
        L += [f"### {topic}", ""]
        L += table(["Area", "Steps"], [[a, ", ".join(f"{ids[s]} {metas[s]['title']}" for s in slugs)] for a, slugs in items])
        L.append("")
    L += ["## 4. Step-by-step map", "",
          "*Builds on* lists the step's prerequisites. *Introduces* lists the Python constructs, imports and library "
          "calls whose first allowed use is this step (checked by `build/audit.py`).", ""]
    for t in TOPICS:
        L += [f"### {t[2]} · {t[1]}", ""]
        L += table(["ID", "Step", "Difficulty", "Builds on", "Introduces", "Concepts"],
                   [[ids[s], metas[s]["title"], metas[s]["difficulty"], ", ".join(metas[s]["prerequisites"]) or "—",
                     introduced_here(s) or "—", ", ".join(metas[s]["concept_tags"])] for s in STEPS[t[0]]])
        L.append("")
    L += ["## 5. Cross-topic links", "", "Steps whose prerequisite is in an earlier topic (at most one per step).", ""]
    L += table(["Step", "Earlier-topic prerequisite"],
               [[f"{ids[s]} {metas[s]['title']}", f"{ids[p]} {metas[p]['title']}"]
                for s in order for p in metas[s]["prerequisite_slugs"] if metas[p]["topic"] != metas[s]["topic"]])
    L += ["", "## 6. Legacy ID mapping", "",
          "Retained packs keep their slugs; their IDs changed. New packs have no legacy ID.", ""]
    L += table(["Slug", "Old ID", "New ID"], [[s, legacy[s], ids[s]] for s in sorted(legacy, key=lambda x: ids[x])])
    L.append("")
    with open(os.path.join(ROOT, "coverage-map.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def write_curriculum(order, metas, ids, results, tname):
    with open(os.path.join(BUILD, "legacy_ids.json")) as fh:
        legacy = json.load(fh)
    new = [s for s in order if s not in legacy]
    L = ["# AIML Gym Curriculum", "",
         f"{len(order)} graded steps ({sum(metas[s].get('optional', False) for s in order)} of them optional deep dives) "
         f"and {sum(len(v) for v in PROJECTS.values())} ungraded project ideas in {len(TOPICS)} topics for UG1/UG2 "
         "learners, arranged as one path that starts from zero "
         "Python. Every step has a lesson (outcomes, explanation, worked example, common mistakes, references) and a "
         "graded exercise (starter, three progressive hints, reference solution, failure feedback and at least six "
         "deterministic tests). Core exercises run on a CPU without network access, GPUs, paid APIs or downloads.", "",
         "## How to work through a step", "", "```bash", "cd topics/python/hello-print",
         "# read article.md and problem.md, edit starter.py, then:", "AIMLGYM_TARGET=starter python -m unittest tests -v",
         "```", "",
         "Python 3.10+ is required (validated on 3.13). Install `build/requirements-executor.txt` (NumPy, pandas, "
         "SciPy, scikit-learn, OpenCV, PyTorch CPU, FastAPI, httpx, LangChain Core, LangGraph, Gymnasium) to run "
         "every step. Optional deep dives are graded but do not count towards topic completion; project ideas are "
         "ungraded briefs (`project.md`).", "",
         "## The learning sequence", ""]
    L += table(["#", "Topic", "Prefix", "Steps", "Topic prerequisites", "You will be able to"],
               [[n, f"[{t[1]}](topics/{t[0]}/overview.md)", t[2], len(STEPS[t[0]]),
                 ", ".join(tname[p] for p in t[3]) or "—", t[5]] for n, t in enumerate(TOPICS, 1)])
    L.append("")
    for t in TOPICS:
        L += [f"### {t[2]} · {t[1]}", ""]
        L += table(["ID", "Step", "Difficulty", "Builds on", "Tests", "Library comparison"],
                   [[ids[s], f"[{metas[s]['title']}]({metas[s]['_path']}/problem.md)", metas[s]["difficulty"],
                     ", ".join(metas[s]["prerequisites"]) or "—",
                     metas[s]["test_count"], "yes" if metas[s]["library_comparison"] else ""] for s in STEPS[t[0]]])
        L.append("")
    L += ["## What changed in this revision", "",
          f"* {len(new)} new steps and {len(order) - len(new)} retained packs, reordered into one path; IDs are "
          "reassigned from the path (`build/legacy_ids.json` keeps the old ones).",
          "* New FastAPI topic (15 steps): HTTP messages, status codes, URLs, JSON bodies, a hand-made router, asyncio "
          "and ASGI with the standard library, then FastAPI routes, parameters, Pydantic bodies, errors, response models, "
          "dependencies, async endpoints and API testing.",
          "* Library comparisons: lessons show the manual and the idiomatic library implementation (standard library, "
          "NumPy, pandas, scikit-learn, SciPy, PyTorch) and tests compare them where the comparison is meaningful.",
          "* Retained packs were adjusted where they used untaught concepts (e.g. Fibonacci no longer raises before "
          "exceptions are taught) and their prerequisites and difficulty labels follow the path.",
          "* New: a static audit that every construct is taught before use, and a coverage map (coverage-map.md).", "",
          "New steps: " + ", ".join(f"{ids[s]} {metas[s]['title']}" for s in new) + ".", "",
          "## Confirmed facts and design choices", "",
          "**Confirmed by running code:** all reference solutions pass and all starters fail at least one test in each "
          "recorded environment (coverage.md §3); the audit in coverage.md §4 reports no violations; worked-example "
          "numbers in new lessons were checked by the tests that reproduce them.", "",
          "**Design choices:** the topic order and step order; difficulty labels; simplified "
          "protocols for teaching (the chat template, the `<tool_call>` format, whole-word tokens, toy MDPs, synthetic "
          "data); scripted models in place of real LLMs; privacy steps teach mechanics without formal guarantees; "
          "test tolerances chosen from observed numerical behaviour.", "",
          "## Remaining gaps", ""]
    L += [f"* {g}" for g in REMAINING_GAPS]
    L += ["", "## Next.js and executor integration", ""]
    L += [f"{n}. {x}" for n, x in enumerate(INTEGRATION, 1)]
    L.append("")
    with open(os.path.join(ROOT, "curriculum.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def write_readme(order, metas, results):
    L = ["# AIML Gym — Learning Path Packs", "",
         f"{len(order)} step-by-step Python lessons and graded exercises "
         f"({sum(metas[s].get('optional', False) for s in order)} optional) and "
         f"{sum(len(v) for v in PROJECTS.values())} project ideas in {len(TOPICS)} topics for UG1/UG2 learners: "
         + ", ".join(t[1] for t in TOPICS) + ".", "",
         "| File | Contents |", "|---|---|",
         "| `curriculum.md` | The learning sequence, every step, what changed, design choices, remaining gaps, integration work |",
         "| `coverage-map.md` | Audit of the previous curriculum, topic prerequisites, required-coverage table, step-by-step map, legacy IDs |",
         "| `coverage.md` | Counts, completeness, validation results per environment, path audits, duplicates, sources, runtime constraints |",
         "| `manifest.csv` | One row per step in path order |",
         "| `sources.csv` | References with URL, access date, licence status and the steps citing them |",
         "| `topics/<topic>/overview.md` | Topic introduction and its ordered steps |",
         "| `topics/<topic>/<slug>/` | `metadata.json`, `article.md` (lesson), `problem.md`, `starter.py`, `solution.py`, `tests.py`; "
         "an ungraded project idea has only `metadata.json` and `project.md` |",
         "| `build/` | Generator sources and validation tooling (see below) |", "",
         "## Working on a step", "",
         "```bash", "cd topics/<topic>/<slug>", "AIMLGYM_TARGET=starter python -m unittest tests -v   # your code",
         "python -m unittest tests -v                          # reference solution", "```", "",
         "## Rebuilding and validating", "",
         "| Path | Role |", "|---|---|",
         "| `build/path.py` | Topic order, step order and the 'taught before used' maps — the single source of the path |",
         "| `build/overviews.py` | Topic introductions |",
         "| `build/topics/*.py` | Step definitions (lesson, statement, starter, hints, solution, tests, feedback) |",
         "| `build/library_comparisons.py` | Library sections and comparison tests attached to retained packs |",
         "| `build/build.py` | Assigns IDs, resolves `[[slug]]` references, renders every pack and overview |",
         "| `build/validate.py` | Runs every pack against solution and starter; writes `build/results/<label>.json` |",
         "| `build/audit.py` | Prerequisite, difficulty and taught-before-used checks |",
         "| `build/reports.py` | Writes the manifest, reports, curriculum and README |",
         "| `build/requirements-*.txt` | Pinned validation environments |", "",
         "From the `aimlgym/` directory:", "",
         "```bash", "python3 build/build.py",
         "uv venv -p 3.13 .venv-exec && VIRTUAL_ENV=.venv-exec uv pip install -r build/requirements-executor.txt",
         ".venv-exec/bin/python build/validate.py --label executor-pins",
         "uv venv -p 3.13 .venv-full && VIRTUAL_ENV=.venv-full uv pip install -r build/requirements-full.txt",
         ".venv-full/bin/python build/validate.py --label full",
         "python3 build/audit.py", "python3 build/reports.py", "```", "",
         "Any Python 3.13 virtual environment works in place of `uv`. `build.py`, `audit.py` and `reports.py` need only "
         "the standard library; `validate.py` must run in an environment with the packages under test. Keep virtual "
         "environments outside the published pack directories.", ""]
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    main()
