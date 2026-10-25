"""The single learning path: topic order, step order inside each topic, and audit maps.

Problem IDs are not stored in the topic modules. `build.py` assigns them from the order
below (PREFIX-01, PREFIX-02, ...), so reordering a list here renumbers the path. Problem text
refers to other problems as [[slug]]; the builder replaces each reference with the new ID.
"""

# (slug, display name, ID prefix, topic prerequisites, topic modules, one-line outcome)
TOPICS = [
    ("python", "Python", "PY", [], ["python_scripts", "python", "python_added", "python_projects"],
     "Write programs from print and input up to functions, collections, files, exceptions, modules, "
     "classes and unit tests."),
    ("mathematics", "Mathematics for AI/ML", "MA", ["python"], ["mathematics", "mathematics_added", "mathematics_projects"],
     "Use summation, exponentials, logarithms, the sigmoid, vectors, matrices, derivatives, the "
     "chain rule, integration, gradient descent, series and eigenvectors."),
    ("statistics", "Statistics", "ST", ["mathematics"], ["statistics", "statistics_added", "statistics_library"],
     "Describe data, reason with probability, conditional probability and Bayes' rule, use the "
     "binomial and normal distributions, simulate, and run interval estimates and hypothesis tests "
     "by hand and with scipy.stats."),
    ("numpy", "NumPy", "NP", ["statistics"], ["numpy_topic", "numpy_added", "numpy_projects"],
     "Replace Python loops with arrays: vectorised arithmetic, slicing, masks, reductions, matrix "
     "products, broadcasting, reshaping, gathers, seeded randomness and linear algebra."),
    ("pandas", "Pandas", "PD", ["numpy"], ["pandas_topic", "pandas_added", "pandas_projects"],
     "Load, inspect, clean, filter, group, merge, reshape and window tabular data, comparing each "
     "operation with its plain-Python equivalent."),
    ("fastapi", "FastAPI", "FA", ["python"], ["fastapi_basics", "fastapi_topic", "fastapi_projects"],
     "Understand HTTP messages, URLs, JSON and routing by hand, then build, validate, secure, run "
     "asynchronously and test FastAPI services."),
    ("machine-learning", "Machine Learning", "ML", ["pandas"], ["machine_learning", "machine_learning_added", "machine_learning_library"],
     "Build baselines and core models by hand, then use scikit-learn's estimator API, splits, "
     "pipelines, ColumnTransformer, cross-validation, grid search, trees, random forests, gradient "
     "boosting, ROC/PR thresholds and k-means in an end-to-end project."),
    ("deep-learning", "Deep Learning", "DL", ["machine-learning"], ["deep_learning", "deep_learning_added", "deep_learning_library"],
     "Understand neurons, activations, losses, backpropagation and optimisers in NumPy, then build, "
     "train, debug, save and reproduce PyTorch models with nn.Module, autograd, torch.optim, "
     "DataLoader, dropout, batch normalisation and Conv1d."),
    ("computer-vision", "Computer Vision", "CV", ["deep-learning"], ["computer_vision", "computer_vision_added", "computer_vision_library"],
     "Treat images as arrays, then process them with OpenCV (colour spaces, transforms, thresholds, "
     "histograms, edges, resizing, contours, connected components), train a small PyTorch CNN with "
     "augmentation, and post-process detections with IoU and NMS."),
    ("nlp", "Natural Language Processing", "NL", ["deep-learning"], ["nlp", "nlp_added", "nlp_library"],
     "Clean and tokenise text, count and vectorise it with CountVectorizer and TF-IDF, retrieve "
     "documents, compare strings, classify text with scikit-learn pipelines and error analysis, and "
     "learn word embeddings with PPMI and PyTorch."),
    ("llms", "Large Language Models", "LM", ["nlp", "deep-learning"], ["llms", "llms_added", "llms_library"],
     "Map text to tokens, model and decode next tokens, build attention and transformer blocks, "
     "train a tiny GPT in PyTorch, and build LangChain prompts, structured output and RAG pipelines "
     "with citation checks."),
    ("explainable-ai", "Explainable AI", "XA", ["computer-vision"], ["explainable_ai", "explainable_ai_library"],
     "Explain models with contributions, decision paths, ICE curves, scikit-learn partial dependence "
     "and permutation importance, occlusion, surrogates, Shapley values, LIME, counterfactuals and "
     "integrated gradients."),
    ("federated-learning", "Federated Learning", "FL", ["deep-learning"], ["federated_learning", "federated_learning_library"],
     "Simulate clients and partitions, train client copies of PyTorch models, aggregate state_dicts "
     "with weighted FedAvg, and add client sampling, clipping, secure aggregation, differential "
     "privacy and FedProx."),
    ("reinforcement-learning", "Reinforcement Learning", "RL", ["numpy"], ["reinforcement_learning", "reinforcement_learning_added", "reinforcement_learning_library"],
     "Define environments and returns (including Gymnasium environments), explore with bandits, "
     "solve MDPs with dynamic programming, and learn values with Monte Carlo, TD(0), Q-learning on "
     "FrozenLake and SARSA."),
    ("agentic-ai", "Agentic AI", "AG", ["llms"], ["agentic_ai", "agentic_ai_added", "agentic_ai_library"],
     "Build agent loops, parsing, budgets, ReAct, planners and evaluation by hand, then LangChain "
     "tools and LangGraph graphs with tool nodes, checkpointed memory, validated retries, "
     "orchestrator–workers and human-approval guardrails."),
]

# Recommended order inside each topic. Earlier steps never depend on later ones.
PATH = {
    "python": [
        # Part 1 - programs without functions (graded through stdout/stdin)
        "hello-print", "variables", "types-conversion", "input-output", "arithmetic-operators",
        "string-basics", "conditionals", "while-loops", "for-loops-range",
        # Part 2 - functions and collections (steps 10-18)
        "greeting-formatter", "sum-and-mean", "filter-evens", "vowel-counter",
        "fibonacci-sequence", "standard-library", "unique-words", "functions-as-values",
        "gradebook-aggregate",
        # Part 3 - robust programs (steps 19-27)
        "factorial-validated", "matrix-transpose", "safe-divide", "guessing-game-feedback", "files-and-json", "expense-tracker-cli",
        "text-stats-stdin", "bank-account", "shapes-inheritance", "unit-testing",
        "quiz-game", "text-adventure-engine",
    ],
    "mathematics": [
        "summation", "exp-log", "sigmoid-function", "dot-product", "vector-norm-unit",
        "matrix-multiply", "binomial-coefficient", "solve-2x2-cramer", "inverse-2x2",
        "central-difference", "derivative-rules", "trapezoid-rule", "gradient-descent-1d",
        "numerical-gradient", "taylor-exp", "power-iteration", "gradient-descent-visualiser",
    ],
    "statistics": [
        "mean-variance", "median-mode", "percentiles", "histogram-bins", "z-scores",
        "probability-basics", "conditional-bayes", "binomial-pmf", "normal-distribution",
        "dice-lln", "covariance-correlation", "sampling-distribution", "bootstrap-ci",
        # scipy.stats; each by-hand test follows its library step as an optional deep dive
        "scipy-stats-intro", "chi-square-scipy", "chi-square-gof", "welch-t-scipy", "welch-t",
        "permutation-test-scipy", "permutation-test", "ab-test-analyser", "dice-coin-simulator",
    ],
    "numpy": [
        "array-info", "vectorized-math", "slicing-subgrid", "boolean-mask", "axis-aggregations",
        "matmul-dot", "broadcast-center", "reshape-stack", "fancy-indexing", "seeded-generator",
        "pairwise-distances", "linalg-solve", "one-hot", "moving-average", "numpy-photo-filters",
    ],
    "pandas": [
        "series-basics", "dataframe-basics", "read-csv-io", "select-filter", "derived-columns",
        "missing-values", "sort-rank", "groupby-agg", "fill-missing-group", "merge-tables",
        "public-dataset-eda",
        "string-cleaning", "datetime-basics", "resample-weekly", "pivot-table", "binning-cut",
        "rolling-features", "personal-finance-data",
    ],
    "machine-learning": [
        # Understand a model by hand, then use scikit-learn; by-hand versions of library steps
        # follow them as optional deep dives.
        "ml-baselines", "sklearn-estimator-api", "regression-metrics",
        "sklearn-train-test-split", "train-test-split", "classification-metrics",
        "sklearn-scaler-pipeline", "standard-scaler", "least-squares-line", "linreg-gradient-descent",
        "logistic-regression", "sklearn-knn", "knn-classifier",
        "sklearn-polynomial-validation", "polynomial-overfitting", "sklearn-cross-validation", "k-fold-cv",
        "sklearn-column-transformer", "house-price-predictor", "sklearn-grid-search", "ridge-regression",
        "decision-stump-gini", "sklearn-trees-forests", "sklearn-gradient-boosting", "sklearn-roc-pr",
        "sklearn-kmeans", "kmeans", "ml-capstone", "spam-fraud-classifier", "serve-your-model",
    ],
    "deep-learning": [
        # Each concept by hand, then PyTorch; NumPy versions of library steps follow them as
        # optional deep dives.
        "activations", "stable-softmax", "cross-entropy", "dense-forward",
        "torch-tensors", "torch-mlp-module", "mlp-forward",
        "scalar-autograd", "torch-autograd", "neuron-backprop", "dense-backward",
        "torch-gradcheck", "gradient-check", "sgd-momentum", "torch-optimizers", "adam-optimizer",
        "torch-datasets", "torch-training-loop", "train-xor-mlp", "digit-recogniser",
        "torch-dropout", "inverted-dropout", "torch-batchnorm", "batchnorm-forward",
        "torch-conv1d", "conv1d", "torch-save-load", "torch-debugging", "training-diagnostics",
    ],
    "computer-vision": [
        # NumPy foundations, then OpenCV and PyTorch; NumPy versions of library steps follow them
        # as optional deep dives.
        "image-arrays", "rgb-to-gray", "cv-opencv-basics", "cv-geometric-transforms", "flip-rotate",
        "cv-threshold-otsu", "threshold-binary", "cv-histograms", "intensity-histogram",
        "conv2d-filter", "cv-sobel-canny", "sobel-edges", "cv-pooling-torch", "max-pool-2d",
        "conv2d-layer", "cv-psnr", "psnr", "cv-resize", "bilinear-resize",
        "cv-contours", "document-scanner", "cv-small-cnn", "cv-augmentation", "shape-sorter",
        "iou", "non-max-suppression", "cv-connected-components", "connected-components", "object-counter",
    ],
    "nlp": [
        # By-hand text processing, then scikit-learn and PyTorch; by-hand versions of library
        # steps follow them as optional deep dives.
        "regex-text", "tokenize-normalize", "nlp-countvectorizer", "stopword-counts",
        "nlp-char-ngrams-sklearn", "char-ngrams", "bag-of-words", "bigram-counts", "tf-idf",
        "nlp-tfidf-retrieval", "cosine-retrieval", "levenshtein", "suffix-stemmer",
        "naive-bayes-text", "nlp-text-classifier", "review-sentiment-analyser", "nlp-error-analysis",
        "ppmi-matrix", "embedding-analogy", "nlp-embedding-bag", "blog-semantic-search",
    ],
    "llms": [
        "token-ids", "bigram-next-token", "temperature-softmax", "greedy-decoding", "perplexity",
        "bpe-merges", "scaled-dot-attention", "causal-mask", "positional-encoding",
        "multi-head-attention", "lm-transformer-module", "transformer-block", "top-k-top-p",
        "beam-search", "kv-cache", "lm-tiny-gpt", "poem-name-generator",
        "lm-chat-prompt-langchain", "chat-prompt", "lm-structured-output",
        "lm-langchain-rag", "rag-pipeline", "course-faq-chatbot", "prompt-playground",
    ],
    "explainable-ai": [
        "linear-contributions", "top-k-attributions", "decision-path", "ice-curve",
        "xai-partial-dependence", "partial-dependence", "xai-permutation-importance",
        "permutation-importance", "occlusion-saliency", "surrogate-fidelity", "exact-shapley",
        "lime-local", "counterfactual-search", "integrated-gradients", "explain-house-prices",
    ],
    "federated-learning": [
        "iid-partition", "weighted-fedavg", "client-delta", "label-skew-partition",
        "fl-torch-local-training", "local-sgd", "fedavg-round", "client-sampling", "update-clipping",
        "fedavg-training", "fl-torch-fedavg", "secure-aggregation", "dp-aggregation", "fedprox",
        "federated-departments",
    ],
    "reinforcement-learning": [
        "discounted-return", "gridworld-step", "env-interface", "rl-gymnasium-env", "epsilon-greedy",
        "bandit-incremental", "ucb-bandit", "policy-evaluation", "value-iteration",
        "policy-iteration", "mc-first-visit", "td0-prediction", "q-learning", "rl-frozenlake-q",
        "sarsa", "grid-game-agent", "bandit-recommender",
    ],
    "agentic-ai": [
        # Agent loops by hand, then LangChain tools and LangGraph graphs; by-hand versions of
        # library steps follow them as optional deep dives.
        "tool-registry", "parse-tool-call", "ag-langchain-tools", "reflex-agent-loop", "goal-and-budget",
        "react-loop", "ag-langgraph-basics", "ag-langgraph-react", "ag-message-memory", "memory-window",
        "bfs-planner", "a-star-planner", "task-dag-plan", "study-planner-agent",
        "ag-validate-retry", "validate-and-retry", "ag-orchestrator-graph", "orchestrator-workers",
        "ag-approval-guardrails", "permission-guardrails", "club-event-assistant",
        "agent-evaluation", "agent-evaluation-suite",
    ],
    "fastapi": [
        "http-requests", "http-responses", "urls-query", "json-bodies", "manual-router",
        "asyncio-basics", "asgi-app", "fastapi-routes", "fastapi-params", "pydantic-bodies",
        "fastapi-errors", "response-models", "fastapi-dependencies", "url-shortener-api",
        "fastapi-async", "api-testing", "notes-rsvp-api",
    ],
}

# ---------------------------------------------------------------- "taught before used" audit
# The audit parses every starter.py and solution.py and checks that each Python construct or
# import it contains was introduced at this step or earlier in the path. Keys are produced by
# reports.py's feature extractor; values are the slugs whose lesson introduces them.
FEATURE_INTRO = {
    "print": "hello-print",
    "assignment": "variables",
    "f-string": "variables",
    "conversion": "types-conversion",
    "input": "input-output",
    "arithmetic": "arithmetic-operators",
    "subscript": "string-basics",
    "if": "conditionals",
    "boolean-logic": "conditionals",
    "while": "while-loops",
    "for": "for-loops-range",
    "def": "greeting-formatter",
    "list": "sum-and-mean",
    "comprehension": "filter-evens",
    "generator-expression": "filter-evens",
    "dict": "vowel-counter",
    "tuple-unpacking": "fibonacci-sequence",
    "import": "standard-library",
    "set": "unique-words",
    "lambda": "functions-as-values",
    "varargs": "functions-as-values",
    "keyword-only": "functions-as-values",
    "decorator": "functions-as-values",
    "nested-function": "functions-as-values",
    "raise": "factorial-validated",
    "try": "safe-divide",
    "with": "files-and-json",
    "class": "bank-account",
    "inheritance": "shapes-inheritance",
    "async": "asyncio-basics",
    "yield": "fastapi-dependencies",
    "matmul": "matmul-dot",
}

IMPORT_INTRO = {
    "math": "standard-library", "random": "standard-library", "string": "standard-library",
    "collections": "standard-library", "itertools": "standard-library",
    "heapq": "standard-library", "functools": "standard-library",
    "statistics": "standard-library", "copy": "standard-library",
    "json": "files-and-json", "csv": "files-and-json", "pathlib": "files-and-json",
    "os": "files-and-json", "io": "files-and-json",
    "sys": "text-stats-stdin",
    "dataclasses": "shapes-inheritance", "typing": "shapes-inheritance",
    "unittest": "unit-testing",
    "fractions": "probability-basics", "datetime": "datetime-basics",
    "numpy": "array-info",
    "pandas": "series-basics",
    "re": "regex-text", "unicodedata": "tokenize-normalize",
    "http": "http-responses", "urllib": "urls-query",
    "asyncio": "asyncio-basics", "enum": "fastapi-params", "hashlib": "response-models",
    "fastapi": "fastapi-routes", "pydantic": "pydantic-bodies", "starlette": "fastapi-routes",
    "scipy": "scipy-stats-intro", "sklearn": "sklearn-estimator-api", "torch": "torch-tensors", "cv2": "cv-opencv-basics", "langchain_core": "lm-chat-prompt-langchain", "langgraph": "ag-langgraph-basics", "operator": "ag-langgraph-basics", "gymnasium": "rl-gymnasium-env",
}

# Library calls that have their own lesson. Attribute names are matched on `np.` / DataFrame
# method calls in solutions; a call before its lesson is reported as a violation.
LIBRARY_INTRO = {
    "default_rng": "seeded-generator",
    "linalg": "linalg-solve",
    "sliding_window_view": "moving-average",
    "read_csv": "read-csv-io",
    "groupby": "groupby-agg",
    "merge": "merge-tables",
    "pivot_table": "pivot-table",
    "melt": "pivot-table",
    "resample": "resample-weekly",
    "rolling": "rolling-features",
    "cut": "binning-cut",
    "to_datetime": "datetime-basics",
    "fillna": "missing-values",
    "dropna": "missing-values",
    "isna": "missing-values",
}
