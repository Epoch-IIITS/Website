# Library-Driven Revision — Plan

Status: **implemented (Phases 0–6), 2026-10-25.** 291 graded packs (250 required, 41 optional deep dives) and 31 project ideas; all pass in both validation environments and through the executor (873 jobs; slowest test run 1.0 s of CPU, peak memory 511 MB; see `executor/measurements.json`).

Requirements from review:

1. Do not compromise the learning experience.
2. Expose students to the common libraries of the ML ecosystem.
3. Add **project ideas** between steps: briefs for things students can build with what they have
   learned so far.
4. Every library must run either in the browser (Pyodide) or on the VPS executor.
5. VPS: **2 vCPU, 4 GB RAM, 40 GB SSD**. Preload libraries so execution is fast.

## 1. Principles

Each topic follows three stages:

1. **Understand** — from-scratch steps for the core ideas (gradient descent, backprop, convolution,
   attention, an agent loop).
2. **Use** — the library, idiomatically: scikit-learn, SciPy, PyTorch, OpenCV, LangChain, LangGraph,
   Gymnasium. Each lesson has a "What the library does inside" section that links to the scratch step.
3. **Apply** — realistic graded tasks, plus ungraded **project ideas** (§3).

**Nothing is deleted.** When a step moves to a library, the library version becomes the required step
and the existing scratch version stays on the path as an **optional deep dive** placed right after it,
under its existing slug. Learners who want the mechanism can still build it; nobody loses progress, and
the required path is not longer than it needs to be.

Unchanged rules: CPU-only, no network, no downloads in graded steps, deterministic tests, at least six
tests, starter fails / solution passes, every library introduced before use (audit).

Deterministic library tests: tiny synthetic data generated in the test; fixed seeds (`random_state`,
`torch.manual_seed`, `torch.use_deterministic_algorithms(True)`, one thread); tolerances and property
checks after training ("loss falls below half its starting value"); fake LLMs from `langchain_core`
(`GenericFakeChatModel`, `FakeListChatModel`, `DeterministicFakeEmbedding`) instead of APIs.

## 2. Topic-by-topic changes

Legend: **Keep** = required, from scratch · **Library** = new required library step that replaces a
scratch step on the required path · **Deep dive** = the replaced scratch step, kept as optional ·
**New** = additional required step.

### Python (27) · Mathematics (16) · NumPy (14) · pandas (16) · FastAPI (15)

No structural change; these already teach their libraries (Mathematics is the concept itself). They gain
project ideas (§3).

### Statistics (16 → 17 required, +3 optional)

| Action | Steps |
|---|---|
| Keep | ST-01–ST-13 |
| New | **Introducing `scipy.stats`** — distribution objects `norm`, `binom`, `.pdf/.cdf/.ppf`, checked against ST-08/ST-09 |
| Library | Chi-square test (`scipy.stats.chisquare`, p-values); Welch's t-test (`ttest_ind(equal_var=False)`); Permutation test (`scipy.stats.permutation_test`) |
| Deep dive | ST-14 Chi-square by hand, ST-15 Welch's t by hand, ST-16 Permutation test by hand |

### Machine Learning (14 → 19 required, +8 optional)

| Action | Steps |
|---|---|
| Keep | ML-01 Baselines, ML-04 Confusion matrix & metrics, ML-06 Least squares, ML-08 Gradient descent regression, ML-09 Logistic regression, ML-13 Decision stump (Gini) |
| New | **scikit-learn estimator API** (`fit`, `predict`, `score`, `get_params`, `clone`, `sklearn.metrics`); **Pipelines and `ColumnTransformer`** on a pandas frame; **Hyperparameter search** (`GridSearchCV`, regularisation with `Ridge`/`LogisticRegression(C=...)`); **Trees and random forests**; **Gradient boosting** (`HistGradientBoostingClassifier`); **Thresholds, ROC and PR curves**; **Capstone: end-to-end tabular model** |
| Library | `train_test_split`/`StratifiedShuffleSplit`; `StandardScaler` in a `Pipeline` (leakage); `KNeighborsClassifier`; `PolynomialFeatures` + validation curve; `KFold`/`cross_val_score`; `KMeans` + silhouette |
| Deep dive | ML-02 Split, ML-03 Regression metrics, ML-05 Scaler, ML-07 k-NN, ML-10 Polynomial overfitting, ML-11 k-fold, ML-12 Ridge closed form, ML-14 k-means (all by hand) |

### Deep Learning (15 → 20 required, +7 optional)

| Action | Steps |
|---|---|
| Keep | DL-01 Activations, DL-02 Softmax, DL-03 Cross-entropy, DL-04 Dense forward, DL-06 Scalar autograd, DL-07 Neuron backprop, DL-08 Dense backward, DL-10 SGD with momentum |
| New | **PyTorch tensors**; **Autograd in PyTorch** (compared with DL-06); **Datasets and DataLoader**; **Saving, loading and reproducibility** (`state_dict`, seeds); **Debugging training** (overfit one batch, learning rate, exploding gradients) |
| Library | `nn.Module`/`nn.Sequential` MLP; `torch.autograd.gradcheck`; `torch.optim` (SGD, Adam, AdamW); full training loop; `nn.Dropout` with `train()`/`eval()`; `nn.BatchNorm1d`; `nn.Conv1d` |
| Deep dive | DL-05, DL-09, DL-11, DL-12, DL-13, DL-14, DL-15 (by hand in NumPy) |

### Computer Vision (14 → 18 required, +8 optional)

| Action | Steps |
|---|---|
| Keep | CV-01 Images as arrays, CV-02 RGB to grey, CV-06 2D filtering, CV-09 Convolution layer, CV-12 IoU, CV-13 NMS |
| New | **OpenCV basics** (BGR/RGB, dtypes, indexing); **Contours and bounding boxes**; **A small CNN in PyTorch** on generated shapes; **Data augmentation** |
| Library | OpenCV: `flip`/`rotate`/`warpAffine`, `threshold` (+ Otsu), `calcHist`/`equalizeHist`, `Sobel`/`Canny`, `PSNR`, `resize`, `connectedComponentsWithStats`; PyTorch: `nn.MaxPool2d`/`AvgPool2d` |
| Deep dive | CV-03, CV-04, CV-05, CV-07, CV-08, CV-10, CV-11, CV-14 (by hand) |

### NLP (13 → 14 required, +5 optional)

| Action | Steps |
|---|---|
| Keep | NL-01 Regex, NL-02 Tokenise, NL-05 Bag of words, NL-07 TF-IDF, NL-09 Levenshtein, NL-11 Naive Bayes, NL-12 PPMI, NL-13 Analogies |
| New | **Text classification pipeline** (`TfidfVectorizer` + `LogisticRegression`); **Evaluating text classifiers** (error analysis); **Embeddings in PyTorch** (`nn.EmbeddingBag` classifier) |
| Library | `Counter` + `CountVectorizer(stop_words=...)`; `CountVectorizer(analyzer="char_wb")`; `TfidfVectorizer` + `cosine_similarity` retrieval |
| Deep dive | NL-03, NL-04, NL-08 (by hand); NL-06 Bigram counts and NL-10 Suffix stemmer become optional (bigrams are counted again in LM-02) |

### Large Language Models (16 → 18 required, +3 optional)

| Action | Steps |
|---|---|
| Keep | LM-01–LM-10, LM-12 Top-k/top-p, LM-13 Beam search, LM-14 KV cache |
| New | **A tiny GPT in PyTorch** (character level, CPU, a few hundred steps); **Structured output** (Pydantic + LangChain output parsers, retries) |
| Library | Transformer block as a PyTorch `nn.Module` (vs `nn.TransformerEncoderLayer`); LangChain `ChatPromptTemplate` and messages; LangChain RAG (`InMemoryVectorStore`, fake embeddings and chat model, citation check) |
| Deep dive | LM-11, LM-15, LM-16 (by hand) |

Hugging Face models and tokenizers need downloads, so they appear in lessons and project ideas, not in
graded steps.

### Explainable AI (12 → 12 required, +2 optional)

| Action | Steps |
|---|---|
| Keep | XA-01–XA-04, XA-07–XA-12 |
| Library | `sklearn.inspection.partial_dependence`; `sklearn.inspection.permutation_importance` on a pipeline |
| Deep dive | XA-05, XA-06 (by hand) |

SHAP is not added (needs `numba`, not available in Pyodide and heavy for the VPS); exact Shapley and
LIME-style steps already teach the ideas. SHAP appears in a project idea.

### Federated Learning (12 → 13 required, +1 optional)

| Action | Steps |
|---|---|
| Keep | FL-01–FL-04, FL-06–FL-12 |
| New | **FedAvg with PyTorch `state_dict`s** |
| Library | Local client training with a PyTorch `nn.Module` |
| Deep dive | FL-05 (by hand) |

Flower is described in a project idea (it needs networking between processes, which graded steps do not
have).

### Reinforcement Learning (13 → 15 required)

| Action | Steps |
|---|---|
| Keep | All 13 |
| New | **Gymnasium environments** (`gymnasium.Env`, wrapping LineWorld, `TimeLimit`); **Q-learning on FrozenLake** (`gymnasium.make("FrozenLake-v1")`, seeded, text-only) |

### Agentic AI (13 → 16 required, +4 optional)

| Action | Steps |
|---|---|
| Keep | AG-01–AG-05, AG-07–AG-09, AG-13 |
| New | **LangChain tools and tool calling** (`@tool`, `bind_tools`, `ToolMessage`, fake model returning tool calls); **LangGraph basics** (state, nodes, conditional edges); **A LangGraph ReAct agent** (`ToolNode`, step limits, `InMemorySaver` checkpoints) |
| Library | Memory with LangChain messages and `trim_messages`; validate-and-retry with Pydantic and a fake model; orchestrator–workers as a LangGraph graph; guardrails with a LangGraph approval (interrupt) node |
| Deep dive | AG-06, AG-10, AG-11, AG-12 (by hand) |

### Summary

| Topic | Required now | Required after | Optional deep dives | Project ideas |
|---|---|---|---|---|
| Python | 27 | 27 | 0 | 3 |
| Mathematics | 16 | 16 | 0 | 1 |
| Statistics | 16 | 17 | 3 | 2 |
| NumPy | 14 | 14 | 0 | 1 |
| pandas | 16 | 16 | 0 | 2 |
| FastAPI | 15 | 15 | 0 | 2 |
| Machine Learning | 14 | 19 | 8 | 3 |
| Deep Learning | 15 | 20 | 7 | 2 |
| Computer Vision | 14 | 18 | 8 | 3 |
| NLP | 13 | 14 | 5 | 2 |
| LLMs | 16 | 18 | 3 | 3 |
| Explainable AI | 12 | 12 | 2 | 1 |
| Federated Learning | 12 | 13 | 1 | 1 |
| Reinforcement Learning | 13 | 15 | 0 | 2 |
| Agentic AI | 13 | 16 | 4 | 3 |
| **Total** | **226** | **250** | **41** | **31** |

Graded steps after the revision: 250 required + 41 optional = 291. Every existing step survives.

## 3. Project ideas

A **project idea** is an ungraded page on the path, placed after the step that completes its
prerequisites. It uses only what has been taught so far.

Each project idea has:

* **Brief** — what to build and who would use it.
* **You will use** — links to the steps it draws on.
* **Milestones** — 4–6 suggested build steps, smallest working version first.
* **Stretch goals** — harder extensions.
* **Data** — synthetic data the student can generate, or a public dataset to download themselves
  (each link checked; never needed for graded work).
* **Run it yourself** — the packages to install locally (`pip install ...`) and how to start.

No editor, Run or Submit; not counted in the topic progress bar.

| After | Project idea | Draws on |
|---|---|---|
| PY files-and-json | **Expense tracker CLI** — add, list and summarise expenses saved to JSON | input, dicts, files, JSON |
| PY unit-testing | **Quiz game with high scores** — question bank in a file, scoring, tests | classes, files, exceptions, unittest |
| PY end of topic | **Text adventure engine** — rooms and items as classes, saved games | classes, inheritance, JSON |
| MA end of topic | **Gradient-descent visualiser** — step through descent on chosen functions | derivatives, gradient descent |
| ST permutation test | **A/B test analyser** — compare two groups, report effect, CI and p-value | bootstrap, tests, scipy.stats |
| ST end of topic | **Dice and coin simulator** — simulations that show the law of large numbers | simulation, distributions |
| NP end of topic | **Photo filters with NumPy** — greyscale, blur, edge, vignette on your own images | arrays, broadcasting, convolution |
| PD groupby/merge | **Exploratory analysis of a public dataset** — clean, group, chart, write findings | pandas end to end |
| PD end of topic | **Personal finance dashboard data** — monthly and category summaries from bank-style CSVs | dates, resample, pivot |
| FA dependencies | **URL shortener API** — create, redirect, stats, API-key auth, tests | FastAPI, Pydantic, dependencies |
| FA end of topic | **Notes or event-RSVP API** — CRUD, validation, async external call, test suite | FastAPI end to end |
| ML pipelines | **House-price predictor** — features, pipeline, cross-validation, error analysis | scikit-learn pipelines |
| ML end of topic | **Spam or fraud classifier** — imbalanced classes, thresholds, ROC/PR | metrics, boosting |
| ML + FastAPI | **Serve your model** — a FastAPI `/predict` endpoint with validation and tests | ML + FastAPI |
| DL training loop | **Handwritten digit recogniser** — train an MLP on MNIST locally | PyTorch training |
| DL end of topic | **Training diagnostics notebook** — learning-rate finder, curves, overfitting demo | debugging training |
| CV contours | **Document scanner** — find the page, warp to a flat view, threshold | OpenCV contours, warpAffine |
| CV CNN | **Shape and colour sorter** — classify objects from a webcam or photos | CNN, augmentation |
| CV end of topic | **Simple object counter** — count coins or cells with components and NMS | components, IoU, NMS |
| NL text pipeline | **Review sentiment analyser** — classify product or movie reviews | TF-IDF, logistic regression |
| NL end of topic | **Semantic search for the club blog** — search posts by meaning | TF-IDF, cosine, embeddings |
| LM tiny GPT | **Poem or name generator** — a character-level model on your own text | tiny GPT, sampling |
| LM RAG | **Course FAQ chatbot** — RAG over the curriculum's lessons with a local or hosted model | LangChain RAG |
| LM end of topic | **Prompt playground** — compare temperature, top-p and templates side by side | decoding, prompts |
| XA end of topic | **Explain your house-price model** — PDP, permutation importance, SHAP report | XAI + scikit-learn |
| FL end of topic | **Federated training across departments** — simulate clients with non-IID data; try Flower | FedAvg, PyTorch |
| RL FrozenLake | **Grid game agent** — design a small game and train a Q-learning agent | Gymnasium, Q-learning |
| RL end of topic | **Bandit-based recommender** — pick articles with UCB and measure regret | bandits |
| AG LangGraph agent | **Study-planner agent** — tools for a calendar file and notes, step limits | LangGraph, tools |
| AG guardrails | **Club event assistant** — answers FAQs, drafts announcements, asks before sending | guardrails, approval |
| AG end of topic | **Agent evaluation suite** — test cases and metrics for your own agent | evaluation |

### App changes for project ideas

* Pack `kind: "project"` with the fields above; no `starter`, `solution` or tests. The builder renders
  `project.md`; validation and the audit skip project ideas; links in "You will use" are checked.
* Catalogue and topic pages: a lightbulb icon instead of a checkbox, label "Project idea", excluded from
  "N problems" and from the progress bar (shown as "N project ideas").
* Project page: a reading layout (brief, milestones checklist that the student can tick locally,
  stretch goals, data and setup), no code editor.
* Optional deep dives: an "Optional" badge; not counted towards topic completion.

## 4. Libraries: where each runs

| Package | Pin | Browser (Pyodide 0.27.7) | VPS executor |
|---|---|---|---|
| NumPy / pandas | 2.2.6 / 2.2.3 (current) | yes | yes |
| SciPy | 1.14.1 | yes | yes |
| scikit-learn | 1.6.1 | yes | yes |
| OpenCV | `opencv-python-headless` 4.10.0.84 | yes (`opencv-python` 4.10) | yes |
| FastAPI + httpx | 0.162.0 + 0.28.1 (current) | no (FastAPI not in Pyodide) | yes |
| PyTorch | 2.14.1, CPU wheel | no | yes |
| `langchain-core` | 1.7.x | no | yes |
| LangGraph | 1.2.x | no (needs compiled `xxhash`, `ormsgpack`) | yes |
| Gymnasium | 1.x | no (not built in) | yes |

Every library runs in at least one place. Versions for SciPy, scikit-learn and OpenCV are pinned to the
ones Pyodide 0.27.7 ships, so browser Run and VPS grading agree.

## 5. VPS runtime: 2 vCPU, 4 GB RAM, 40 GB SSD

### Measured cost of importing libraries (peak memory and CPU, on an M-series Mac)

| Libraries | Memory | Import CPU |
|---|---|---|
| NumPy + pandas | ~90 MB | 0.6 s |
| + SciPy + scikit-learn | ~160 MB | 1.5 s |
| + PyTorch | ~310 MB | 2.6 s |
| FastAPI + TestClient | ~55 MB | 0.25 s |

Expect roughly 2–3× the CPU time on a VPS core. Without preloading, a Submit that uses PyTorch or
scikit-learn would spend most of its time importing.

### Design for about 100 students

* **One image** (`epoch-learn-runner`) with every executor library: Python 3.13, NumPy, pandas, FastAPI,
  httpx, SciPy, scikit-learn, OpenCV headless, PyTorch CPU, LangChain, LangGraph, Gymnasium. About
  1.3 GB on disk; keeping the previous version for rollback still uses under 3 GB of the 40 GB SSD.
  PyTorch must come from `https://download.pytorch.org/whl/cpu`; the default Linux wheel pulls several
  GB of CUDA libraries.
* **A fresh container for every submission.** Student code is untrusted. A container that runs one job
  and is then destroyed means no student's code can read the hidden tests or another submission,
  leave processes or files behind that affect the next result, or take the grader down for everyone.
* **A warm pool of 2 preloaded containers** so the fresh container costs almost nothing (below).

### Preloading with warm containers

The service keeps **2 containers already started, with the libraries imported**, each waiting for one
job on stdin:

1. At start, the runner imports NumPy, pandas, SciPy, scikit-learn, OpenCV, PyTorch, LangChain, LangGraph,
   Gymnasium and FastAPI, runs one tiny warm-up operation, then waits.
2. On a request, `service.py` takes a waiting container, sends the code and tests, reads the result, and
   the container exits.
3. A replacement starts in the background, so the pool is refilled for the next request.
4. The runner sets its CPU limit **after** the imports (current usage + the job's budget), so import time
   is not charged to the student's code.

Effect: a Submit no longer waits for `docker run` (~0.5–1 s) or imports (several seconds on the VPS); it
pays only for running the tests.

### Capacity and memory

Two jobs run at a time (one per vCPU); others wait in a short queue. Most graded tests take well under
2 s, so the executor handles roughly 40–60 submissions per minute — more than 100 students submitting
during the same lab session (typically a few per minute, bursts of 10–20).

| Item | Memory |
|---|---|
| OS, Docker, `service.py`, HTTPS proxy | ~0.7 GB |
| 2 warm containers waiting, libraries loaded (~450 MB each) | ~0.9 GB |
| 2 running jobs, limit 1 GB each | ≤ 2.0 GB |
| **Worst case** | **≈ 3.6 GB of 4 GB** |

Settings:

* **Concurrency:** 2 running jobs, `--cpus 1` each.
* **Queue:** replace today's immediate "Busy" response with a queue of up to 30 requests; a request
  waiting more than ~30 s gets "busy, try again". Run is lower priority than Submit.
* **Pool:** 2 warm containers; a replacement starts only when a job slot is free, so refilling never
  competes with running tests.
* **Per-job limits:** 1 GB memory (swap disabled per container), 10 s CPU for the student's code after
  imports, 30 s wall clock. Keep `--network none`, read-only root filesystem, `--pids-limit 64`.
* **Threads:** `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `torch.set_num_threads(1)`; deterministic and
  matched to `--cpus 1`.
* **Swap:** add a 2 GB swap file to the VPS as a safety margin for the host; containers cannot swap.
* **Measure first:** before content work, run every pack on the VPS and record time and memory; adjust the
  pool size, limits and queue length.

### Browser (Pyodide) preloading

* Start the Pyodide worker **when a problem page opens** (not on the first Run) and load that pack's
  packages in the background, with a "Preparing Python…" indicator.
* Keep the worker alive while the learner stays on the page and run each attempt in a fresh namespace;
  today a new worker (and package load) is created for every Run.
* Allow `scipy`, `scikit-learn` and `opencv-python` in the local allow-list and map
  `opencv-python-headless` → `opencv-python` for Pyodide.
* Packages are cached by the browser after the first download (tens of MB for scikit-learn/OpenCV).

## 6. Curriculum and tooling

* `build/path.py`: `IMPORT_INTRO` entries for each library's first step (`scipy` → Introducing
  scipy.stats, `sklearn` → estimator API, `torch` → PyTorch tensors, `cv2` → OpenCV basics,
  `langchain_core` → LangChain tools, `langgraph` → LangGraph basics, `gymnasium` → Gymnasium).
* New pack fields: `optional: true` for deep dives; `kind: "project"` for project ideas.
* Validation environments: `requirements-executor.txt` mirrors the single image; a second environment
  keeps current NumPy/pandas to catch version-specific behaviour.
* Library lessons include "What the library does inside" (link to the deep dive) and API-specific
  common mistakes (leakage outside a `Pipeline`, forgetting `model.eval()`, BGR order in OpenCV, mutating
  LangGraph state instead of returning updates).

## 7. Phases

| Phase | Work |
|---|---|
| 0 | Single image with all libraries, warm pool of 2 and queue in `service.py`, post-import CPU limits, VPS measurements, swap; Pyodide preloading and allow-list; `optional` and `project` support in builder, generator and UI |
| 1 | Statistics (SciPy) and Machine Learning (scikit-learn), with their project ideas |
| 2 | Deep Learning (PyTorch) |
| 3 | Computer Vision (OpenCV, PyTorch CNN) |
| 4 | NLP and LLMs (scikit-learn text, PyTorch, LangChain) |
| 5 | Agentic AI (LangChain, LangGraph) |
| 6 | Explainable AI, Federated Learning, Reinforcement Learning (Gymnasium); project ideas for Python, Maths, NumPy, pandas and FastAPI |

Each phase ends with full validation in both environments, the audit, regenerated app data, a run of
the affected packs on the VPS, and a check of the affected pages.

## 8. Risks

* Heavy-pack timings on the actual VPS may differ from the estimates; Phase 0 measures them.
* Warm containers cost memory while idle; the pool size is the main tuning knob.
* Training-based tests (CNN, tiny GPT, FrozenLake) must stay within a few seconds; assert trends, not
  exact values.
* LangChain and LangGraph change quickly; pin exact versions and use stable primitives.
* Browser and VPS versions still differ for NumPy (2.0.2 vs 2.2.6) and pandas; tests avoid
  version-specific behaviour.
