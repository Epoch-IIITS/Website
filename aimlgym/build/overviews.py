"""Topic introductions rendered at the top of topics/<topic>/overview.md."""

OVERVIEWS = {
"python": r'''
This topic assumes no programming experience. It climbs in three stages:

1. **Programs (steps 1–9).** `print`, variables, types, `input`, operators, strings, `if`,
   `while` and `for`. You write whole programs; the tests run them with sample input and compare
   what they print.
2. **Functions and collections (steps 10–18).** `def`, lists, comprehensions, dictionaries,
   tuples, the standard library, sets, functions as values and grouping records. From here
   on, tests call your functions and check their return values.
3. **Robust programs (steps 19–27).** Raising exceptions, validating nested lists, handling
   exceptions, a stateful game loop,
   files and JSON, scripts that read standard input, classes, inheritance and writing your own
   unit tests.

**Packages:** standard library only. Where Python has a built-in shortcut (`sum`,
`collections.Counter`, `math.comb`), the lesson first shows the loop it replaces.

**Project ideas:** ungraded briefs between steps suggest things to build with what you have learned so far.
''',
"mathematics": r'''
The mathematics that later topics use, each idea implemented in plain Python before NumPy
appears. It starts with notation (Σ and Π), exponentials and logarithms, and the sigmoid — the
pieces needed for probabilities and logistic regression — then moves through vectors and
matrices, counting, small linear systems, numerical and analytic derivatives (including the
chain rule used by backpropagation), integration, gradient descent, series and eigenvectors.

**Packages:** standard library only. Each lesson compares the hand-written version with the
`math` module where one exists; [[vectorized-math]] and [[matmul-dot]] later redo these
operations in NumPy and check that the answers agree.

**Project ideas:** ungraded briefs between steps suggest things to build with what you have learned so far.
''',
"statistics": r'''
Describing data first (mean, variance, median, percentiles, histograms, z-scores), then
probability (sample spaces, conditional probability, Bayes' rule), two named distributions
(binomial and normal), simulation and the law of large numbers, correlation, sampling
distributions and standard errors, and bootstrap intervals. The topic ends with
`scipy.stats`: distribution objects, then the chi-square test, Welch's t-test and the
permutation test, each followed by an optional deep dive that computes the same test by hand.

**Packages:** standard library, then `scipy` for the last four required steps. Random
simulations use `random.Random(seed).random()`, whose sequence Python documents as reproducible.
**Project ideas:** an A/B test analyser and a dice-and-coin simulator.
''',
"numpy": r'''
NumPy replaces Python loops over numbers with operations on whole arrays. The topic starts by
creating and inspecting arrays and repeating the loops you wrote in Mathematics as vectorised
expressions, then covers slicing, masks, axis reductions, matrix products, broadcasting,
reshaping, gathers, seeded random generators, pairwise distances, linear solvers, one-hot
encoding and sliding windows.

**Packages:** `numpy` (validated on 2.2 and 2.5). Most tests check a NumPy implementation
against a plain-Python reference so you can see they compute the same thing.

**Project ideas:** ungraded briefs between steps suggest things to build with what you have learned so far.
''',
"pandas": r'''
pandas adds labelled rows and columns on top of NumPy. You start with a single labelled column
(`Series`), then build and read tables, select and derive columns, handle missing values, sort,
group, merge, clean text, work with dates, resample, pivot, bin and compute rolling features.
Group-by and merge lessons first solve the task with dictionaries so the library's behaviour is
not magic.

**Packages:** `pandas` and `numpy`. Packs are validated on pandas 2.2 (the executor image) and
pandas 3.x; code avoids chained assignment so it behaves the same under Copy-on-Write.

**Project ideas:** ungraded briefs between steps suggest things to build with what you have learned so far.
''',
"machine-learning": r'''
Machine learning from the ground up, then with scikit-learn. You start with features, labels and
baselines, then learn the estimator API (`fit`, `predict`, `score`, `clone`), splitting,
classification metrics and scaling inside a pipeline. Least squares, gradient-descent regression
and logistic regression are built by hand; k-NN, validation curves, cross-validation,
ColumnTransformer pipelines, regularisation with grid search, decision trees, random forests,
gradient boosting, ROC and precision–recall thresholds and k-means use scikit-learn. A capstone
combines everything in one leak-free workflow.

**Packages:** `numpy`, `pandas` and `scikit-learn`. Where a library step replaces an earlier
from-scratch step, that step follows it as an **optional deep dive** showing what the library does
inside. **Project ideas:** a house-price predictor, a spam or fraud classifier, and serving your
model with FastAPI.
''',
"deep-learning": r'''
Neural networks in two passes. In NumPy you write activations, softmax, cross-entropy, dense
layers, a tiny scalar autograd engine and backpropagation, and SGD with momentum. In PyTorch you
then use tensors, `nn.Module`, autograd, custom gradients with `gradcheck`, `torch.optim`,
`Dataset` and `DataLoader`, a full training loop, dropout, batch normalisation and `Conv1d`, and
finish with saving, loading, reproducibility and debugging training.

**Packages:** `numpy`, then `torch` (CPU). Everything trains in about a second. The NumPy versions
of the MLP, gradient check, Adam, XOR training, dropout, batch normalisation and convolution stay
as **optional deep dives** after their PyTorch steps. **Project ideas:** a handwritten digit
recogniser and a training-diagnostics notebook.
''',
"computer-vision": r'''
Images are arrays of numbers. After image dtypes and colour-to-grey conversion, OpenCV takes over:
BGR order and indexing, flips, rotations and affine warps, thresholding with Otsu's method,
histograms and equalisation, 2D filtering, Sobel and Canny edges, PSNR, resizing, contours and
bounding boxes. With PyTorch you use pooling layers and a convolution layer, train a small CNN and
add data augmentation; the topic ends with IoU, non-maximum suppression and connected components.

**Packages:** `numpy`, `opencv-python-headless` and `torch`. Images are small synthetic arrays
defined in the tests. The NumPy versions of the library steps follow them as **optional deep
dives**. **Project ideas:** a document scanner, a shape and colour sorter, and an object counter.
''',
"nlp": r'''
Working with text: regular expressions, tokenisation and normalisation, word and character n-gram
counts with `Counter` and `CountVectorizer`, bag-of-words vectors, TF-IDF and cosine-similarity
search with scikit-learn, edit distance, Naive Bayes, a TF-IDF + logistic-regression text
classifier with error analysis, PPMI word vectors and analogies, and learned embeddings with
PyTorch's `nn.EmbeddingBag`.

**Packages:** standard library, `numpy`, `scikit-learn` and `torch`. The hand-written stopword,
character n-gram and retrieval steps, bigram counts and the suffix stemmer are **optional deep
dives**. **Project ideas:** a review sentiment analyser and semantic search for the club blog.
''',
"llms": r'''
How a language model turns text into tokens and tokens into text: vocabularies and token IDs,
next-token probabilities, temperature, greedy decoding and perplexity, byte-pair encoding, then
the transformer — scaled dot-product attention, causal masks, positional encodings, multi-head
attention and a pre-norm block as a PyTorch `nn.Module` — then sampling (top-k/top-p), beam search,
KV caching and a tiny character-level GPT trained in PyTorch. The topic ends with LangChain: chat
prompts and messages, structured output with Pydantic and retries, and retrieval-augmented
generation with citation checks.

**Packages:** `numpy`, `torch` and `langchain-core`. No model weights are downloaded and no API is
called: LangChain steps use fake chat models, so tests are exact. The NumPy transformer block,
the hand-made chat template and RAG pipeline are **optional deep dives**. **Project ideas:** a poem
or name generator, a course FAQ chatbot and a prompt playground.
''',
"explainable-ai": r'''
Explaining predictions, from models that explain themselves (linear contributions, decision
paths) to model-agnostic methods — ICE curves, partial dependence and permutation importance with
`sklearn.inspection`, occlusion, global surrogates, exact Shapley values, LIME, counterfactuals —
and a gradient method for neural networks (integrated gradients). Every model being explained is
small and defined in the test, so each attribution can be checked.

**Packages:** `numpy`, `pandas` and `scikit-learn`. The NumPy partial dependence and permutation
importance are **optional deep dives**. **Project idea:** explain your house-price model.
''',
"federated-learning": r'''
Training a model across many clients without collecting their data. The topic simulates clients
in one process: IID and label-skewed partitions, weighted averaging, client updates as deltas,
client training of a PyTorch model copy, a FedAvg round and full training loop, FedAvg over
PyTorch `state_dict`s, client sampling, update clipping, secure aggregation with pairwise masks,
differentially private aggregation and FedProx.

**Packages:** `numpy` and `torch`. The privacy steps teach the mechanics (clipping, noise,
masking); they do not compute formal privacy guarantees. Local SGD in NumPy is an **optional deep
dive**. **Project idea:** federated training across departments, with a pointer to the Flower
framework.
''',
"reinforcement-learning": r'''
Learning from rewards. You first define returns, a gridworld transition function and the
reset/step environment interface — then the same environment as a real `gymnasium.Env` with
spaces and a time-limit wrapper. You explore with ε-greedy, incremental estimates and UCB bandits,
solve known MDPs with policy evaluation, value iteration and policy iteration, and learn from
experience with first-visit Monte Carlo, TD(0), Q-learning (also on Gymnasium's FrozenLake) and
SARSA.

**Packages:** `numpy` and `gymnasium`. **MDP format (design choice):** `P[s][a]` is a list of
`(probability, next_state, reward, done)` tuples; terminal transitions stop bootstrapping.
All environments are tiny and seeded, so every result is reproducible. **Project ideas:** a grid
game agent and a bandit-based recommender.
''',
"agentic-ai": r'''
Agents are programs that repeatedly decide on an action, act through tools and observe the
result. You first build each part with ordinary Python and a **scripted model** — tool registries,
parsing model output, perceive–act loops, goals and budgets, the ReAct loop, BFS and A* planners,
dependency-ordered plans and an evaluation harness. Then you use the libraries: LangChain tools and
tool calling, LangGraph state graphs, a ReAct agent with a tool node and checkpointed threads,
message trimming, validated tool arguments with retries, orchestrator–workers with `Send`, and
human approval with interrupts.

**Packages:** standard library, `langchain-core` and `langgraph`. Fake chat models keep every test
deterministic; no paid API or network is used. The hand-written memory window, validate-and-retry,
orchestrator and guardrail steps are **optional deep dives**. **Project ideas:** a study-planner
agent, a club event assistant and an agent evaluation suite.
''',
"fastapi": r'''
Web APIs from first principles. The first half uses only the standard library: the structure
of HTTP requests and responses, status codes, URLs and query strings, JSON bodies, a hand-made
router, `asyncio`, and a minimal ASGI application. The second half rebuilds the same ideas with
FastAPI — routes, typed parameters and validation, Pydantic request bodies, error handling,
response models, dependencies, asynchronous endpoints — and finishes by writing API tests.

**Packages:** standard library for steps 1–7; `fastapi` (with `httpx`, used by
`fastapi.testclient.TestClient`) from step 8. No server is started and no network is used:
tests call the application in-process, and external services are replaced by fakes.
**Prerequisite:** the Python topic only; you can take this topic any time after Python.

**Project ideas:** ungraded briefs between steps suggest things to build with what you have learned so far.
''',
}
