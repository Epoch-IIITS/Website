# AIML Gym — Learning Path Packs

291 step-by-step Python lessons and graded exercises (41 optional) and 31 project ideas in 15 topics for UG1/UG2 learners: Python, Mathematics for AI/ML, Statistics, NumPy, Pandas, FastAPI, Machine Learning, Deep Learning, Computer Vision, Natural Language Processing, Large Language Models, Explainable AI, Federated Learning, Reinforcement Learning, Agentic AI.

| File | Contents |
|---|---|
| `curriculum.md` | The learning sequence, every step, what changed, design choices, remaining gaps, integration work |
| `coverage-map.md` | Audit of the previous curriculum, topic prerequisites, required-coverage table, step-by-step map, legacy IDs |
| `coverage.md` | Counts, completeness, validation results per environment, path audits, duplicates, sources, runtime constraints |
| `manifest.csv` | One row per step in path order |
| `sources.csv` | References with URL, access date, licence status and the steps citing them |
| `topics/<topic>/overview.md` | Topic introduction and its ordered steps |
| `topics/<topic>/<slug>/` | `metadata.json`, `article.md` (lesson), `problem.md`, `starter.py`, `solution.py`, `tests.py`; an ungraded project idea has only `metadata.json` and `project.md` |
| `build/` | Generator sources and validation tooling (see below) |

## Working on a step

```bash
cd topics/<topic>/<slug>
AIMLGYM_TARGET=starter python -m unittest tests -v   # your code
python -m unittest tests -v                          # reference solution
```

## Rebuilding and validating

| Path | Role |
|---|---|
| `build/path.py` | Topic order, step order and the 'taught before used' maps — the single source of the path |
| `build/overviews.py` | Topic introductions |
| `build/topics/*.py` | Step definitions (lesson, statement, starter, hints, solution, tests, feedback) |
| `build/library_comparisons.py` | Library sections and comparison tests attached to retained packs |
| `build/build.py` | Assigns IDs, resolves `[[slug]]` references, renders every pack and overview |
| `build/validate.py` | Runs every pack against solution and starter; writes `build/results/<label>.json` |
| `build/audit.py` | Prerequisite, difficulty and taught-before-used checks |
| `build/reports.py` | Writes the manifest, reports, curriculum and README |
| `build/requirements-*.txt` | Pinned validation environments |

From the `aimlgym/` directory:

```bash
python3 build/build.py
uv venv -p 3.13 .venv-exec && VIRTUAL_ENV=.venv-exec uv pip install -r build/requirements-executor.txt
.venv-exec/bin/python build/validate.py --label executor-pins
uv venv -p 3.13 .venv-full && VIRTUAL_ENV=.venv-full uv pip install -r build/requirements-full.txt
.venv-full/bin/python build/validate.py --label full
python3 build/audit.py
python3 build/reports.py
```

Any Python 3.13 virtual environment works in place of `uv`. `build.py`, `audit.py` and `reports.py` need only the standard library; `validate.py` must run in an environment with the packages under test. Keep virtual environments outside the published pack directories.
