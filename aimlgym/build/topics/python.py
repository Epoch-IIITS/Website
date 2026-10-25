"""Problem definitions for the python topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- greeting-formatter
{
"slug": "greeting-formatter", "title": "Greeting Formatter",
"difficulty": "beginner", "prereqs": ["for-loops-range"], "packages": [],
"objectives": ["Define a function with a default argument", "Use str.strip and f-strings",
               "Return a value instead of printing it"],
"tags": ["functions", "strings", "f-strings", "default-arguments"],
"sources": ["S001", "S005"], "entry": "greet(name='World')",
"article": r'''
# Functions, Strings and f-strings

## Intuition
A function is a named recipe: you give it ingredients (arguments) and it hands back a result
(the return value). Most bugs in beginner code come from mixing up *printing* something with
*returning* it. Printing shows text to a human; returning gives a value to the rest of the
program — and to the automatic tests.

## Precise explanation
```python
def greet(name="World"):
    return f"Hello, {name}!"
```
* `def` creates a function object and binds it to the name `greet`.
* `name="World"` is a **default argument**: if the caller passes nothing, `name` is `"World"`.
* An **f-string** (`f"..."`) evaluates every `{expression}` inside it and inserts the result.
* `return` ends the function and sends the value back to the caller. A function with no
  `return` returns `None`.

Useful string methods: `s.strip()` removes leading/trailing whitespace; `s.title()`
capitalises each word; `s.lower()` / `s.upper()` change case. Strings are **immutable** — each
method returns a *new* string and leaves the original unchanged.

## Worked example
```python
>>> raw = "   ada lovelace  "
>>> clean = raw.strip()        # 'ada lovelace'
>>> clean.title()              # 'Ada Lovelace'
>>> f"Hello, {clean.title()}!"
'Hello, Ada Lovelace!'
>>> raw                        # unchanged
'   ada lovelace  '
```

## Common mistakes
* Using `print(...)` inside the function and forgetting `return` → the caller receives `None`.
* Writing `raw.strip()` on its own line and expecting `raw` to change (strings are immutable).
* Forgetting the `f` prefix, which produces the literal text `{name}`.
* Using a mutable default such as `def f(x=[])` — the same list is shared between calls.

## Why this matters
Every later exercise — from a NumPy helper to an agent tool — is a function whose *return
value* is checked. Clean input normalisation (strip, lower) is also the first step of every
text-processing pipeline in NLP.
''',
"statement": r'''
Write `greet(name="World")` that returns a greeting string.

**Requirements**
1. Remove leading and trailing whitespace from `name`.
2. If the cleaned name is empty, use `"World"`.
3. Convert the name to title case (`str.title()`).
4. Return exactly `"Hello, <Name>!"`. Do not print anything.

**Constraints:** `name` is a `str` of length 0–100.

**Return format:** a `str`.

**Examples**
```python
greet()                    # 'Hello, World!'   — default argument used
greet("  ada lovelace ")   # 'Hello, Ada Lovelace!' — stripped, then title-cased
greet("   ")               # 'Hello, World!'   — only spaces → empty after strip
```
''',
"starter": r'''
def greet(name="World"):
    """Return 'Hello, <Name>!' with the name stripped and title-cased."""
    # TODO: clean the name, fall back to "World" if empty, return the f-string
    pass
''',
"hints": [
    "Start with `name = name.strip()`; remember strip returns a new string.",
    "An empty string is falsy, so `if not name:` detects it.",
    "Build the answer with `f\"Hello, {name.title()}!\"` and `return` it.",
],
"solution": r'''
def greet(name="World"):
    name = name.strip()
    if not name:
        name = "World"
    return f"Hello, {name.title()}!"
''',
"explanation": r'''
The function normalises its input first (strip), handles the empty case by falling back to the
default, and only then formats. Doing validation before formatting keeps each step simple and
means the f-string always receives a clean, non-empty name. `str.title()` is applied inside the
f-string so the stored value stays as the user typed it (minus whitespace).
''',
"tests": r'''
class TestGreet(unittest.TestCase):
    def test_default(self):
        self.assertEqual(S.greet(), "Hello, World!")

    def test_simple_name(self):
        self.assertEqual(S.greet("alice"), "Hello, Alice!")

    def test_strip_and_title(self):
        self.assertEqual(S.greet("  ada lovelace "), "Hello, Ada Lovelace!")

    def test_only_spaces(self):
        self.assertEqual(S.greet("   "), "Hello, World!")

    def test_empty_string(self):
        self.assertEqual(S.greet(""), "Hello, World!")

    def test_returns_str_not_none(self):
        self.assertIsInstance(S.greet("bob"), str)

    def test_already_capitalised(self):
        self.assertEqual(S.greet("GRACE HOPPER"), "Hello, Grace Hopper!")
''',
"feedback": [
    ("test_returns_str_not_none", "You probably used `print` instead of `return`."),
    ("test_strip_and_title", "Call `.strip()` before `.title()` and keep the result in a variable."),
    ("test_only_spaces", "Check for emptiness *after* stripping, not before."),
    ("test_already_capitalised", "`.title()` also lowercases the remaining letters — use it rather than `.capitalize()` on the first letter only."),
],
},
# ---------------------------------------------------------------- sum-and-mean
{
"slug": "sum-and-mean", "title": "Sum and Mean of a List",
"difficulty": "beginner", "prereqs": ["greeting-formatter"], "packages": [],
"objectives": ["Accumulate values in a loop", "Handle the empty-input edge case",
               "Return a tuple of results"],
"tags": ["loops", "accumulator", "tuples", "edge-cases"],
"sources": ["S001", "S003"], "entry": "sum_and_mean(nums)",
"article": r'''
# The Accumulator Pattern

## Intuition
To add up a column of numbers by hand you keep a running total and update it once per number.
In code this is the **accumulator pattern**: start a variable at a neutral value, then update it
inside a loop.

## Precise explanation
```python
total = 0            # neutral element for addition
for x in nums:
    total += x       # same as total = total + x
```
The mean (arithmetic average) of $n$ numbers is

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i.$$

It is undefined when $n = 0$, so code must decide what to do with an empty list. Here we return
`None` for the mean (the sum of an empty list is still `0`).

A function can return several values as a **tuple**: `return total, mean` returns
`(total, mean)`, which the caller can unpack: `t, m = sum_and_mean(data)`.

Python also provides `sum(nums)` and `statistics.mean(nums)`; the latter raises
`StatisticsError` on empty input. Writing the loop yourself once makes clear what those helpers do.

## Worked example
For `[2, 4, 9]`: total goes 0 → 2 → 6 → 15; n = 3; mean = 15 / 3 = 5.0.

## Common mistakes
* Dividing by `len(nums)` without checking for zero → `ZeroDivisionError`.
* Initialising `total = nums[0]` → crashes on an empty list and double-counts if you then loop
  over all items.
* Using `//` (floor division) instead of `/` → `7 // 2 == 3`, not `3.5`.

## Why this matters
Means appear everywhere: average loss per batch, average reward per episode, feature
standardisation. The empty-input edge case is the classic source of crashes in data pipelines.
''',
"statement": r'''
Write `sum_and_mean(nums)` returning a tuple `(total, mean)`.

**Requirements**
* `total` is the sum of the numbers (an `int` if all inputs are ints).
* `mean` is `total / len(nums)` as a `float`.
* For an empty list return `(0, None)`.
* Use a loop (do not call `sum` or `statistics`). Do not modify the input list.

**Constraints:** 0 ≤ `len(nums)` ≤ 10⁵; elements are ints or floats.

**Examples**
```python
sum_and_mean([2, 4, 9])     # (15, 5.0)
sum_and_mean([])            # (0, None)   — mean undefined for empty data
sum_and_mean([-1.5, 1.5])   # (0.0, 0.0)
```
''',
"starter": r'''
def sum_and_mean(nums):
    """Return (total, mean) of nums; mean is None for an empty list."""
    total = 0
    # TODO: loop and accumulate, then compute the mean safely
    return total, None
''',
"hints": [
    "Loop with `for x in nums:` and update `total += x`.",
    "Check `if len(nums) == 0:` (or `if not nums:`) before dividing.",
    "Use true division `/` so the mean is a float.",
],
"solution": r'''
def sum_and_mean(nums):
    total = 0
    count = 0
    for x in nums:
        total += x
        count += 1
    if count == 0:
        return 0, None
    return total, total / count
''',
"explanation": r'''
One pass over the data maintains two accumulators: the running total and the count. Counting
inside the loop means the function would also work for any iterable (not only lists). The empty
case is detected via `count == 0` before division, avoiding `ZeroDivisionError`.
''',
"tests": r'''
class TestSumAndMean(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(S.sum_and_mean([2, 4, 9]), (15, 5.0))

    def test_empty(self):
        self.assertEqual(S.sum_and_mean([]), (0, None))

    def test_single(self):
        self.assertEqual(S.sum_and_mean([7]), (7, 7.0))

    def test_floats_tolerance(self):
        t, m = S.sum_and_mean([0.1, 0.2, 0.3])
        self.assertAlmostEqual(t, 0.6, places=9)
        self.assertAlmostEqual(m, 0.2, places=9)

    def test_negative_cancel(self):
        t, m = S.sum_and_mean([-1.5, 1.5])
        self.assertAlmostEqual(t, 0.0)
        self.assertAlmostEqual(m, 0.0)

    def test_mean_is_true_division(self):
        self.assertEqual(S.sum_and_mean([1, 2])[1], 1.5)

    def test_input_not_modified(self):
        data = [3, 1, 2]
        S.sum_and_mean(data)
        self.assertEqual(data, [3, 1, 2])
''',
"feedback": [
    ("test_empty", "Return `(0, None)` before dividing; dividing by zero raises an error."),
    ("test_mean_is_true_division", "Use `/` not `//`."),
    ("test_floats_tolerance", "Floats are compared with a tolerance of 1e-9; make sure you return numbers, not strings."),
    ("test_single", "With one element the mean equals that element as a float."),
],
},
# ---------------------------------------------------------------- filter-evens
{
"slug": "filter-evens", "title": "Filter Even Numbers",
"difficulty": "beginner", "prereqs": ["sum-and-mean"], "packages": [],
"objectives": ["Use the modulo operator", "Write a list comprehension with a condition",
               "Preserve order while filtering"],
"tags": ["list-comprehension", "modulo", "filtering"],
"sources": ["S001"], "entry": "evens(nums)",
"article": r'''
# Filtering with List Comprehensions

## Intuition
Filtering means keeping the items that pass a test. In Python the most readable filter is a
**list comprehension**: "give me `x` for each `x` in `nums` if `x` is even".

## Precise explanation
`a % b` is the remainder of `a` divided by `b`. An integer `x` is even exactly when
`x % 2 == 0`. In Python `%` always returns a result with the sign of the divisor, so
`-4 % 2 == 0` and `-3 % 2 == 1`: the test works for negative numbers too.

```python
[x for x in nums if x % 2 == 0]
```
is equivalent to
```python
out = []
for x in nums:
    if x % 2 == 0:
        out.append(x)
```
Both keep the original order and build a **new** list.

## Worked example
`nums = [5, -4, 0, 7, 12]` → test each: 5%2=1 ✗, -4%2=0 ✓, 0%2=0 ✓, 7%2=1 ✗, 12%2=0 ✓ →
`[-4, 0, 12]`.

## Common mistakes
* Testing `x % 2 == 1` for "odd" and then negating incorrectly; just test `== 0`.
* Removing items from a list while looping over it — skips elements. Build a new list instead.
* Forgetting that `0` is even.

## Why this matters
Boolean filtering is the same idea as NumPy masks (`a[a % 2 == 0]`) and pandas row selection
(`df[df.score > 50]`), which you will use constantly.
''',
"statement": r'''
Write `evens(nums)` that returns a new list containing only the even integers of `nums`, in
their original order.

**Constraints:** `nums` is a list of 0–10⁵ integers (may be negative). Do not modify `nums`.

**Examples**
```python
evens([5, -4, 0, 7, 12])   # [-4, 0, 12]  — 0 and negatives handled
evens([1, 3, 5])           # []           — nothing passes the test
```
''',
"starter": r'''
def evens(nums):
    """Return the even numbers of nums in order."""
    # TODO
    return []
''',
"hints": [
    "A number is even when `x % 2 == 0`.",
    "A list comprehension can include `if` at the end.",
    "`return [x for x in nums if x % 2 == 0]`",
],
"solution": r'''
def evens(nums):
    return [x for x in nums if x % 2 == 0]
''',
"explanation": r'''
A conditional list comprehension iterates once, keeps elements whose remainder modulo 2 is zero,
and returns a new list, so the input is untouched and order is preserved. Python's `%` makes
the test correct for negative numbers.
''',
"tests": r'''
class TestEvens(unittest.TestCase):
    def test_mixed(self):
        self.assertEqual(S.evens([5, -4, 0, 7, 12]), [-4, 0, 12])

    def test_none_even(self):
        self.assertEqual(S.evens([1, 3, 5]), [])

    def test_empty(self):
        self.assertEqual(S.evens([]), [])

    def test_all_even_order(self):
        self.assertEqual(S.evens([8, 2, 6]), [8, 2, 6])

    def test_negatives(self):
        self.assertEqual(S.evens([-3, -2, -1]), [-2])

    def test_duplicates_kept(self):
        self.assertEqual(S.evens([2, 2, 3, 2]), [2, 2, 2])

    def test_not_modified(self):
        data = [1, 2, 3]
        S.evens(data)
        self.assertEqual(data, [1, 2, 3])
''',
"feedback": [
    ("test_mixed", "Is 0 included? It is even."),
    ("test_all_even_order", "Do not sort — keep the original order."),
    ("test_not_modified", "Build a new list; don't call `.remove()` on the input."),
    ("test_duplicates_kept", "Filtering keeps duplicates; don't convert to a set."),
],
},
# ---------------------------------------------------------------- vowel-counter
{
"slug": "vowel-counter", "title": "Vowel Counter",
"difficulty": "beginner", "prereqs": ["filter-evens"], "packages": [],
"objectives": ["Iterate over characters of a string", "Use dictionaries as counters",
               "Normalise case before comparing"],
"tags": ["strings", "dictionaries", "counting", "membership"],
"sources": ["S001"], "entry": "count_vowels(text)",
"article": r'''
# Counting with Dictionaries

## Intuition
Counting how often each vowel appears is like tallying votes: one box per candidate, add a mark
for each vote. A **dictionary** maps keys (the candidates) to values (the tallies).

## Precise explanation
* Iterating over a string yields its characters: `for ch in "hey": ...` gives `'h'`, `'e'`, `'y'`.
* `ch in "aeiou"` tests membership (works for strings, lists, sets, dict keys).
* Initialise all counters so missing vowels report 0:
  `counts = {v: 0 for v in "aeiou"}` (a **dict comprehension**).
* Lower-case once (`text.lower()`) so `'A'` and `'a'` are counted together.

```python
counts = {v: 0 for v in "aeiou"}
for ch in text.lower():
    if ch in counts:
        counts[ch] += 1
```

## Worked example
`"Banana Split!"` → lower: `"banana split!"` → a appears 3 times, i once →
`{'a': 3, 'e': 0, 'i': 1, 'o': 0, 'u': 0}`; total = 4.

## Common mistakes
* Forgetting to lowercase, so capital vowels are missed.
* Writing `counts[ch] += 1` for a key that doesn't exist → `KeyError`. Pre-fill keys or use
  `dict.get(ch, 0) + 1`.
* Counting `'y'` — this problem defines vowels as `a e i o u` only.

## Why this matters
Frequency counting is the foundation of bag-of-words models, n-gram language models and
histograms. `collections.Counter` does this for you; knowing the manual version helps you read it.
''',
"statement": r'''
Write `count_vowels(text)` returning `(total, counts)` where `counts` is a dict with exactly the
keys `'a','e','i','o','u'` mapped to how many times each occurs in `text` (case-insensitive), and
`total` is the sum of those counts.

**Constraints:** `text` is a `str` of length 0–10⁵. Only the five ASCII vowels count.

**Examples**
```python
count_vowels("Banana Split!")
# (4, {'a': 3, 'e': 0, 'i': 1, 'o': 0, 'u': 0})
count_vowels("rhythm")
# (0, {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0})   — 'y' is not a vowel here
```
''',
"starter": r'''
def count_vowels(text):
    """Return (total, counts) for the vowels a, e, i, o, u (case-insensitive)."""
    counts = {}
    # TODO
    return 0, counts
''',
"hints": [
    "Create `counts = {v: 0 for v in 'aeiou'}` so every key exists.",
    "Loop over `text.lower()` and test `if ch in counts`.",
    "`total = sum(counts.values())`.",
],
"solution": r'''
def count_vowels(text):
    counts = {v: 0 for v in "aeiou"}
    for ch in text.lower():
        if ch in counts:
            counts[ch] += 1
    return sum(counts.values()), counts
''',
"explanation": r'''
Pre-filling the dictionary guarantees all five keys appear even when a vowel is absent. Lowering
the text once makes the comparison case-insensitive. Membership in a dict is an O(1) lookup, so
the whole function is a single linear pass.
''',
"tests": r'''
ZERO = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

class TestVowels(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.count_vowels("Banana Split!"),
                         (4, {"a": 3, "e": 0, "i": 1, "o": 0, "u": 0}))

    def test_no_vowels(self):
        self.assertEqual(S.count_vowels("rhythm"), (0, ZERO))

    def test_empty(self):
        self.assertEqual(S.count_vowels(""), (0, ZERO))

    def test_uppercase(self):
        self.assertEqual(S.count_vowels("AEIOU aeiou"),
                         (10, {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}))

    def test_keys_exact(self):
        self.assertEqual(set(S.count_vowels("xyz")[1].keys()), set("aeiou"))

    def test_total_matches(self):
        total, counts = S.count_vowels("Machine Learning")
        self.assertEqual(total, sum(counts.values()))
        self.assertEqual(total, 6)
''',
"feedback": [
    ("test_uppercase", "Lower-case the text before counting."),
    ("test_keys_exact", "All five vowel keys must be present, even with count 0."),
    ("test_no_vowels", "'y' is not counted in this problem."),
    ("test_total_matches", "`total` must equal the sum of the dictionary values."),
],
},
# ---------------------------------------------------------------- unique-words
{
"slug": "unique-words", "title": "Unique Words in Order",
"difficulty": "intermediate", "prereqs": ["standard-library"], "packages": [],
"objectives": ["Normalise tokens (case, punctuation)", "Use a set for fast membership",
               "Preserve first-occurrence order"],
"tags": ["sets", "strings", "deduplication", "order-preservation"],
"sources": ["S001"], "entry": "unique_words(sentence)",
"article": r'''
# Sets, Order and Normalisation

## Intuition
A **set** remembers *whether* you have seen something, not *when*. To list unique words in the
order they first appeared, combine a set (fast "seen?" checks) with a list (keeps order).

## Precise explanation
* `set()` stores unique hashable items; `x in s` is on average O(1).
* Converting a list to a set loses order: `list(set(words))` may come back in any order.
* Pattern:
```python
seen, out = set(), []
for w in words:
    if w not in seen:
        seen.add(w)
        out.append(w)
```
* Normalisation: two tokens should count as the same word if they differ only in case or in
  surrounding punctuation. `w.strip(string.punctuation).lower()` removes punctuation from both
  ends only (so the apostrophe in "don't" survives).
* `str.split()` with no argument splits on any run of whitespace and drops empty strings.

## Worked example
`"The cat saw the CAT, then the dog."` → split → `The, cat, saw, the, CAT,, then, the, dog.` →
normalise → `the, cat, saw, the, cat, then, the, dog` → unique in order →
`['the', 'cat', 'saw', 'then', 'dog']`.

## Common mistakes
* `sorted(set(words))` — alphabetical, not first-occurrence order.
* `split(" ")` — produces empty strings for double spaces.
* Stripping *all* punctuation characters with `replace`, which turns "don't" into "dont".
* Keeping tokens that become empty after stripping (e.g. a lone "—").

## Why this matters
Building a vocabulary (word → index) for NLP models is exactly this operation; the order
determines each word's index, so it must be deterministic.
''',
"statement": r'''
Write `unique_words(sentence)` that returns the list of distinct words in order of first
appearance.

**Rules**
1. Split on whitespace with `str.split()`.
2. Normalise each token: strip characters in `string.punctuation` from both ends, then lowercase.
3. Discard tokens that are empty after stripping.
4. Keep the first occurrence of each normalised word.

**Constraints:** `len(sentence)` ≤ 10⁵.

**Examples**
```python
unique_words("The cat saw the CAT, then the dog.")
# ['the', 'cat', 'saw', 'then', 'dog']
unique_words("Don't stop -- don't!")
# ["don't", 'stop']   — inner apostrophe kept; '--' becomes empty and is dropped
```
''',
"starter": r'''
import string


def unique_words(sentence):
    """Return distinct normalised words in first-occurrence order."""
    # TODO
    return []
''',
"hints": [
    "`token.strip(string.punctuation).lower()` normalises one token.",
    "Skip a token if it is empty after normalising.",
    "Use a `seen` set alongside an output list to keep order.",
],
"solution": r'''
import string


def unique_words(sentence):
    seen = set()
    out = []
    for token in sentence.split():
        word = token.strip(string.punctuation).lower()
        if word and word not in seen:
            seen.add(word)
            out.append(word)
    return out
''',
"explanation": r'''
Each token is normalised by stripping punctuation from its ends and lowercasing. The set gives
constant-time duplicate checks while the list records first-occurrence order. Empty tokens
(pure punctuation) are skipped by the `if word` condition.
''',
"tests": r'''
class TestUniqueWords(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.unique_words("The cat saw the CAT, then the dog."),
                         ["the", "cat", "saw", "then", "dog"])

    def test_apostrophe_and_dash(self):
        self.assertEqual(S.unique_words("Don't stop -- don't!"), ["don't", "stop"])

    def test_empty(self):
        self.assertEqual(S.unique_words(""), [])

    def test_only_punctuation(self):
        self.assertEqual(S.unique_words("!!! ... ,"), [])

    def test_multiple_spaces(self):
        self.assertEqual(S.unique_words("a   b\tA\nb"), ["a", "b"])

    def test_order_not_sorted(self):
        self.assertEqual(S.unique_words("zebra apple zebra mango"), ["zebra", "apple", "mango"])

    def test_returns_list(self):
        self.assertIsInstance(S.unique_words("x"), list)
''',
"feedback": [
    ("test_order_not_sorted", "Don't sort; keep first-occurrence order."),
    ("test_apostrophe_and_dash", "Strip punctuation only from the ends (str.strip), and drop empty tokens."),
    ("test_multiple_spaces", "Use `split()` with no argument to handle tabs/newlines/multiple spaces."),
    ("test_only_punctuation", "Tokens that are empty after stripping must not be added."),
],
},
# ---------------------------------------------------------------- factorial-validated
{
"slug": "factorial-validated", "title": "Validated Factorial",
"difficulty": "intermediate", "prereqs": ["gradebook-aggregate"], "packages": [],
"objectives": ["Raise exceptions for invalid input", "Use isinstance checks correctly",
               "Compute a product iteratively"],
"tags": ["exceptions", "validation", "loops", "integers"],
"sources": ["S001"], "entry": "factorial(n)",
"article": r'''
# Validating Input and Raising Exceptions

## Intuition
A function has a *contract*: what it accepts and what it promises to return. When a caller
breaks the contract (e.g. asks for the factorial of −3), the function should fail **loudly**
with a clear error rather than return a wrong answer silently.

## Precise explanation
The factorial of a non-negative integer $n$ is $n! = 1 \cdot 2 \cdots n$, with $0! = 1$ (the
empty product).

```python
result = 1
for k in range(2, n + 1):
    result *= k
```
Python integers have arbitrary precision, so `factorial(50)` is exact.

**Raising exceptions**
* `TypeError` — the argument has the wrong *type* (e.g. `2.5`, `"5"`).
* `ValueError` — right type, unacceptable *value* (e.g. `-3`).
```python
if not isinstance(n, int) or isinstance(n, bool):
    raise TypeError("n must be an int")
if n < 0:
    raise ValueError("n must be >= 0")
```
`bool` is a subclass of `int` in Python (`True == 1`), so it must be excluded explicitly if you
want to reject it.

## Worked example
`factorial(5)`: result 1 → ×2 = 2 → ×3 = 6 → ×4 = 24 → ×5 = 120.

## Common mistakes
* Returning `-1` or `None` for bad input — the caller may not notice.
* `range(1, n)` — stops at n−1 (off-by-one).
* Recursion without a base case for 0 → infinite recursion.
* Accepting `5.0` because `5.0 == 5`; the contract asks for an `int`.

## Why this matters
ML code fails in confusing ways deep inside a pipeline when inputs are invalid. Early, specific
exceptions turn a mysterious NaN three steps later into an obvious message. Factorials also
power combinatorics (binomial coefficients, [[binomial-coefficient]]).
''',
"statement": r'''
Write `factorial(n)`.

**Requirements**
* Return $n!$ as an `int` for integers $n \ge 0$ (with $0! = 1$). Use a loop, not `math.factorial`.
* Raise `TypeError` if `n` is not an `int`, or is a `bool`.
* Raise `ValueError` if `n < 0`.

**Constraints:** 0 ≤ n ≤ 1000 for valid input.

**Examples**
```python
factorial(5)     # 120
factorial(0)     # 1      — empty product
factorial(-2)    # raises ValueError
factorial(3.0)   # raises TypeError — floats are rejected even if whole
```
''',
"starter": r'''
def factorial(n):
    """Return n! for int n >= 0; raise TypeError/ValueError for invalid input."""
    # TODO: validate, then multiply 1 * 2 * ... * n
    pass
''',
"hints": [
    "Check the type first: `isinstance(n, bool) or not isinstance(n, int)`.",
    "Then check `n < 0` and raise `ValueError`.",
    "Start `result = 1` and multiply by `k` for `k in range(2, n + 1)`.",
],
"solution": r'''
def factorial(n):
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result
''',
"explanation": r'''
Type validation comes before value validation so that comparing `n < 0` is never attempted on,
say, a string. `bool` is rejected explicitly because it is a subclass of `int`. The loop starts
at 2 because multiplying by 1 changes nothing; for n = 0 or 1 the loop body never runs and the
empty product 1 is returned.
''',
"tests": r'''
class TestFactorial(unittest.TestCase):
    def test_five(self):
        self.assertEqual(S.factorial(5), 120)

    def test_zero_and_one(self):
        self.assertEqual(S.factorial(0), 1)
        self.assertEqual(S.factorial(1), 1)

    def test_large_exact(self):
        self.assertEqual(S.factorial(25), 15511210043330985984000000)

    def test_negative(self):
        with self.assertRaises(ValueError):
            S.factorial(-2)

    def test_float(self):
        with self.assertRaises(TypeError):
            S.factorial(3.0)

    def test_string(self):
        with self.assertRaises(TypeError):
            S.factorial("4")

    def test_bool(self):
        with self.assertRaises(TypeError):
            S.factorial(True)
''',
"feedback": [
    ("test_zero_and_one", "0! is defined as 1; make sure your loop handles n = 0."),
    ("test_float", "Use isinstance(n, int); 3.0 is a float even though it equals 3."),
    ("test_bool", "bool is a subclass of int — check for it explicitly."),
    ("test_negative", "Raise ValueError (not return) when n < 0."),
],
},
# ---------------------------------------------------------------- fibonacci-sequence
{
"slug": "fibonacci-sequence", "title": "Fibonacci Sequence",
"difficulty": "intermediate", "prereqs": ["vowel-counter"], "packages": [],
"objectives": ["Maintain state across loop iterations", "Use tuple assignment",
               "Handle small-n boundary cases"],
"tags": ["loops", "sequences", "tuple-unpacking", "state"],
"sources": ["S001"], "entry": "fibonacci(n)",
"article": r'''
# Loop State and Tuple Assignment

## Intuition
Each Fibonacci number is the sum of the previous two: 0, 1, 1, 2, 3, 5, 8, … To generate them
you only need to remember the *last two* values — a sliding window of state.

## Precise explanation
$F_0 = 0,\; F_1 = 1,\; F_k = F_{k-1} + F_{k-2}$ for $k \ge 2$.

**Tuple assignment** evaluates the whole right-hand side first, then assigns:
```python
a, b = 0, 1
for _ in range(n):
    out.append(a)
    a, b = b, a + b    # new a = old b, new b = old a + old b
```
Without tuple assignment you would need a temporary variable (`t = a + b; a = b; b = t`).
Writing `a = b` then `b = a + b` is a bug: `a` has already changed.

`_` is a conventional name for a loop variable you don't use.

## Worked example (n = 6)
| step | append a | (a, b) after |
|---|---|---|
| 1 | 0 | (1, 1) |
| 2 | 1 | (1, 2) |
| 3 | 1 | (2, 3) |
| 4 | 2 | (3, 5) |
| 5 | 3 | (5, 8) |
| 6 | 5 | (8, 13) |

Result: `[0, 1, 1, 2, 3, 5]`.

## Common mistakes
* Naive recursion `fib(k-1) + fib(k-2)` — exponential time; n = 40 takes seconds.
* Special-casing n = 1 and n = 2 with hard-coded lists and getting n = 0 wrong.
* Sequential (not simultaneous) assignment, as described above.

## Why this matters
Carrying a small amount of state through a loop is the core of running averages, momentum in
optimizers ([[sgd-momentum]]) and discounted returns in RL ([[discounted-return]]).
''',
"statement": r'''
Write `fibonacci(n)` returning a list of the first `n` Fibonacci numbers, starting `0, 1, ...`.

**Requirements:** iterative (O(n) time); `n = 0` returns `[]`; a negative `n` also returns `[]` (raising errors for bad input comes later, in [[factorial-validated]]).

**Constraints:** 0 ≤ n ≤ 10⁴.

**Examples**
```python
fibonacci(6)   # [0, 1, 1, 2, 3, 5]
fibonacci(1)   # [0]
fibonacci(0)   # []
```
''',
"starter": r'''
def fibonacci(n):
    """Return the first n Fibonacci numbers [0, 1, 1, 2, ...]."""
    out = []
    # TODO
    return out
''',
"hints": [
    "Keep two variables `a, b = 0, 1`.",
    "Each iteration: append `a`, then `a, b = b, a + b`.",
    "Loop exactly `n` times with `for _ in range(n)`; `range(n)` is empty when n ≤ 0, so no special case is needed.",
],
"solution": r'''
def fibonacci(n):
    out = []
    a, b = 0, 1
    for _ in range(n):
        out.append(a)
        a, b = b, a + b
    return out
''',
"explanation": r'''
Two variables hold the current and next Fibonacci numbers. Simultaneous tuple assignment advances
the window by one step. Because the loop runs exactly n times, the n = 0 and n = 1 cases need no
special handling.
''',
"tests": r'''
class TestFibonacci(unittest.TestCase):
    def test_six(self):
        self.assertEqual(S.fibonacci(6), [0, 1, 1, 2, 3, 5])

    def test_zero(self):
        self.assertEqual(S.fibonacci(0), [])

    def test_one(self):
        self.assertEqual(S.fibonacci(1), [0])

    def test_two(self):
        self.assertEqual(S.fibonacci(2), [0, 1])

    def test_negative(self):
        self.assertEqual(S.fibonacci(-1), [])

    def test_recurrence_holds(self):
        f = S.fibonacci(50)
        self.assertEqual(len(f), 50)
        for k in range(2, 50):
            self.assertEqual(f[k], f[k - 1] + f[k - 2])

    def test_fast_large(self):
        f = S.fibonacci(5000)
        self.assertEqual(len(f), 5000)
''',
"feedback": [
    ("test_one", "The sequence starts with 0, so fibonacci(1) is [0]."),
    ("test_recurrence_holds", "Check simultaneous assignment `a, b = b, a + b`."),
    ("test_fast_large", "Avoid recursion; an O(n) loop finishes instantly."),
    ("test_negative", "A negative n should give an empty list; `range(n)` already does this."),
],
},
# ---------------------------------------------------------------- safe-divide
{
"slug": "safe-divide", "title": "Safe Division with Exceptions",
"difficulty": "intermediate", "prereqs": ["matrix-transpose"], "packages": [],
"objectives": ["Catch specific exceptions with try/except", "Distinguish recoverable and unrecoverable errors",
               "Process a batch while recording failures"],
"tags": ["exceptions", "try-except", "error-handling", "batch-processing"],
"sources": ["S001"], "entry": "safe_divide(a, b); divide_pairs(pairs)",
"article": r'''
# Handling Exceptions Deliberately

## Intuition
Some errors are expected and recoverable (dividing by zero in a ratio where "undefined" is a
fine answer); others signal a bug (passing a string where a number belongs). Good code catches
the first kind *specifically* and lets the second kind surface.

## Precise explanation
```python
try:
    result = a / b
except ZeroDivisionError:
    result = None
```
* Code in `try` runs; if an exception is raised, Python looks for a matching `except`.
* Catch the **narrowest** exception you can handle. A bare `except:` or `except Exception:`
  also swallows typos (`NameError`) and type bugs, hiding real problems.
* `else:` runs only if no exception occurred; `finally:` always runs.
* Division by zero: `1 / 0` raises `ZeroDivisionError`, and so does `1.0 / 0.0` in plain Python
  (NumPy instead returns `inf` with a warning).

**Batch processing pattern:** process each item, store the result or a marker, and keep a list
of the indices that failed — one bad record should not abort a whole dataset.

## Worked example
`divide_pairs([(6, 3), (1, 0), (5, 2)])` → results `[2.0, None, 2.5]`, failed indices `[1]`.

## Common mistakes
* `except:` with no type → hides `TypeError` from `safe_divide("6", 3)`.
* Checking `if b == 0` only — fine for numbers, but the exercise asks you to practise exceptions.
* Returning the error message string as the result, mixing types in the output list.

## Why this matters
Data loaders, tool-calling agents ([[validate-and-retry]]) and federated clients that drop out (FL topics) all
need the same skill: recover from expected failures, record them, continue.
''',
"statement": r'''
Implement two functions.

1. `safe_divide(a, b)` → `a / b` as a float, or `None` if `b` is zero. Catch **only**
   `ZeroDivisionError`; any other error (e.g. `TypeError` for strings) must propagate.
2. `divide_pairs(pairs)` → `(results, failed)` where `results[i] = safe_divide(*pairs[i])` and
   `failed` is the sorted list of indices whose result is `None`.

**Constraints:** numbers are ints or floats; `len(pairs)` ≤ 10⁵.

**Examples**
```python
safe_divide(7, 2)          # 3.5
safe_divide(1, 0)          # None
safe_divide("6", 3)        # raises TypeError (not caught)
divide_pairs([(6, 3), (1, 0), (5, 2)])   # ([2.0, None, 2.5], [1])
```
''',
"starter": r'''
def safe_divide(a, b):
    """Return a / b, or None if b is zero. Do not hide other errors."""
    # TODO: use try/except ZeroDivisionError
    pass


def divide_pairs(pairs):
    """Return (results, failed_indices)."""
    # TODO
    return [], []
''',
"hints": [
    "Wrap only the division in `try:` and catch `except ZeroDivisionError:`.",
    "Use `enumerate(pairs)` to get each index.",
    "Append the index to `failed` when the result `is None`.",
],
"solution": r'''
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def divide_pairs(pairs):
    results = []
    failed = []
    for i, (a, b) in enumerate(pairs):
        r = safe_divide(a, b)
        results.append(r)
        if r is None:
            failed.append(i)
    return results, failed
''',
"explanation": r'''
`safe_divide` catches exactly one exception type, so programming errors such as dividing a
string still raise `TypeError`. `divide_pairs` reuses it, records `None` for failures and the
index of each failure. Indices come out sorted automatically because the loop visits them in order.
''',
"tests": r'''
class TestSafeDivide(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(S.safe_divide(7, 2), 3.5)

    def test_zero(self):
        self.assertIsNone(S.safe_divide(1, 0))

    def test_float_zero(self):
        self.assertIsNone(S.safe_divide(1.0, 0.0))

    def test_type_error_propagates(self):
        with self.assertRaises(TypeError):
            S.safe_divide("6", 3)

    def test_pairs(self):
        self.assertEqual(S.divide_pairs([(6, 3), (1, 0), (5, 2)]), ([2.0, None, 2.5], [1]))

    def test_pairs_empty(self):
        self.assertEqual(S.divide_pairs([]), ([], []))

    def test_pairs_all_fail(self):
        self.assertEqual(S.divide_pairs([(1, 0), (0, 0)]), ([None, None], [0, 1]))

    def test_zero_numerator_ok(self):
        self.assertEqual(S.divide_pairs([(0, 5)]), ([0.0], []))
''',
"feedback": [
    ("test_type_error_propagates", "Catch only ZeroDivisionError; a bare except hides TypeError."),
    ("test_zero_numerator_ok", "0 / 5 is 0.0, a valid result — only a None result counts as failed. Use `is None`, not `not r`."),
    ("test_pairs", "Use enumerate to record indices of failures."),
    ("test_float_zero", "Plain Python raises ZeroDivisionError for 1.0/0.0 too."),
],
},
# ---------------------------------------------------------------- text-stats-stdin
{
"slug": "text-stats-stdin", "title": "Text Statistics from stdin",
"difficulty": "advanced", "prereqs": ["files-and-json"], "packages": [],
"objectives": ["Read all of standard input", "Separate pure logic from I/O",
               "Format output exactly"],
"tags": ["stdin", "io", "strings", "program-structure"],
"sources": ["S001"], "entry": "text_stats(text); main()",
"article": r'''
# Programs that Read Standard Input

## Intuition
Online judges and code runners such as Piston feed your program text on **standard input
(stdin)** and compare what it prints on **standard output (stdout)**. The trick to writing such
programs well is to keep the *logic* in a pure function you can test, and keep the *I/O* in a
tiny `main()`.

## Precise explanation
* `sys.stdin.read()` returns everything on stdin as one string (possibly empty).
* `text.splitlines()` splits on line boundaries without keeping `\n`. A trailing newline does
  not create an extra empty line: `"a\nb\n".splitlines() == ['a', 'b']`.
* Words: `text.split()` (whitespace-separated tokens).
* Characters: `len(text)` counts every character including spaces and newlines.
* The guard `if __name__ == "__main__": main()` runs `main` only when the file is executed as a
  script, not when it is imported by tests.

```python
def main():
    text = sys.stdin.read()
    lines, words, chars = text_stats(text)
    print(f"lines={lines} words={words} chars={chars}")
```

## Worked example
stdin = `"to be\nor not\n"` → splitlines → 2 lines; split → 4 words; len → 13 chars.
Output: `lines=2 words=4 chars=13`.

## Common mistakes
* `text.count("\n")` for lines — wrong when the last line has no trailing newline.
* Calling `input()` in a loop and crashing with `EOFError` at end of input.
* Printing extra spaces or a different label format — exact-match graders reject it.
* Putting `print` inside `text_stats`, which makes it hard to test.

## Why this matters
Separating computation from I/O is how all testable software is structured — the same idea
reappears when agents (AG topics) separate the "model" from the "tools".
''',
"statement": r'''
Implement:

1. `text_stats(text)` → tuple `(lines, words, chars)` where
   `lines = len(text.splitlines())`, `words = len(text.split())`, `chars = len(text)`.
2. `main()` → reads **all** of stdin, prints exactly one line
   `lines=<L> words=<W> chars=<C>` and returns `None`.

Guard the call with `if __name__ == "__main__":`.

**stdin/stdout format**
```
input  (stdin):  to be\nor not\n
output (stdout): lines=2 words=4 chars=13
```

**Examples**
```python
text_stats("to be\nor not\n")   # (2, 4, 13)
text_stats("")                  # (0, 0, 0)  — empty input
text_stats("one line no newline")  # (1, 4, 19)
```
''',
"starter": r'''
import sys


def text_stats(text):
    """Return (lines, words, chars) for text."""
    # TODO
    return 0, 0, 0


def main():
    # TODO: read stdin, print 'lines=.. words=.. chars=..'
    pass


if __name__ == "__main__":
    main()
''',
"hints": [
    "`len(text.splitlines())`, `len(text.split())`, `len(text)`.",
    "In `main`, `text = sys.stdin.read()`.",
    "Use an f-string with exactly one space between fields.",
],
"solution": r'''
import sys


def text_stats(text):
    return len(text.splitlines()), len(text.split()), len(text)


def main():
    text = sys.stdin.read()
    lines, words, chars = text_stats(text)
    print(f"lines={lines} words={words} chars={chars}")


if __name__ == "__main__":
    main()
''',
"explanation": r'''
All counting lives in `text_stats`, which is pure and easy to test. `main` is three lines of I/O:
read everything, compute, print once. `splitlines` handles a missing final newline correctly,
which `count("\n")` would not.
''',
"tests": r'''
import io
import subprocess
from contextlib import redirect_stdout
from unittest import mock


class TestTextStats(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.text_stats("to be\nor not\n"), (2, 4, 13))

    def test_empty(self):
        self.assertEqual(S.text_stats(""), (0, 0, 0))

    def test_no_trailing_newline(self):
        self.assertEqual(S.text_stats("one line no newline"), (1, 4, 19))

    def test_blank_lines(self):
        self.assertEqual(S.text_stats("a\n\n b \n"), (3, 2, 7))

    def test_main_output(self):
        buf = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO("to be\nor not\n")), redirect_stdout(buf):
            S.main()
        self.assertEqual(buf.getvalue(), "lines=2 words=4 chars=13\n")

    def test_main_empty(self):
        buf = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO("")), redirect_stdout(buf):
            S.main()
        self.assertEqual(buf.getvalue(), "lines=0 words=0 chars=0\n")

    def test_as_script(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), S.__name__ + ".py")
        r = subprocess.run([sys.executable, path], input="x y z\n", capture_output=True,
                           text=True, timeout=30)
        self.assertEqual(r.stdout, "lines=1 words=3 chars=6\n")
''',
"feedback": [
    ("test_no_trailing_newline", "Count lines with splitlines(), not count('\\n')."),
    ("test_main_output", "Print exactly `lines=L words=W chars=C` with single spaces."),
    ("test_as_script", "Add `if __name__ == \"__main__\": main()` at the bottom."),
    ("test_blank_lines", "Blank lines still count as lines; words come from split()."),
],
},
# ---------------------------------------------------------------- guessing-game-feedback
{
"slug": "guessing-game-feedback", "title": "Guessing Game Feedback",
"difficulty": "advanced", "prereqs": ["safe-divide"], "packages": [],
"objectives": ["Write a loop with early termination", "Model game state deterministically",
               "Validate inputs and limits"],
"tags": ["loops", "break", "state-machines", "validation"],
"sources": ["S001"], "entry": "guess_feedback(target, guesses, max_attempts=7)",
"article": r'''
# Deterministic Game Loops

## Intuition
An interactive guessing game ("too low", "too high", "correct!") is really a loop over guesses
with a stopping condition. If we pass the guesses in as a list instead of calling `input()`, the
game becomes **deterministic** and testable — the same idea used to test agents with scripted
model outputs ([[react-loop]]).

## Precise explanation
* Loop over guesses; compare each to the target; produce one feedback string per guess.
* **Early termination:** `break` leaves the loop as soon as the guess is correct; later guesses
  are ignored.
* **Attempt limit:** stop after `max_attempts` guesses even if not solved.
* The final status depends on *how* the loop ended. Python's `for ... else` runs the `else`
  block only if the loop was **not** broken — handy, but a boolean flag is often clearer.

State summary returned as a dict:
```python
{"feedback": [...], "attempts": k, "won": True/False}
```

## Worked example
target = 42, guesses = [50, 25, 42, 10]:
50 → "too high", 25 → "too low", 42 → "correct" → stop. attempts = 3, won = True;
the guess 10 is never examined.

## Common mistakes
* Forgetting to `break`, so guesses after the correct one add feedback.
* Counting attempts with `len(guesses)` instead of guesses actually used.
* Off-by-one with the attempt limit (`>` vs `>=`).
* Using `input()` — untestable and blocks automated runners.

## Why this matters
Every agent, simulator and RL environment is a loop of "observe, act, check if done, stop at a
step budget". This is the smallest version of that loop.
''',
"statement": r'''
Write `guess_feedback(target, guesses, max_attempts=7)` returning a dict
`{"feedback": list[str], "attempts": int, "won": bool}`.

**Rules**
* Process guesses in order, at most `max_attempts` of them.
* For each processed guess append `"too low"`, `"too high"` or `"correct"`.
* Stop immediately after `"correct"`.
* `attempts` = number of guesses processed; `won` = whether `"correct"` occurred.
* Raise `ValueError` if `max_attempts < 1`.

**Constraints:** ints; `len(guesses)` ≤ 1000.

**Examples**
```python
guess_feedback(42, [50, 25, 42, 10])
# {'feedback': ['too high', 'too low', 'correct'], 'attempts': 3, 'won': True}
guess_feedback(5, [1, 2, 3], max_attempts=2)
# {'feedback': ['too low', 'too low'], 'attempts': 2, 'won': False}   — limit reached
```
''',
"starter": r'''
def guess_feedback(target, guesses, max_attempts=7):
    """Simulate a guessing game and return feedback, attempts and win flag."""
    # TODO
    return {"feedback": [], "attempts": 0, "won": False}
''',
"hints": [
    "Loop over `guesses[:max_attempts]`.",
    "Compare with `<`, `>`, `==` and append the right string.",
    "Set `won = True` and `break` on a correct guess; attempts = len(feedback).",
],
"solution": r'''
def guess_feedback(target, guesses, max_attempts=7):
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")
    feedback = []
    won = False
    for g in guesses[:max_attempts]:
        if g < target:
            feedback.append("too low")
        elif g > target:
            feedback.append("too high")
        else:
            feedback.append("correct")
            won = True
            break
    return {"feedback": feedback, "attempts": len(feedback), "won": won}
''',
"explanation": r'''
Slicing `guesses[:max_attempts]` enforces the attempt budget up front. Each guess produces one
feedback string; on a correct guess the flag is set and the loop breaks, so later guesses are
never processed. Because exactly one string is appended per processed guess, `attempts` is just
the length of the feedback list.
''',
"tests": r'''
class TestGuess(unittest.TestCase):
    def test_win(self):
        self.assertEqual(S.guess_feedback(42, [50, 25, 42, 10]),
                         {"feedback": ["too high", "too low", "correct"], "attempts": 3, "won": True})

    def test_limit(self):
        self.assertEqual(S.guess_feedback(5, [1, 2, 3], max_attempts=2),
                         {"feedback": ["too low", "too low"], "attempts": 2, "won": False})

    def test_first_try(self):
        self.assertEqual(S.guess_feedback(7, [7, 7]),
                         {"feedback": ["correct"], "attempts": 1, "won": True})

    def test_no_guesses(self):
        self.assertEqual(S.guess_feedback(3, []), {"feedback": [], "attempts": 0, "won": False})

    def test_win_on_last_allowed(self):
        r = S.guess_feedback(10, [1, 2, 10], max_attempts=3)
        self.assertTrue(r["won"])
        self.assertEqual(r["attempts"], 3)

    def test_correct_after_limit_ignored(self):
        r = S.guess_feedback(10, [1, 2, 10], max_attempts=2)
        self.assertFalse(r["won"])

    def test_bad_limit(self):
        with self.assertRaises(ValueError):
            S.guess_feedback(1, [1], max_attempts=0)
''',
"feedback": [
    ("test_win", "Stop the loop with `break` after a correct guess."),
    ("test_win_on_last_allowed", "Check your attempt-limit comparison: max_attempts guesses are allowed, not max_attempts-1."),
    ("test_correct_after_limit_ignored", "Only the first max_attempts guesses may be processed."),
    ("test_bad_limit", "Validate max_attempts before looping."),
],
},
# ---------------------------------------------------------------- gradebook-aggregate
{
"slug": "gradebook-aggregate", "title": "Gradebook Aggregation",
"difficulty": "intermediate", "prereqs": ["functions-as-values"], "packages": [],
"objectives": ["Group records with dict.setdefault / defaultdict", "Sort with a key function and tie-breaking",
               "Round results correctly"],
"tags": ["dictionaries", "grouping", "sorting", "lambda"],
"sources": ["S001"], "entry": "gradebook(records)",
"article": r'''
# Grouping and Sorting Records

## Intuition
Given a pile of (student, score) slips, you sort them into one stack per student, compute each
stack's average, then rank students. That is **group → aggregate → sort**, the same recipe as
SQL `GROUP BY` and pandas `groupby` ([[groupby-agg]]).

## Precise explanation
**Grouping** with a dict of lists:
```python
groups = {}
for name, score in records:
    groups.setdefault(name, []).append(score)
```
`setdefault(key, default)` returns the existing value or inserts `default` first.
`collections.defaultdict(list)` does the same automatically.

**Sorting with a key**: `sorted(items, key=f)` sorts by `f(item)`. To sort by average
descending and break ties by name ascending, use a tuple key with a negated number:
```python
sorted(rows, key=lambda r: (-r[1], r[0]))
```
Tuples compare element by element, so the name is consulted only when averages are equal.

**Rounding**: `round(x, 2)` rounds to 2 decimals (using round-half-to-even on the exact binary
value). Round only for the final output, never in intermediate steps.

## Worked example
records = [("ann", 90), ("bob", 70), ("ann", 80), ("cy", 85)]
groups: ann → [90, 80], bob → [70], cy → [85]; averages 85.0, 70.0, 85.0.
Sorted: (-85, "ann"), (-85, "cy"), (-70, "bob") → ann, cy, bob.

## Common mistakes
* `sorted(..., reverse=True)` with a tuple key reverses the name tie-break too.
* Rounding each score before averaging.
* Overwriting `groups[name] = [score]` instead of appending.

## Why this matters
Grouped statistics drive per-class metrics, per-client summaries in federated learning and
leaderboards; deterministic tie-breaking keeps outputs reproducible.
''',
"statement": r'''
Write `gradebook(records)` where `records` is a list of `(name, score)` tuples.

Return a list of `(name, average, count)` tuples:
* `average` = mean score rounded to 2 decimals (`round(x, 2)`), `count` = number of scores;
* sorted by average **descending**, ties broken by name **ascending**.

Ignore records whose score is not in `[0, 100]` (they do not count).

**Constraints:** ≤ 10⁵ records; names are non-empty strings; scores are ints/floats.

**Examples**
```python
gradebook([("ann", 90), ("bob", 70), ("ann", 80), ("cy", 85)])
# [('ann', 85.0, 2), ('cy', 85.0, 1), ('bob', 70.0, 1)]  — tie on 85 broken by name
gradebook([("x", 101), ("x", 50)])
# [('x', 50.0, 1)]  — 101 is out of range and ignored
```
''',
"starter": r'''
def gradebook(records):
    """Return [(name, average, count)] sorted by average desc, then name asc."""
    groups = {}
    # TODO: group valid scores, compute averages, sort
    return []
''',
"hints": [
    "Skip a record unless `0 <= score <= 100`.",
    "`groups.setdefault(name, []).append(score)` groups scores.",
    "Sort with `key=lambda r: (-r[1], r[0])` after computing (name, avg, count).",
],
"solution": r'''
def gradebook(records):
    groups = {}
    for name, score in records:
        if 0 <= score <= 100:
            groups.setdefault(name, []).append(score)
    rows = []
    for name, scores in groups.items():
        avg = sum(scores) / len(scores)
        rows.append((name, round(avg, 2), len(scores)))
    rows.sort(key=lambda r: (-r[1], r[0]))
    return rows
''',
"explanation": r'''
Invalid scores are filtered while grouping, so names that only have invalid scores never appear.
Averages are computed from raw scores and rounded once. The tuple sort key `(-average, name)`
gives descending averages with ascending-name tie-breaks in a single stable sort.
''',
"tests": r'''
class TestGradebook(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.gradebook([("ann", 90), ("bob", 70), ("ann", 80), ("cy", 85)]),
                         [("ann", 85.0, 2), ("cy", 85.0, 1), ("bob", 70.0, 1)])

    def test_out_of_range(self):
        self.assertEqual(S.gradebook([("x", 101), ("x", 50)]), [("x", 50.0, 1)])

    def test_only_invalid(self):
        self.assertEqual(S.gradebook([("z", -5)]), [])

    def test_empty(self):
        self.assertEqual(S.gradebook([]), [])

    def test_rounding(self):
        self.assertEqual(S.gradebook([("a", 1), ("a", 2), ("a", 2)]), [("a", 1.67, 3)])

    def test_boundaries_included(self):
        self.assertEqual(S.gradebook([("a", 0), ("b", 100)]), [("b", 100.0, 1), ("a", 0.0, 1)])

    def test_tie_alphabetical(self):
        names = [r[0] for r in S.gradebook([("d", 60), ("b", 60), ("c", 60)])]
        self.assertEqual(names, ["b", "c", "d"])
''',
"feedback": [
    ("test_example", "Ties on average must be ordered by name ascending; reverse=True breaks this."),
    ("test_rounding", "Average raw scores, then round once with round(x, 2)."),
    ("test_boundaries_included", "0 and 100 are valid scores (inclusive range)."),
    ("test_only_invalid", "A name with no valid scores should not appear."),
],
},
# ---------------------------------------------------------------- matrix-transpose
{
"slug": "matrix-transpose", "title": "Matrix Transpose with Validation",
"difficulty": "intermediate", "prereqs": ["factorial-validated"], "packages": [],
"objectives": ["Use nested list comprehensions", "Validate rectangular shape",
               "Reason about rows and columns by index"],
"tags": ["nested-lists", "list-comprehension", "zip", "validation"],
"sources": ["S001", "S009"], "entry": "transpose(matrix)",
"article": r'''
# Nested Lists and the Transpose

## Intuition
A matrix stored as a list of rows is like a spreadsheet. The **transpose** flips it over its
diagonal: rows become columns. Row 0 of the result is column 0 of the original.

## Precise explanation
For an $m \times n$ matrix $A$, the transpose $A^\top$ is $n \times m$ with
$(A^\top)_{ji} = A_{ij}$.

As a nested comprehension (outer loop over output rows = input columns):
```python
[[matrix[i][j] for i in range(m)] for j in range(n)]
```
Equivalently with `zip`: `[list(col) for col in zip(*matrix)]`. `zip(*matrix)` unpacks the rows
as separate arguments and groups the i-th elements together. **Warning:** `zip` silently stops
at the shortest row, so it hides ragged input — validate first.

A matrix is **rectangular** when every row has the same length. A "ragged" list of lists is not a
matrix.

Edge cases: an empty matrix `[]` transposes to `[]`. A matrix of empty rows `[[], []]` has
shape 2×0; its transpose is 0×2, which as a list of rows is `[]`.

## Worked example
```
[[1, 2, 3],        [[1, 4],
 [4, 5, 6]]   →     [2, 5],
                    [3, 6]]
```
Shape (2, 3) → (3, 2).

## Common mistakes
* Swapping loop order in the comprehension, which returns a copy instead of the transpose.
* `[[0]*m]*n` to pre-allocate — every row is the **same** list object; writing one cell changes
  all rows.
* Mutating the input in place.

## Why this matters
Transposes are everywhere in ML: $X^\top X$ in least squares ([[least-squares-line]]), switching between
"samples × features" and "features × samples", attention's $QK^\top$ ([[scaled-dot-attention]]). Shape validation
is the habit that prevents silent broadcasting bugs in NumPy.
''',
"statement": r'''
Write `transpose(matrix)` for a list of lists of numbers.

**Requirements**
* Return a new list of lists equal to the transpose. Do not modify the input.
* If rows have different lengths, raise `ValueError("ragged matrix")`.
* `[]` and any matrix whose rows are all empty return `[]`.
* Do not use NumPy.

**Constraints:** up to 500×500.

**Examples**
```python
transpose([[1, 2, 3], [4, 5, 6]])   # [[1, 4], [2, 5], [3, 6]]
transpose([[7]])                    # [[7]]
transpose([[1, 2], [3]])            # raises ValueError — ragged
```
''',
"starter": r'''
def transpose(matrix):
    """Return the transpose of a rectangular list-of-lists matrix."""
    # TODO: validate row lengths, then build the transpose
    return []
''',
"hints": [
    "Let `n = len(matrix[0])`; every row must satisfy `len(row) == n`.",
    "Output row `j` is `[row[j] for row in matrix]`.",
    "`[[row[j] for row in matrix] for j in range(n)]` builds the whole result.",
],
"solution": r'''
def transpose(matrix):
    if not matrix:
        return []
    n = len(matrix[0])
    for row in matrix:
        if len(row) != n:
            raise ValueError("ragged matrix")
    return [[row[j] for row in matrix] for j in range(n)]
''',
"explanation": r'''
Validation runs first so the comprehension can assume a rectangle. The outer comprehension loops
over column indices of the input (rows of the output), the inner one collects that column from
every row. When rows are empty, `n == 0` and the result is `[]`, which correctly represents a
0-row matrix. New lists are built, so the input is untouched.
''',
"tests": r'''
class TestTranspose(unittest.TestCase):
    def test_2x3(self):
        self.assertEqual(S.transpose([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])

    def test_1x1(self):
        self.assertEqual(S.transpose([[7]]), [[7]])

    def test_ragged(self):
        with self.assertRaises(ValueError):
            S.transpose([[1, 2], [3]])

    def test_empty(self):
        self.assertEqual(S.transpose([]), [])

    def test_empty_rows(self):
        self.assertEqual(S.transpose([[], []]), [])

    def test_column_vector(self):
        self.assertEqual(S.transpose([[1], [2], [3]]), [[1, 2, 3]])

    def test_involution_and_no_mutation(self):
        m = [[1, 2], [3, 4], [5, 6]]
        copy = [r[:] for r in m]
        self.assertEqual(S.transpose(S.transpose(m)), copy)
        self.assertEqual(m, copy)

    def test_independent_rows(self):
        t = S.transpose([[1, 2], [3, 4]])
        t[0][0] = 99
        self.assertEqual(t[1][0], 2)
''',
"feedback": [
    ("test_ragged", "Check every row length before transposing; zip() hides ragged rows."),
    ("test_2x3", "The outer loop must run over columns (j), the inner over rows."),
    ("test_independent_rows", "Don't create rows with `[[0]*m]*n`; each row must be a separate list."),
    ("test_empty_rows", "Rows of length 0 give n = 0, so the result is []."),
],
},
]
