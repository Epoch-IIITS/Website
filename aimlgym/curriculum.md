# AIML Gym Curriculum

291 graded steps (41 of them optional deep dives) and 31 ungraded project ideas in 15 topics for UG1/UG2 learners, arranged as one path that starts from zero Python. Every step has a lesson (outcomes, explanation, worked example, common mistakes, references) and a graded exercise (starter, three progressive hints, reference solution, failure feedback and at least six deterministic tests). Core exercises run on a CPU without network access, GPUs, paid APIs or downloads.

## How to work through a step

```bash
cd topics/python/hello-print
# read article.md and problem.md, edit starter.py, then:
AIMLGYM_TARGET=starter python -m unittest tests -v
```

Python 3.10+ is required (validated on 3.13). Install `build/requirements-executor.txt` (NumPy, pandas, SciPy, scikit-learn, OpenCV, PyTorch CPU, FastAPI, httpx, LangChain Core, LangGraph, Gymnasium) to run every step. Optional deep dives are graded but do not count towards topic completion; project ideas are ungraded briefs (`project.md`).

## The learning sequence

| # | Topic | Prefix | Steps | Topic prerequisites | You will be able to |
|---|---|---|---|---|---|
| 1 | [Python](topics/python/overview.md) | PY | 27 | — | Write programs from print and input up to functions, collections, files, exceptions, modules, classes and unit tests. |
| 2 | [Mathematics for AI/ML](topics/mathematics/overview.md) | MA | 16 | Python | Use summation, exponentials, logarithms, the sigmoid, vectors, matrices, derivatives, the chain rule, integration, gradient descent, series and eigenvectors. |
| 3 | [Statistics](topics/statistics/overview.md) | ST | 20 | Mathematics for AI/ML | Describe data, reason with probability, conditional probability and Bayes' rule, use the binomial and normal distributions, simulate, and run interval estimates and hypothesis tests by hand and with scipy.stats. |
| 4 | [NumPy](topics/numpy/overview.md) | NP | 14 | Statistics | Replace Python loops with arrays: vectorised arithmetic, slicing, masks, reductions, matrix products, broadcasting, reshaping, gathers, seeded randomness and linear algebra. |
| 5 | [Pandas](topics/pandas/overview.md) | PD | 16 | NumPy | Load, inspect, clean, filter, group, merge, reshape and window tabular data, comparing each operation with its plain-Python equivalent. |
| 6 | [FastAPI](topics/fastapi/overview.md) | FA | 15 | Python | Understand HTTP messages, URLs, JSON and routing by hand, then build, validate, secure, run asynchronously and test FastAPI services. |
| 7 | [Machine Learning](topics/machine-learning/overview.md) | ML | 27 | Pandas | Build baselines and core models by hand, then use scikit-learn's estimator API, splits, pipelines, ColumnTransformer, cross-validation, grid search, trees, random forests, gradient boosting, ROC/PR thresholds and k-means in an end-to-end project. |
| 8 | [Deep Learning](topics/deep-learning/overview.md) | DL | 27 | Machine Learning | Understand neurons, activations, losses, backpropagation and optimisers in NumPy, then build, train, debug, save and reproduce PyTorch models with nn.Module, autograd, torch.optim, DataLoader, dropout, batch normalisation and Conv1d. |
| 9 | [Computer Vision](topics/computer-vision/overview.md) | CV | 26 | Deep Learning | Treat images as arrays, then process them with OpenCV (colour spaces, transforms, thresholds, histograms, edges, resizing, contours, connected components), train a small PyTorch CNN with augmentation, and post-process detections with IoU and NMS. |
| 10 | [Natural Language Processing](topics/nlp/overview.md) | NL | 19 | Deep Learning | Clean and tokenise text, count and vectorise it with CountVectorizer and TF-IDF, retrieve documents, compare strings, classify text with scikit-learn pipelines and error analysis, and learn word embeddings with PPMI and PyTorch. |
| 11 | [Large Language Models](topics/llms/overview.md) | LM | 21 | Natural Language Processing, Deep Learning | Map text to tokens, model and decode next tokens, build attention and transformer blocks, train a tiny GPT in PyTorch, and build LangChain prompts, structured output and RAG pipelines with citation checks. |
| 12 | [Explainable AI](topics/explainable-ai/overview.md) | XA | 14 | Computer Vision | Explain models with contributions, decision paths, ICE curves, scikit-learn partial dependence and permutation importance, occlusion, surrogates, Shapley values, LIME, counterfactuals and integrated gradients. |
| 13 | [Federated Learning](topics/federated-learning/overview.md) | FL | 14 | Deep Learning | Simulate clients and partitions, train client copies of PyTorch models, aggregate state_dicts with weighted FedAvg, and add client sampling, clipping, secure aggregation, differential privacy and FedProx. |
| 14 | [Reinforcement Learning](topics/reinforcement-learning/overview.md) | RL | 15 | NumPy | Define environments and returns (including Gymnasium environments), explore with bandits, solve MDPs with dynamic programming, and learn values with Monte Carlo, TD(0), Q-learning on FrozenLake and SARSA. |
| 15 | [Agentic AI](topics/agentic-ai/overview.md) | AG | 20 | Large Language Models | Build agent loops, parsing, budgets, ReAct, planners and evaluation by hand, then LangChain tools and LangGraph graphs with tool nodes, checkpointed memory, validated retries, orchestrator–workers and human-approval guardrails. |

### PY · Python

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| PY-01 | [Hello, print()](topics/python/hello-print/problem.md) | beginner | — | 8 |  |
| PY-02 | [Variables and f-strings](topics/python/variables/problem.md) | beginner | PY-01 | 6 |  |
| PY-03 | [Types and Conversion](topics/python/types-conversion/problem.md) | beginner | PY-02 | 6 |  |
| PY-04 | [Reading Input](topics/python/input-output/problem.md) | beginner | PY-03 | 6 |  |
| PY-05 | [Arithmetic Operators](topics/python/arithmetic-operators/problem.md) | beginner | PY-04 | 7 |  |
| PY-06 | [Strings: Indexing, Slicing and Methods](topics/python/string-basics/problem.md) | beginner | PY-05 | 7 |  |
| PY-07 | [Conditionals: Letter Grades](topics/python/conditionals/problem.md) | beginner | PY-06 | 7 |  |
| PY-08 | [While Loops: Read Until Done](topics/python/while-loops/problem.md) | beginner | PY-07 | 6 |  |
| PY-09 | [For Loops and range: FizzBuzz](topics/python/for-loops-range/problem.md) | beginner | PY-08 | 6 |  |
| PY-10 | [Greeting Formatter](topics/python/greeting-formatter/problem.md) | beginner | PY-09 | 7 |  |
| PY-11 | [Sum and Mean of a List](topics/python/sum-and-mean/problem.md) | beginner | PY-10 | 8 | yes |
| PY-12 | [Filter Even Numbers](topics/python/filter-evens/problem.md) | beginner | PY-11 | 7 |  |
| PY-13 | [Vowel Counter](topics/python/vowel-counter/problem.md) | beginner | PY-12 | 6 |  |
| PY-14 | [Fibonacci Sequence](topics/python/fibonacci-sequence/problem.md) | intermediate | PY-13 | 7 |  |
| PY-15 | [Importing the Standard Library](topics/python/standard-library/problem.md) | intermediate | PY-14 | 8 |  |
| PY-16 | [Unique Words in Order](topics/python/unique-words/problem.md) | intermediate | PY-15 | 8 | yes |
| PY-17 | [Functions as Values](topics/python/functions-as-values/problem.md) | intermediate | PY-16 | 7 |  |
| PY-18 | [Gradebook Aggregation](topics/python/gradebook-aggregate/problem.md) | intermediate | PY-17 | 7 |  |
| PY-19 | [Validated Factorial](topics/python/factorial-validated/problem.md) | intermediate | PY-18 | 8 | yes |
| PY-20 | [Matrix Transpose with Validation](topics/python/matrix-transpose/problem.md) | intermediate | PY-19 | 9 | yes |
| PY-21 | [Safe Division with Exceptions](topics/python/safe-divide/problem.md) | intermediate | PY-20 | 8 |  |
| PY-22 | [Guessing Game Feedback](topics/python/guessing-game-feedback/problem.md) | advanced | PY-21 | 7 |  |
| PY-23 | [Files, CSV and JSON](topics/python/files-and-json/problem.md) | advanced | PY-22 | 7 |  |
| PY-24 | [Text Statistics from stdin](topics/python/text-stats-stdin/problem.md) | advanced | PY-23 | 7 |  |
| PY-25 | [Classes: A Bank Account](topics/python/bank-account/problem.md) | advanced | PY-24 | 7 |  |
| PY-26 | [Inheritance, Special Methods and Dataclasses](topics/python/shapes-inheritance/problem.md) | advanced | PY-25 | 7 |  |
| PY-27 | [Writing Unit Tests](topics/python/unit-testing/problem.md) | advanced | PY-26 | 8 |  |

### MA · Mathematics for AI/ML

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| MA-01 | [Summation and Product Notation](topics/mathematics/summation/problem.md) | beginner | PY-17 | 8 | yes |
| MA-02 | [Exponentials and Logarithms](topics/mathematics/exp-log/problem.md) | beginner | MA-01 | 10 | yes |
| MA-03 | [The Sigmoid Function](topics/mathematics/sigmoid-function/problem.md) | beginner | MA-02 | 7 | yes |
| MA-04 | [Dot Product](topics/mathematics/dot-product/problem.md) | beginner | MA-01 | 7 |  |
| MA-05 | [Vector Norm and Unit Vector](topics/mathematics/vector-norm-unit/problem.md) | beginner | MA-04 | 8 |  |
| MA-06 | [Matrix Multiplication](topics/mathematics/matrix-multiply/problem.md) | beginner | MA-04, PY-20 | 8 |  |
| MA-07 | [Binomial Coefficient](topics/mathematics/binomial-coefficient/problem.md) | intermediate | MA-01, PY-19 | 9 | yes |
| MA-08 | [Solve a 2x2 System (Cramer's Rule)](topics/mathematics/solve-2x2-cramer/problem.md) | intermediate | MA-06 | 7 |  |
| MA-09 | [Inverse of a 2x2 Matrix](topics/mathematics/inverse-2x2/problem.md) | intermediate | MA-08 | 7 |  |
| MA-10 | [Numerical Derivative (Central Difference)](topics/mathematics/central-difference/problem.md) | intermediate | MA-02 | 7 |  |
| MA-11 | [Derivative Rules and the Chain Rule](topics/mathematics/derivative-rules/problem.md) | intermediate | MA-10, MA-03 | 7 |  |
| MA-12 | [Trapezoidal Integration](topics/mathematics/trapezoid-rule/problem.md) | intermediate | MA-10 | 8 | yes |
| MA-13 | [Gradient Descent in 1D](topics/mathematics/gradient-descent-1d/problem.md) | advanced | MA-11 | 8 |  |
| MA-14 | [Numerical Gradient of f(x1..xn)](topics/mathematics/numerical-gradient/problem.md) | advanced | MA-10, MA-13 | 7 |  |
| MA-15 | [Taylor Series for exp(x)](topics/mathematics/taylor-exp/problem.md) | advanced | MA-11, MA-07 | 9 |  |
| MA-16 | [Dominant Eigenvalue by Power Iteration](topics/mathematics/power-iteration/problem.md) | advanced | MA-05, MA-06 | 9 | yes |

### ST · Statistics

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| ST-01 | [Mean and Variance (Population vs Sample)](topics/statistics/mean-variance/problem.md) | beginner | MA-01 | 8 | yes |
| ST-02 | [Median and Mode](topics/statistics/median-mode/problem.md) | beginner | ST-01 | 9 | yes |
| ST-03 | [Percentiles by Linear Interpolation](topics/statistics/percentiles/problem.md) | beginner | ST-02 | 9 | yes |
| ST-04 | [Histogram with Equal-Width Bins](topics/statistics/histogram-bins/problem.md) | beginner | ST-01 | 9 | yes |
| ST-05 | [Standardize to z-scores](topics/statistics/z-scores/problem.md) | beginner | ST-01 | 7 |  |
| ST-06 | [Probability by Counting Outcomes](topics/statistics/probability-basics/problem.md) | intermediate | ST-04 | 8 | yes |
| ST-07 | [Conditional Probability and Bayes' Rule](topics/statistics/conditional-bayes/problem.md) | intermediate | ST-06 | 7 |  |
| ST-08 | [Binomial Probabilities](topics/statistics/binomial-pmf/problem.md) | intermediate | ST-06, MA-07 | 10 | yes |
| ST-09 | [The Normal Distribution](topics/statistics/normal-distribution/problem.md) | intermediate | ST-05, ST-08 | 8 | yes |
| ST-10 | [Dice Simulation and the Law of Large Numbers](topics/statistics/dice-lln/problem.md) | intermediate | ST-06 | 8 |  |
| ST-11 | [Covariance and Pearson Correlation](topics/statistics/covariance-correlation/problem.md) | intermediate | ST-05, MA-04 | 10 | yes |
| ST-12 | [Sampling Distributions and Standard Error](topics/statistics/sampling-distribution/problem.md) | advanced | ST-10, ST-09 | 8 | yes |
| ST-13 | [Bootstrap Confidence Interval](topics/statistics/bootstrap-ci/problem.md) | advanced | ST-12, ST-03 | 8 | yes |
| ST-14 | [Introducing scipy.stats](topics/statistics/scipy-stats-intro/problem.md) | advanced | ST-09 | 6 |  |
| ST-15 | [Chi-Square Test with SciPy](topics/statistics/chi-square-scipy/problem.md) | advanced | ST-14 | 6 |  |
| ST-16 | [Chi-Square Goodness of Fit by Hand](topics/statistics/chi-square-gof/problem.md) | advanced | ST-08 | 8 | yes |
| ST-17 | [Welch's t-test with SciPy](topics/statistics/welch-t-scipy/problem.md) | advanced | ST-15, ST-12 | 6 |  |
| ST-18 | [Welch's t-statistic by Hand](topics/statistics/welch-t/problem.md) | advanced | ST-12 | 8 | yes |
| ST-19 | [Permutation Test with SciPy](topics/statistics/permutation-test-scipy/problem.md) | advanced | ST-17 | 6 |  |
| ST-20 | [Permutation Test for a Mean Difference by Hand](topics/statistics/permutation-test/problem.md) | advanced | ST-13, ST-18 | 7 |  |

### NP · NumPy

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| NP-01 | [Create an Array and Inspect It](topics/numpy/array-info/problem.md) | beginner | PY-20 | 7 |  |
| NP-02 | [Vectorised Arithmetic and ufuncs](topics/numpy/vectorized-math/problem.md) | beginner | NP-01, MA-03 | 9 | yes |
| NP-03 | [Slicing a Sub-grid](topics/numpy/slicing-subgrid/problem.md) | beginner | NP-01 | 7 |  |
| NP-04 | [Boolean Masks](topics/numpy/boolean-mask/problem.md) | beginner | NP-03 | 8 |  |
| NP-05 | [Aggregations Along Axes](topics/numpy/axis-aggregations/problem.md) | beginner | NP-02 | 7 |  |
| NP-06 | [Matrix Products with @](topics/numpy/matmul-dot/problem.md) | intermediate | NP-05, MA-06 | 8 | yes |
| NP-07 | [Centering Columns with Broadcasting](topics/numpy/broadcast-center/problem.md) | intermediate | NP-05, ST-05 | 8 |  |
| NP-08 | [Reshape and Stack](topics/numpy/reshape-stack/problem.md) | intermediate | NP-03 | 7 |  |
| NP-09 | [Fancy Indexing and Gather](topics/numpy/fancy-indexing/problem.md) | intermediate | NP-04, NP-05 | 7 |  |
| NP-10 | [Seeded Random Generators](topics/numpy/seeded-generator/problem.md) | intermediate | NP-09, ST-10 | 7 |  |
| NP-11 | [Vectorized Pairwise Distances](topics/numpy/pairwise-distances/problem.md) | advanced | NP-07, NP-06 | 9 | yes |
| NP-12 | [Solve Linear Systems Safely](topics/numpy/linalg-solve/problem.md) | advanced | NP-06, MA-08 | 10 | yes |
| NP-13 | [One-Hot Encoding](topics/numpy/one-hot/problem.md) | advanced | NP-09 | 9 | yes |
| NP-14 | [Moving Average with cumsum](topics/numpy/moving-average/problem.md) | advanced | NP-08 | 8 | yes |

### PD · Pandas

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| PD-01 | [Series: Labelled Columns](topics/pandas/series-basics/problem.md) | beginner | NP-04 | 6 |  |
| PD-02 | [Build and Describe a DataFrame](topics/pandas/dataframe-basics/problem.md) | beginner | PD-01 | 6 |  |
| PD-03 | [Reading and Writing CSV](topics/pandas/read-csv-io/problem.md) | beginner | PD-02, PY-23 | 6 |  |
| PD-04 | [Select and Filter Rows](topics/pandas/select-filter/problem.md) | beginner | PD-03 | 7 |  |
| PD-05 | [Derived Columns](topics/pandas/derived-columns/problem.md) | beginner | PD-04 | 7 |  |
| PD-06 | [Finding and Handling Missing Values](topics/pandas/missing-values/problem.md) | beginner | PD-05 | 6 |  |
| PD-07 | [Sort and Rank](topics/pandas/sort-rank/problem.md) | intermediate | PD-06 | 7 |  |
| PD-08 | [Group-by Aggregation](topics/pandas/groupby-agg/problem.md) | intermediate | PD-07, PY-18 | 7 | yes |
| PD-09 | [Fill Missing Values by Group](topics/pandas/fill-missing-group/problem.md) | intermediate | PD-08 | 7 |  |
| PD-10 | [Merging Tables](topics/pandas/merge-tables/problem.md) | intermediate | PD-08 | 8 | yes |
| PD-11 | [Cleaning Text Columns](topics/pandas/string-cleaning/problem.md) | intermediate | PD-06 | 7 |  |
| PD-12 | [Working with Dates](topics/pandas/datetime-basics/problem.md) | intermediate | PD-11 | 6 |  |
| PD-13 | [Weekly Resampling](topics/pandas/resample-weekly/problem.md) | advanced | PD-12, PD-08 | 7 |  |
| PD-14 | [Pivot Tables](topics/pandas/pivot-table/problem.md) | advanced | PD-08 | 6 |  |
| PD-15 | [Binning with pd.cut](topics/pandas/binning-cut/problem.md) | advanced | PD-08, ST-04 | 6 |  |
| PD-16 | [Rolling-Window Features](topics/pandas/rolling-features/problem.md) | advanced | PD-13, NP-14 | 7 |  |

### FA · FastAPI

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| FA-01 | [Anatomy of an HTTP Request](topics/fastapi/http-requests/problem.md) | beginner | PY-23 | 7 | yes |
| FA-02 | [HTTP Responses and Status Codes](topics/fastapi/http-responses/problem.md) | beginner | FA-01 | 7 | yes |
| FA-03 | [URLs, Paths and Query Strings](topics/fastapi/urls-query/problem.md) | beginner | FA-02 | 9 | yes |
| FA-04 | [JSON Request Bodies and Validation](topics/fastapi/json-bodies/problem.md) | intermediate | FA-03 | 7 |  |
| FA-05 | [A Router by Hand](topics/fastapi/manual-router/problem.md) | intermediate | FA-04 | 7 |  |
| FA-06 | [async and await with asyncio](topics/fastapi/asyncio-basics/problem.md) | intermediate | FA-05 | 6 |  |
| FA-07 | [A Minimal ASGI Application](topics/fastapi/asgi-app/problem.md) | intermediate | FA-06 | 6 |  |
| FA-08 | [First FastAPI Routes](topics/fastapi/fastapi-routes/problem.md) | intermediate | FA-07 | 7 | yes |
| FA-09 | [Query and Path Parameters with Validation](topics/fastapi/fastapi-params/problem.md) | intermediate | FA-08 | 6 |  |
| FA-10 | [Request Bodies with Pydantic](topics/fastapi/pydantic-bodies/problem.md) | intermediate | FA-09, FA-04 | 7 | yes |
| FA-11 | [Handling Errors in FastAPI](topics/fastapi/fastapi-errors/problem.md) | intermediate | FA-10 | 7 |  |
| FA-12 | [Response Models and Status Codes](topics/fastapi/response-models/problem.md) | advanced | FA-11 | 6 |  |
| FA-13 | [Dependencies and Dependency Overrides](topics/fastapi/fastapi-dependencies/problem.md) | advanced | FA-12 | 7 |  |
| FA-14 | [Async Endpoints and External Services](topics/fastapi/fastapi-async/problem.md) | advanced | FA-13, FA-06 | 7 |  |
| FA-15 | [Testing an API](topics/fastapi/api-testing/problem.md) | advanced | FA-14, PY-27 | 8 |  |

### ML · Machine Learning

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| ML-01 | [Features, Labels and Baseline Models](topics/machine-learning/ml-baselines/problem.md) | beginner | NP-05 | 9 | yes |
| ML-02 | [The scikit-learn Estimator API](topics/machine-learning/sklearn-estimator-api/problem.md) | beginner | ML-01 | 6 |  |
| ML-03 | [Regression Metrics](topics/machine-learning/regression-metrics/problem.md) | beginner | ML-01 | 8 | yes |
| ML-04 | [Splitting Data with scikit-learn](topics/machine-learning/sklearn-train-test-split/problem.md) | beginner | ML-02 | 6 |  |
| ML-05 | [Seeded Train/Test Split](topics/machine-learning/train-test-split/problem.md) | beginner | ML-01, NP-10 | 8 | yes |
| ML-06 | [Confusion Matrix, Precision, Recall, F1](topics/machine-learning/classification-metrics/problem.md) | beginner | ML-01 | 8 | yes |
| ML-07 | [Scaling inside a Pipeline](topics/machine-learning/sklearn-scaler-pipeline/problem.md) | beginner | ML-04 | 6 |  |
| ML-08 | [Standard Scaler (fit on train only)](topics/machine-learning/standard-scaler/problem.md) | beginner | ML-05 | 8 | yes |
| ML-09 | [Least-Squares Line](topics/machine-learning/least-squares-line/problem.md) | intermediate | ML-02, ST-11 | 9 | yes |
| ML-10 | [Linear Regression by Gradient Descent](topics/machine-learning/linreg-gradient-descent/problem.md) | intermediate | ML-09, MA-14 | 6 |  |
| ML-11 | [Logistic Regression from Scratch](topics/machine-learning/logistic-regression/problem.md) | intermediate | ML-10, MA-03 | 9 | yes |
| ML-12 | [k-Nearest Neighbours with scikit-learn](topics/machine-learning/sklearn-knn/problem.md) | intermediate | ML-07, ML-11 | 6 |  |
| ML-13 | [k-Nearest Neighbors Classifier by Hand](topics/machine-learning/knn-classifier/problem.md) | intermediate | ML-06, NP-11 | 9 | yes |
| ML-14 | [Polynomial Features and Validation Curves](topics/machine-learning/sklearn-polynomial-validation/problem.md) | intermediate | ML-12, ML-10 | 6 |  |
| ML-15 | [Polynomial Features and Overfitting by Hand](topics/machine-learning/polynomial-overfitting/problem.md) | intermediate | ML-09, ML-05 | 8 | yes |
| ML-16 | [Cross-Validation with scikit-learn](topics/machine-learning/sklearn-cross-validation/problem.md) | intermediate | ML-14 | 6 |  |
| ML-17 | [k-Fold Cross-Validation by Hand](topics/machine-learning/k-fold-cv/problem.md) | advanced | ML-15 | 8 | yes |
| ML-18 | [Pipelines and ColumnTransformer](topics/machine-learning/sklearn-column-transformer/problem.md) | intermediate | ML-16 | 6 |  |
| ML-19 | [Regularisation and Hyperparameter Search](topics/machine-learning/sklearn-grid-search/problem.md) | advanced | ML-18 | 6 |  |
| ML-20 | [Ridge Regression (Closed Form)](topics/machine-learning/ridge-regression/problem.md) | advanced | ML-17, ML-08 | 8 | yes |
| ML-21 | [Decision Stump with Gini Impurity](topics/machine-learning/decision-stump-gini/problem.md) | advanced | ML-06 | 8 | yes |
| ML-22 | [Decision Trees and Random Forests](topics/machine-learning/sklearn-trees-forests/problem.md) | advanced | ML-21, ML-19 | 6 |  |
| ML-23 | [Gradient Boosting](topics/machine-learning/sklearn-gradient-boosting/problem.md) | advanced | ML-22 | 6 |  |
| ML-24 | [Thresholds, ROC and Precision–Recall Curves](topics/machine-learning/sklearn-roc-pr/problem.md) | advanced | ML-23, ML-06 | 6 |  |
| ML-25 | [k-Means and Silhouette Scores](topics/machine-learning/sklearn-kmeans/problem.md) | advanced | ML-24 | 6 |  |
| ML-26 | [k-Means Clustering by Hand](topics/machine-learning/kmeans/problem.md) | advanced | ML-13 | 8 | yes |
| ML-27 | [Capstone: an End-to-End Tabular Model](topics/machine-learning/ml-capstone/problem.md) | advanced | ML-25, ML-18 | 6 |  |

### DL · Deep Learning

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| DL-01 | [Activation Functions](topics/deep-learning/activations/problem.md) | beginner | ML-11 | 7 |  |
| DL-02 | [Numerically Stable Softmax](topics/deep-learning/stable-softmax/problem.md) | beginner | DL-01, MA-02 | 8 | yes |
| DL-03 | [Cross-Entropy Loss](topics/deep-learning/cross-entropy/problem.md) | beginner | DL-02 | 8 | yes |
| DL-04 | [Dense Layer Forward Pass](topics/deep-learning/dense-forward/problem.md) | beginner | DL-01, NP-06 | 7 |  |
| DL-05 | [PyTorch Tensors](topics/deep-learning/torch-tensors/problem.md) | beginner | DL-04 | 6 |  |
| DL-06 | [Models with nn.Module](topics/deep-learning/torch-mlp-module/problem.md) | beginner | DL-05 | 6 |  |
| DL-07 | [MLP Forward Pass](topics/deep-learning/mlp-forward/problem.md) | beginner | DL-04 | 6 |  |
| DL-08 | [A Tiny Autograd Engine](topics/deep-learning/scalar-autograd/problem.md) | intermediate | DL-06, MA-11 | 8 | yes |
| DL-09 | [Autograd in PyTorch](topics/deep-learning/torch-autograd/problem.md) | intermediate | DL-08, DL-06 | 6 |  |
| DL-10 | [Backprop Through One Neuron](topics/deep-learning/neuron-backprop/problem.md) | intermediate | DL-08 | 6 |  |
| DL-11 | [Backpropagation Through a Dense Layer](topics/deep-learning/dense-backward/problem.md) | intermediate | DL-10 | 7 | yes |
| DL-12 | [Custom Gradients and gradcheck](topics/deep-learning/torch-gradcheck/problem.md) | intermediate | DL-11, DL-09 | 6 |  |
| DL-13 | [Gradient Checking by Hand](topics/deep-learning/gradient-check/problem.md) | intermediate | DL-11, MA-14 | 7 |  |
| DL-14 | [SGD with Momentum](topics/deep-learning/sgd-momentum/problem.md) | intermediate | DL-11, MA-13 | 6 |  |
| DL-15 | [Optimisers in torch.optim](topics/deep-learning/torch-optimizers/problem.md) | advanced | DL-14, DL-12 | 6 |  |
| DL-16 | [The Adam Optimiser](topics/deep-learning/adam-optimizer/problem.md) | advanced | DL-14 | 7 | yes |
| DL-17 | [Datasets and DataLoader](topics/deep-learning/torch-datasets/problem.md) | advanced | DL-15 | 6 |  |
| DL-18 | [A Full Training Loop](topics/deep-learning/torch-training-loop/problem.md) | advanced | DL-17 | 6 |  |
| DL-19 | [Train an MLP on XOR](topics/deep-learning/train-xor-mlp/problem.md) | advanced | DL-11, DL-14 | 7 |  |
| DL-20 | [Dropout with train() and eval()](topics/deep-learning/torch-dropout/problem.md) | advanced | DL-18 | 6 |  |
| DL-21 | [Inverted Dropout](topics/deep-learning/inverted-dropout/problem.md) | advanced | DL-19, NP-10 | 7 |  |
| DL-22 | [Batch Normalisation with nn.BatchNorm1d](topics/deep-learning/torch-batchnorm/problem.md) | advanced | DL-20 | 6 |  |
| DL-23 | [Batch Normalization by Hand (train/eval)](topics/deep-learning/batchnorm-forward/problem.md) | advanced | DL-21 | 8 | yes |
| DL-24 | [1-D Convolution with nn.Conv1d](topics/deep-learning/torch-conv1d/problem.md) | advanced | DL-22, NP-14 | 6 |  |
| DL-25 | [1D Convolution by Hand (valid, stride)](topics/deep-learning/conv1d/problem.md) | advanced | DL-04, NP-14 | 8 | yes |
| DL-26 | [Saving, Loading and Reproducibility](topics/deep-learning/torch-save-load/problem.md) | advanced | DL-24 | 6 |  |
| DL-27 | [Debugging Training](topics/deep-learning/torch-debugging/problem.md) | advanced | DL-26 | 6 |  |

### CV · Computer Vision

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| CV-01 | [Images as Arrays](topics/computer-vision/image-arrays/problem.md) | beginner | DL-24 | 8 | yes |
| CV-02 | [RGB to Grayscale](topics/computer-vision/rgb-to-gray/problem.md) | beginner | CV-01 | 6 |  |
| CV-03 | [OpenCV Basics: BGR, dtypes and Indexing](topics/computer-vision/cv-opencv-basics/problem.md) | beginner | CV-02 | 6 |  |
| CV-04 | [Flips, Rotations and Affine Warps](topics/computer-vision/cv-geometric-transforms/problem.md) | beginner | CV-03 | 6 |  |
| CV-05 | [Flip and Rotate](topics/computer-vision/flip-rotate/problem.md) | beginner | CV-01 | 6 |  |
| CV-06 | [Thresholding and Otsu's Method](topics/computer-vision/cv-threshold-otsu/problem.md) | beginner | CV-04 | 6 |  |
| CV-07 | [Binary Thresholding](topics/computer-vision/threshold-binary/problem.md) | beginner | CV-02 | 7 |  |
| CV-08 | [Histograms and Equalisation](topics/computer-vision/cv-histograms/problem.md) | beginner | CV-06 | 6 |  |
| CV-09 | [Intensity Histogram](topics/computer-vision/intensity-histogram/problem.md) | beginner | CV-02, ST-04 | 7 |  |
| CV-10 | [2D Filtering (Blur)](topics/computer-vision/conv2d-filter/problem.md) | intermediate | CV-02, DL-24 | 8 | yes |
| CV-11 | [Edges with Sobel and Canny](topics/computer-vision/cv-sobel-canny/problem.md) | intermediate | CV-10, CV-08 | 6 |  |
| CV-12 | [Sobel Edge Magnitude](topics/computer-vision/sobel-edges/problem.md) | intermediate | CV-10 | 8 | yes |
| CV-13 | [Pooling with nn.MaxPool2d and nn.AvgPool2d](topics/computer-vision/cv-pooling-torch/problem.md) | intermediate | CV-11, DL-24 | 6 |  |
| CV-14 | [2D Max Pooling](topics/computer-vision/max-pool-2d/problem.md) | intermediate | CV-10 | 7 | yes |
| CV-15 | [A Convolution Layer with Channels](topics/computer-vision/conv2d-layer/problem.md) | intermediate | CV-13, CV-10 | 8 | yes |
| CV-16 | [Image Quality: MSE and PSNR](topics/computer-vision/cv-psnr/problem.md) | intermediate | CV-15, CV-13 | 6 |  |
| CV-17 | [MSE and PSNR by Hand](topics/computer-vision/psnr/problem.md) | intermediate | CV-01, ML-02 | 7 |  |
| CV-18 | [Resizing with cv2.resize](topics/computer-vision/cv-resize/problem.md) | advanced | CV-16 | 6 |  |
| CV-19 | [Bilinear Resize](topics/computer-vision/bilinear-resize/problem.md) | advanced | CV-05, NP-09 | 8 |  |
| CV-20 | [Contours and Bounding Boxes](topics/computer-vision/cv-contours/problem.md) | advanced | CV-18 | 6 |  |
| CV-21 | [A Small CNN in PyTorch](topics/computer-vision/cv-small-cnn/problem.md) | advanced | CV-20, DL-18 | 6 |  |
| CV-22 | [Data Augmentation](topics/computer-vision/cv-augmentation/problem.md) | advanced | CV-21 | 6 |  |
| CV-23 | [Intersection over Union](topics/computer-vision/iou/problem.md) | advanced | CV-01, NP-07 | 6 |  |
| CV-24 | [Non-Maximum Suppression](topics/computer-vision/non-max-suppression/problem.md) | advanced | CV-23 | 8 |  |
| CV-25 | [Connected Components with OpenCV](topics/computer-vision/cv-connected-components/problem.md) | advanced | CV-24 | 6 |  |
| CV-26 | [Connected Components Labeling by Hand](topics/computer-vision/connected-components/problem.md) | advanced | CV-07 | 9 | yes |

### NL · Natural Language Processing

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| NL-01 | [Regular Expressions for Text](topics/nlp/regex-text/problem.md) | beginner | PY-16 | 7 |  |
| NL-02 | [Tokenize and Normalize](topics/nlp/tokenize-normalize/problem.md) | beginner | NL-01 | 7 |  |
| NL-03 | [Counting Words with Counter and CountVectorizer](topics/nlp/nlp-countvectorizer/problem.md) | beginner | NL-02, ML-02 | 6 |  |
| NL-04 | [Stopwords and Word Counts](topics/nlp/stopword-counts/problem.md) | beginner | NL-02 | 8 | yes |
| NL-05 | [Character n-grams with CountVectorizer](topics/nlp/nlp-char-ngrams-sklearn/problem.md) | beginner | NL-03 | 6 |  |
| NL-06 | [Character n-grams by Hand](topics/nlp/char-ngrams/problem.md) | beginner | NL-02 | 7 |  |
| NL-07 | [Bag-of-Words Vectors](topics/nlp/bag-of-words/problem.md) | intermediate | NL-03 | 8 | yes |
| NL-08 | [Bigram Counts with Sentence Markers](topics/nlp/bigram-counts/problem.md) | intermediate | NL-04 | 7 |  |
| NL-09 | [TF-IDF](topics/nlp/tf-idf/problem.md) | intermediate | NL-07 | 7 | yes |
| NL-10 | [Search with TfidfVectorizer and Cosine Similarity](topics/nlp/nlp-tfidf-retrieval/problem.md) | intermediate | NL-09 | 6 |  |
| NL-11 | [Cosine Similarity Retrieval](topics/nlp/cosine-retrieval/problem.md) | intermediate | NL-09 | 7 | yes |
| NL-12 | [Levenshtein Edit Distance](topics/nlp/levenshtein/problem.md) | intermediate | NL-05 | 7 |  |
| NL-13 | [Rule-Based Suffix Stemmer](topics/nlp/suffix-stemmer/problem.md) | advanced | NL-02 | 7 |  |
| NL-14 | [Multinomial Naive Bayes Text Classifier](topics/nlp/naive-bayes-text/problem.md) | advanced | NL-07, ST-07 | 8 | yes |
| NL-15 | [A Text Classification Pipeline](topics/nlp/nlp-text-classifier/problem.md) | advanced | NL-14, NL-10 | 6 |  |
| NL-16 | [Evaluating Text Classifiers](topics/nlp/nlp-error-analysis/problem.md) | advanced | NL-15 | 6 |  |
| NL-17 | [PPMI Co-occurrence Matrix](topics/nlp/ppmi-matrix/problem.md) | advanced | NL-07, NL-09 | 7 |  |
| NL-18 | [Word Embedding Analogies](topics/nlp/embedding-analogy/problem.md) | advanced | NL-10, NL-17 | 7 |  |
| NL-19 | [Word Embeddings in PyTorch](topics/nlp/nlp-embedding-bag/problem.md) | advanced | NL-18, DL-18 | 6 |  |

### LM · Large Language Models

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| LM-01 | [Vocabularies and Token IDs](topics/llms/token-ids/problem.md) | beginner | NL-07 | 6 | yes |
| LM-02 | [Next-Token Probabilities (Add-k)](topics/llms/bigram-next-token/problem.md) | beginner | LM-01, NL-02 | 7 |  |
| LM-03 | [Logits, Temperature and Softmax](topics/llms/temperature-softmax/problem.md) | beginner | LM-02, DL-02 | 8 |  |
| LM-04 | [Greedy Decoding](topics/llms/greedy-decoding/problem.md) | beginner | LM-03 | 8 |  |
| LM-05 | [Perplexity](topics/llms/perplexity/problem.md) | beginner | LM-02, DL-03 | 7 |  |
| LM-06 | [Byte-Pair Encoding Merges](topics/llms/bpe-merges/problem.md) | intermediate | LM-01 | 8 |  |
| LM-07 | [Scaled Dot-Product Attention](topics/llms/scaled-dot-attention/problem.md) | intermediate | LM-03, NP-06 | 7 |  |
| LM-08 | [Causal Masking](topics/llms/causal-mask/problem.md) | intermediate | LM-07 | 7 |  |
| LM-09 | [Sinusoidal Positional Encoding](topics/llms/positional-encoding/problem.md) | intermediate | LM-07 | 7 |  |
| LM-10 | [Multi-Head Attention](topics/llms/multi-head-attention/problem.md) | intermediate | LM-07, LM-08 | 7 |  |
| LM-11 | [A Transformer Block as nn.Module](topics/llms/lm-transformer-module/problem.md) | intermediate | LM-10, DL-06 | 6 |  |
| LM-12 | [A Pre-Norm Transformer Block by Hand](topics/llms/transformer-block/problem.md) | intermediate | LM-10, LM-09 | 7 | yes |
| LM-13 | [Top-k and Top-p Filtering](topics/llms/top-k-top-p/problem.md) | advanced | LM-03 | 10 |  |
| LM-14 | [Beam Search](topics/llms/beam-search/problem.md) | advanced | LM-04 | 7 |  |
| LM-15 | [Incremental Decoding with a KV Cache](topics/llms/kv-cache/problem.md) | advanced | LM-08, LM-10 | 6 |  |
| LM-16 | [A Tiny GPT in PyTorch](topics/llms/lm-tiny-gpt/problem.md) | advanced | LM-15, LM-11 | 6 |  |
| LM-17 | [Chat Prompts and Messages with LangChain](topics/llms/lm-chat-prompt-langchain/problem.md) | advanced | LM-16 | 6 |  |
| LM-18 | [Chat Prompt Templates](topics/llms/chat-prompt/problem.md) | advanced | LM-01 | 6 | yes |
| LM-19 | [Structured Output with Pydantic and Retries](topics/llms/lm-structured-output/problem.md) | advanced | LM-17 | 6 |  |
| LM-20 | [Retrieval-Augmented Generation with LangChain](topics/llms/lm-langchain-rag/problem.md) | advanced | LM-19, NL-10 | 6 |  |
| LM-21 | [Retrieval-Augmented Generation by Hand](topics/llms/rag-pipeline/problem.md) | advanced | LM-18, NL-11 | 7 | yes |

### XA · Explainable AI

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| XA-01 | [Linear Model Contributions](topics/explainable-ai/linear-contributions/problem.md) | beginner | ML-09 | 6 |  |
| XA-02 | [Ranking Attributions](topics/explainable-ai/top-k-attributions/problem.md) | beginner | XA-01 | 6 |  |
| XA-03 | [Tracing a Decision Path](topics/explainable-ai/decision-path/problem.md) | beginner | ML-21 | 7 |  |
| XA-04 | [Individual Conditional Expectation](topics/explainable-ai/ice-curve/problem.md) | beginner | XA-01 | 6 |  |
| XA-05 | [Partial Dependence with sklearn.inspection](topics/explainable-ai/xai-partial-dependence/problem.md) | intermediate | XA-04, ML-22 | 6 |  |
| XA-06 | [Partial Dependence by Hand](topics/explainable-ai/partial-dependence/problem.md) | intermediate | XA-04 | 7 |  |
| XA-07 | [Permutation Importance with sklearn.inspection](topics/explainable-ai/xai-permutation-importance/problem.md) | intermediate | XA-05 | 6 |  |
| XA-08 | [Permutation Feature Importance by Hand](topics/explainable-ai/permutation-importance/problem.md) | intermediate | XA-06, ML-02 | 7 | yes |
| XA-09 | [Occlusion Saliency Map](topics/explainable-ai/occlusion-saliency/problem.md) | intermediate | CV-13, XA-04 | 7 |  |
| XA-10 | [Global Surrogate and Fidelity](topics/explainable-ai/surrogate-fidelity/problem.md) | intermediate | XA-07, ML-09 | 6 |  |
| XA-11 | [Exact Shapley Values](topics/explainable-ai/exact-shapley/problem.md) | advanced | MA-07, XA-01 | 7 |  |
| XA-12 | [LIME-style Local Linear Explanation](topics/explainable-ai/lime-local/problem.md) | advanced | XA-10, ML-19 | 7 |  |
| XA-13 | [Minimal Counterfactual Search](topics/explainable-ai/counterfactual-search/problem.md) | advanced | XA-03 | 7 |  |
| XA-14 | [Integrated Gradients](topics/explainable-ai/integrated-gradients/problem.md) | advanced | XA-11, DL-10 | 7 |  |

### FL · Federated Learning

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| FL-01 | [IID Client Partitioning](topics/federated-learning/iid-partition/problem.md) | beginner | ML-16 | 6 |  |
| FL-02 | [Weighted Federated Averaging](topics/federated-learning/weighted-fedavg/problem.md) | beginner | FL-01 | 6 |  |
| FL-03 | [Client Updates as Deltas](topics/federated-learning/client-delta/problem.md) | beginner | FL-02 | 6 |  |
| FL-04 | [Label-Skewed (non-IID) Partition](topics/federated-learning/label-skew-partition/problem.md) | beginner | FL-01 | 6 |  |
| FL-05 | [Client Training with a PyTorch Model](topics/federated-learning/fl-torch-local-training/problem.md) | intermediate | FL-04, DL-18 | 6 |  |
| FL-06 | [Local SGD on a Client](topics/federated-learning/local-sgd/problem.md) | intermediate | ML-10, FL-03 | 6 |  |
| FL-07 | [One FedAvg Round](topics/federated-learning/fedavg-round/problem.md) | intermediate | FL-02, FL-05 | 7 |  |
| FL-08 | [Seeded Client Sampling](topics/federated-learning/client-sampling/problem.md) | intermediate | FL-07 | 7 |  |
| FL-09 | [Clipping Client Updates](topics/federated-learning/update-clipping/problem.md) | intermediate | FL-03 | 7 |  |
| FL-10 | [Full FedAvg Training Loop](topics/federated-learning/fedavg-training/problem.md) | advanced | FL-07, FL-08 | 6 |  |
| FL-11 | [FedAvg with PyTorch state_dicts](topics/federated-learning/fl-torch-fedavg/problem.md) | advanced | FL-10, FL-05 | 6 |  |
| FL-12 | [Secure Aggregation with Pairwise Masks](topics/federated-learning/secure-aggregation/problem.md) | advanced | FL-02 | 7 |  |
| FL-13 | [Differentially Private Aggregation](topics/federated-learning/dp-aggregation/problem.md) | advanced | FL-09, FL-02 | 7 |  |
| FL-14 | [FedProx Local Objective](topics/federated-learning/fedprox/problem.md) | advanced | FL-05, FL-10 | 7 |  |

### RL · Reinforcement Learning

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| RL-01 | [Discounted Return](topics/reinforcement-learning/discounted-return/problem.md) | beginner | PY-14 | 7 |  |
| RL-02 | [Gridworld Transition Function](topics/reinforcement-learning/gridworld-step/problem.md) | beginner | RL-01 | 6 |  |
| RL-03 | [The Environment Interface: reset and step](topics/reinforcement-learning/env-interface/problem.md) | beginner | RL-02 | 7 | yes |
| RL-04 | [Gymnasium Environments](topics/reinforcement-learning/rl-gymnasium-env/problem.md) | beginner | RL-03 | 6 |  |
| RL-05 | [Epsilon-Greedy Action Selection](topics/reinforcement-learning/epsilon-greedy/problem.md) | beginner | RL-03, NP-10 | 7 |  |
| RL-06 | [Incremental Value Estimates](topics/reinforcement-learning/bandit-incremental/problem.md) | intermediate | RL-05 | 6 |  |
| RL-07 | [UCB1 Bandit](topics/reinforcement-learning/ucb-bandit/problem.md) | intermediate | RL-06 | 7 |  |
| RL-08 | [Iterative Policy Evaluation](topics/reinforcement-learning/policy-evaluation/problem.md) | intermediate | RL-02, RL-01 | 6 |  |
| RL-09 | [Value Iteration](topics/reinforcement-learning/value-iteration/problem.md) | intermediate | RL-08 | 6 |  |
| RL-10 | [Policy Iteration](topics/reinforcement-learning/policy-iteration/problem.md) | intermediate | RL-08, RL-09 | 6 |  |
| RL-11 | [First-Visit Monte Carlo Prediction](topics/reinforcement-learning/mc-first-visit/problem.md) | advanced | RL-03, RL-08 | 6 |  |
| RL-12 | [TD(0) Prediction](topics/reinforcement-learning/td0-prediction/problem.md) | advanced | RL-08, RL-11 | 6 |  |
| RL-13 | [Tabular Q-Learning](topics/reinforcement-learning/q-learning/problem.md) | advanced | RL-05, RL-02, RL-12 | 7 |  |
| RL-14 | [Q-Learning on FrozenLake](topics/reinforcement-learning/rl-frozenlake-q/problem.md) | advanced | RL-13, RL-04 | 6 |  |
| RL-15 | [SARSA](topics/reinforcement-learning/sarsa/problem.md) | advanced | RL-13 | 6 |  |

### AG · Agentic AI

| ID | Step | Difficulty | Builds on | Tests | Library comparison |
|---|---|---|---|---|---|
| AG-01 | [Tool Registry and Dispatch](topics/agentic-ai/tool-registry/problem.md) | beginner | PY-17 | 7 |  |
| AG-02 | [Parsing Model Tool Calls](topics/agentic-ai/parse-tool-call/problem.md) | beginner | AG-01, NL-01 | 9 |  |
| AG-03 | [Tools and Tool Calling with LangChain](topics/agentic-ai/ag-langchain-tools/problem.md) | beginner | AG-02, LM-17 | 6 |  |
| AG-04 | [Perceive-Act Loop](topics/agentic-ai/reflex-agent-loop/problem.md) | beginner | AG-01 | 7 |  |
| AG-05 | [Goal Tests and Step Budgets](topics/agentic-ai/goal-and-budget/problem.md) | beginner | AG-04 | 7 |  |
| AG-06 | [ReAct Loop with a Scripted Model](topics/agentic-ai/react-loop/problem.md) | intermediate | AG-02, AG-05 | 7 |  |
| AG-07 | [LangGraph Basics: State, Nodes and Edges](topics/agentic-ai/ag-langgraph-basics/problem.md) | intermediate | AG-06, AG-03 | 6 |  |
| AG-08 | [A ReAct Agent in LangGraph](topics/agentic-ai/ag-langgraph-react/problem.md) | intermediate | AG-07 | 6 |  |
| AG-09 | [Conversation Memory with trim_messages](topics/agentic-ai/ag-message-memory/problem.md) | intermediate | AG-08 | 6 |  |
| AG-10 | [Conversation Memory Window by Hand](topics/agentic-ai/memory-window/problem.md) | intermediate | AG-06 | 8 |  |
| AG-11 | [BFS Planner](topics/agentic-ai/bfs-planner/problem.md) | intermediate | AG-05 | 6 |  |
| AG-12 | [A* Planner](topics/agentic-ai/a-star-planner/problem.md) | intermediate | AG-11 | 7 |  |
| AG-13 | [Dependency-Ordered Plans](topics/agentic-ai/task-dag-plan/problem.md) | advanced | AG-11 | 7 |  |
| AG-14 | [Validating Tool Arguments and Retrying](topics/agentic-ai/ag-validate-retry/problem.md) | advanced | AG-13, AG-09, LM-19 | 6 |  |
| AG-15 | [Validate-and-Retry Tool Calls](topics/agentic-ai/validate-and-retry/problem.md) | advanced | AG-02, AG-06 | 6 |  |
| AG-16 | [Orchestrator and Workers in LangGraph](topics/agentic-ai/ag-orchestrator-graph/problem.md) | advanced | AG-14 | 6 |  |
| AG-17 | [Orchestrator-Workers Pipeline by Hand](topics/agentic-ai/orchestrator-workers/problem.md) | advanced | AG-13, AG-15 | 7 |  |
| AG-18 | [Guardrails with Human Approval](topics/agentic-ai/ag-approval-guardrails/problem.md) | advanced | AG-16 | 6 |  |
| AG-19 | [Permission Guardrails](topics/agentic-ai/permission-guardrails/problem.md) | advanced | AG-01, AG-06 | 7 |  |
| AG-20 | [Evaluating Agents](topics/agentic-ai/agent-evaluation/problem.md) | advanced | AG-06, AG-18 | 6 |  |

## What changed in this revision

* 123 new steps and 168 retained packs, reordered into one path; IDs are reassigned from the path (`build/legacy_ids.json` keeps the old ones).
* New FastAPI topic (15 steps): HTTP messages, status codes, URLs, JSON bodies, a hand-made router, asyncio and ASGI with the standard library, then FastAPI routes, parameters, Pydantic bodies, errors, response models, dependencies, async endpoints and API testing.
* Library comparisons: lessons show the manual and the idiomatic library implementation (standard library, NumPy, pandas, scikit-learn, SciPy, PyTorch) and tests compare them where the comparison is meaningful.
* Retained packs were adjusted where they used untaught concepts (e.g. Fibonacci no longer raises before exceptions are taught) and their prerequisites and difficulty labels follow the path.
* New: a static audit that every construct is taught before use, and a coverage map (coverage-map.md).

New steps: PY-01 Hello, print(), PY-02 Variables and f-strings, PY-03 Types and Conversion, PY-04 Reading Input, PY-05 Arithmetic Operators, PY-06 Strings: Indexing, Slicing and Methods, PY-07 Conditionals: Letter Grades, PY-08 While Loops: Read Until Done, PY-09 For Loops and range: FizzBuzz, PY-15 Importing the Standard Library, PY-17 Functions as Values, PY-23 Files, CSV and JSON, PY-25 Classes: A Bank Account, PY-26 Inheritance, Special Methods and Dataclasses, PY-27 Writing Unit Tests, MA-01 Summation and Product Notation, MA-02 Exponentials and Logarithms, MA-03 The Sigmoid Function, MA-11 Derivative Rules and the Chain Rule, ST-06 Probability by Counting Outcomes, ST-07 Conditional Probability and Bayes' Rule, ST-09 The Normal Distribution, ST-12 Sampling Distributions and Standard Error, ST-14 Introducing scipy.stats, ST-15 Chi-Square Test with SciPy, ST-17 Welch's t-test with SciPy, ST-19 Permutation Test with SciPy, NP-02 Vectorised Arithmetic and ufuncs, NP-06 Matrix Products with @, PD-01 Series: Labelled Columns, PD-03 Reading and Writing CSV, PD-06 Finding and Handling Missing Values, PD-12 Working with Dates, FA-01 Anatomy of an HTTP Request, FA-02 HTTP Responses and Status Codes, FA-03 URLs, Paths and Query Strings, FA-04 JSON Request Bodies and Validation, FA-05 A Router by Hand, FA-06 async and await with asyncio, FA-07 A Minimal ASGI Application, FA-08 First FastAPI Routes, FA-09 Query and Path Parameters with Validation, FA-10 Request Bodies with Pydantic, FA-11 Handling Errors in FastAPI, FA-12 Response Models and Status Codes, FA-13 Dependencies and Dependency Overrides, FA-14 Async Endpoints and External Services, FA-15 Testing an API, ML-01 Features, Labels and Baseline Models, ML-02 The scikit-learn Estimator API, ML-04 Splitting Data with scikit-learn, ML-07 Scaling inside a Pipeline, ML-12 k-Nearest Neighbours with scikit-learn, ML-14 Polynomial Features and Validation Curves, ML-15 Polynomial Features and Overfitting by Hand, ML-16 Cross-Validation with scikit-learn, ML-18 Pipelines and ColumnTransformer, ML-19 Regularisation and Hyperparameter Search, ML-22 Decision Trees and Random Forests, ML-23 Gradient Boosting, ML-24 Thresholds, ROC and Precision–Recall Curves, ML-25 k-Means and Silhouette Scores, ML-27 Capstone: an End-to-End Tabular Model, DL-05 PyTorch Tensors, DL-06 Models with nn.Module, DL-08 A Tiny Autograd Engine, DL-09 Autograd in PyTorch, DL-11 Backpropagation Through a Dense Layer, DL-12 Custom Gradients and gradcheck, DL-15 Optimisers in torch.optim, DL-16 The Adam Optimiser, DL-17 Datasets and DataLoader, DL-18 A Full Training Loop, DL-20 Dropout with train() and eval(), DL-22 Batch Normalisation with nn.BatchNorm1d, DL-24 1-D Convolution with nn.Conv1d, DL-26 Saving, Loading and Reproducibility, DL-27 Debugging Training, CV-01 Images as Arrays, CV-03 OpenCV Basics: BGR, dtypes and Indexing, CV-04 Flips, Rotations and Affine Warps, CV-06 Thresholding and Otsu's Method, CV-08 Histograms and Equalisation, CV-11 Edges with Sobel and Canny, CV-13 Pooling with nn.MaxPool2d and nn.AvgPool2d, CV-15 A Convolution Layer with Channels, CV-16 Image Quality: MSE and PSNR, CV-18 Resizing with cv2.resize, CV-20 Contours and Bounding Boxes, CV-21 A Small CNN in PyTorch, CV-22 Data Augmentation, CV-25 Connected Components with OpenCV, NL-01 Regular Expressions for Text, NL-03 Counting Words with Counter and CountVectorizer, NL-05 Character n-grams with CountVectorizer, NL-10 Search with TfidfVectorizer and Cosine Similarity, NL-15 A Text Classification Pipeline, NL-16 Evaluating Text Classifiers, NL-19 Word Embeddings in PyTorch, LM-01 Vocabularies and Token IDs, LM-11 A Transformer Block as nn.Module, LM-12 A Pre-Norm Transformer Block by Hand, LM-16 A Tiny GPT in PyTorch, LM-17 Chat Prompts and Messages with LangChain, LM-18 Chat Prompt Templates, LM-19 Structured Output with Pydantic and Retries, LM-20 Retrieval-Augmented Generation with LangChain, LM-21 Retrieval-Augmented Generation by Hand, XA-05 Partial Dependence with sklearn.inspection, XA-07 Permutation Importance with sklearn.inspection, FL-05 Client Training with a PyTorch Model, FL-11 FedAvg with PyTorch state_dicts, RL-03 The Environment Interface: reset and step, RL-04 Gymnasium Environments, RL-14 Q-Learning on FrozenLake, AG-03 Tools and Tool Calling with LangChain, AG-07 LangGraph Basics: State, Nodes and Edges, AG-08 A ReAct Agent in LangGraph, AG-09 Conversation Memory with trim_messages, AG-14 Validating Tool Arguments and Retrying, AG-16 Orchestrator and Workers in LangGraph, AG-18 Guardrails with Human Approval, AG-20 Evaluating Agents.

## Confirmed facts and design choices

**Confirmed by running code:** all reference solutions pass and all starters fail at least one test in each recorded environment (coverage.md §3); the audit in coverage.md §4 reports no violations; worked-example numbers in new lessons were checked by the tests that reproduce them.

**Design choices:** the topic order and step order; difficulty labels; simplified protocols for teaching (the chat template, the `<tool_call>` format, whole-word tokens, toy MDPs, synthetic data); scripted models in place of real LLMs; privacy steps teach mechanics without formal guarantees; test tolerances chosen from observed numerical behaviour.

## Remaining gaps

* Optional GPU explorations (Colab/Kaggle notebooks) were dropped from this revision at the maintainer's request; no exploration links are published.
* Not covered as graded steps: SVD/PCA, Poisson p-values, SVMs, recurrent networks, CNN training on real images, fine-tuning or downloading pretrained models (Hugging Face), SHAP, policy-gradient and deep RL methods, SQL databases and OAuth2/JWT authentication in FastAPI, and deployment. Several of these appear in the ungraded project ideas.
* LLM and agent steps use scripted fake chat models (LangChain's FakeListChatModel and GenericFakeChatModel) and keyword or toy embeddings; no real model is downloaded or called in graded work.
* Difficulty labels are design choices, not measured learner outcomes.
* Licences for many references are recorded as 'not confirmed' (see sources.csv).
* Packs that need PyTorch, FastAPI, LangChain, LangGraph or Gymnasium, and the asyncio ASGI step, always use the executor for Run; Pyodide does not provide those libraries or a nested event loop. The other 251 packs run their visible tests in the browser.
* Starlette 1.9 prints a deprecation warning recommending `httpx2` for `TestClient`; tests pass with `httpx` 0.28.1, and `httpx2` was not evaluated.

## Next.js and executor integration

1. Done (library revision Phase 0): one executor image with every pack library (`executor/requirements.txt`, mirrored by `build/requirements-executor.txt`), two preloaded single-use containers, two job slots and a queue of 30 (Submit first), 1 GB/1 CPU/30 s per job with a 10 s CPU budget charged after imports. All 226 packs were graded through it (solution passes Run and Submit, starter fails Submit; 678 jobs, 73 per minute, slowest test run 0.7 s, peak runner memory 489 MB, measured on an Apple-silicon Mac; see `executor/measurements.json`). Pyodide now starts when a problem page opens and stays alive across Runs; SciPy, scikit-learn and OpenCV are allowed locally. The builder, generator and app support `optional` deep dives and ungraded `project` ideas.
2. Done: `scripts/generate-learn-demo.py` reads topic order, step order and outcomes from `aimlgym/build/path.py` (15 topics including FastAPI) and publishes `kind`, `optionalPackages` and a `localPrelude` (the test-module helpers the visible cases call).
3. Done: `public/learn/pyodide-worker.mjs` runs whole-program (`kind: script`) steps with a replaced stdin and executes the helper prelude, so 209 of 226 packs are eligible for in-browser Run (82 of 168 before). The harness was exercised with CPython 3.9 and 3.13 for every eligible pack (solution passes all visible cases, starter fails at least one); it was not run inside Pyodide in a browser.
4. Done: `executor/Dockerfile` adds `fastapi==0.162.0` and `httpx==0.28.1`. `executor/runner.py` graded every pack in run and submit mode with the executor-pinned packages (slowest submit about 0.6 s of CPU against the 6 s limit). The image was rebuilt locally and every pack was graded through `executor/service.py`'s hardened container (no network, read-only, 768 MB, 64 PIDs): all reference solutions pass in run and submit mode and every starter fails.
5. Done: Learn copy computes topic and problem counts; FastAPI is in the Foundations filter; `AGENTS.md`, `README.md`, `dev.md` and `executor/README.md` describe the new workflow; Learn and executor tests read test counts from the generated data.
6. To deploy: rebuild the runner image on the VPS, copy the regenerated `executor/tests.generated.json`, restart the service, and release the matching `lib/learn/*.generated.json` fixtures together.
7. Done (library revision Phases 1–6): library steps for SciPy, scikit-learn, PyTorch, OpenCV, LangChain, LangGraph and Gymnasium; the from-scratch steps they replace stay on the path as optional deep dives; 31 ungraded project ideas. See `library-revision-plan.md`. All 291 packs were graded through the executor on 2026-10-25 (solution passes Run and Submit, starter fails; 873 jobs at 79 per minute; slowest test run 1.0 s of CPU, peak runner memory 511 MB, on an Apple-silicon Mac; `executor/measurements.json`). The runner now counts tests blocked by a failing setUpClass as failed instead of rejecting the result.
8. Problem IDs changed. Slugs of retained packs are unchanged, so slug-keyed progress keeps working; `aimlgym/build/legacy_ids.json` maps each retained slug to its old ID for any ID-keyed data.
