"""Problem definitions for the numpy topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- array-info
{
"slug": "array-info", "title": "Create an Array and Inspect It",
"difficulty": "beginner", "prereqs": ["matrix-transpose"], "packages": ["numpy"],
"objectives": ["Create ndarrays from nested lists with a chosen dtype", "Read shape, ndim, size and dtype",
               "Explain why ragged lists cannot become numeric arrays"],
"tags": ["ndarray", "dtype", "shape"],
"sources": ["S007", "S006"], "entry": "to_array(rows, dtype=float); describe(a)",
"article": r'''
# The ndarray

## Intuition
A NumPy array is a rectangular grid of numbers that all share one type. Because every element
has the same size and the grid is regular, NumPy can store the data in one contiguous block and
run fast compiled loops over it.

## Precise explanation
* `np.array(rows, dtype=float)` builds an array; `dtype` fixes the element type
  (`float64`, `int64`, `bool`, …).
* `a.shape` — tuple of lengths per axis; `a.ndim` — number of axes (`len(a.shape)`);
  `a.size` — total elements (product of the shape); `a.dtype` — element type.
* A 1-D array has shape `(n,)` (note the comma); a 2-D array `(rows, cols)`.
* Ragged nested lists (rows of different lengths) cannot form a numeric grid. Since NumPy 1.24
  `np.array([[1, 2], [3]])` raises `ValueError` unless you explicitly ask for `dtype=object`.

```python
>>> a = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)
>>> a.shape, a.ndim, a.size, a.dtype
((2, 3), 2, 6, dtype('float64'))
```

## Worked example
`np.array([7, 8, 9])` → shape `(3,)`, ndim 1, size 3, dtype int64 (on most 64-bit platforms).
`np.array([[7], [8], [9]])` → shape `(3, 1)` — a column, ndim 2.

## Common mistakes
* Confusing `(3,)` and `(3, 1)` — they broadcast differently ([[broadcast-center]]).
* Expecting `len(a)` to be the total size (it is the length of the first axis).
* Mixing ints and strings in one list → NumPy picks a string dtype.

## Why this matters
Every ML dataset is an array of shape `(n_samples, n_features)`; knowing its shape and dtype is
the first debugging step for almost every error message in later topics.
''',
"statement": r'''
Implement:
* `to_array(rows, dtype=float)` → `np.ndarray` built from nested lists with the given dtype.
  Raise `ValueError` if `rows` is ragged (rows of different lengths).
* `describe(a)` → dict `{"shape": tuple, "ndim": int, "size": int, "dtype": str}` where
  `dtype` is `str(a.dtype)`.

**Examples**
```python
a = to_array([[1, 2, 3], [4, 5, 6]])
describe(a)   # {'shape': (2, 3), 'ndim': 2, 'size': 6, 'dtype': 'float64'}
describe(to_array([1, 2], dtype=int))['shape']   # (2,)
to_array([[1, 2], [3]])   # raises ValueError
```
''',
"starter": r'''
import numpy as np


def to_array(rows, dtype=float):
    # TODO
    pass


def describe(a):
    # TODO
    return {}
''',
"hints": [
    "`np.array(rows, dtype=dtype)` raises ValueError for ragged numeric lists in NumPy ≥ 1.24.",
    "You may also check row lengths yourself for clarity.",
    "Use `tuple(a.shape)`, `int(a.ndim)`, `int(a.size)`, `str(a.dtype)`.",
],
"solution": r'''
import numpy as np


def to_array(rows, dtype=float):
    if isinstance(rows, (list, tuple)) and rows and isinstance(rows[0], (list, tuple)):
        n = len(rows[0])
        if any(len(r) != n for r in rows):
            raise ValueError("ragged rows")
    return np.array(rows, dtype=dtype)


def describe(a):
    return {"shape": tuple(a.shape), "ndim": int(a.ndim), "size": int(a.size),
            "dtype": str(a.dtype)}
''',
"explanation": r'''
An explicit row-length check gives a clear error message (NumPy would also raise). `describe`
converts NumPy's attributes into plain Python types so they compare cleanly in tests.
''',
"tests": r'''
import numpy as np

class TestArrayInfo(unittest.TestCase):
    def test_2d(self):
        self.assertEqual(S.describe(S.to_array([[1, 2, 3], [4, 5, 6]])),
                         {"shape": (2, 3), "ndim": 2, "size": 6, "dtype": "float64"})

    def test_1d_int(self):
        d = S.describe(S.to_array([1, 2], dtype=int))
        self.assertEqual(d["shape"], (2,))
        self.assertTrue(d["dtype"].startswith("int"))

    def test_column(self):
        self.assertEqual(S.describe(S.to_array([[7], [8], [9]]))["shape"], (3, 1))

    def test_ragged(self):
        with self.assertRaises(ValueError):
            S.to_array([[1, 2], [3]])

    def test_returns_ndarray(self):
        a = S.to_array([[1.5, 2.5]])
        self.assertIsInstance(a, np.ndarray)
        np.testing.assert_array_equal(a, np.array([[1.5, 2.5]]))

    def test_bool_dtype(self):
        self.assertEqual(S.describe(S.to_array([1, 0, 1], dtype=bool))["dtype"], "bool")

    def test_3d(self):
        d = S.describe(S.to_array([[[1, 2]], [[3, 4]], [[5, 6]]]))
        self.assertEqual((d["shape"], d["ndim"], d["size"]), ((3, 1, 2), 3, 6))
''',
"feedback": [
    ("test_2d", "Pass dtype to np.array and return shape as a tuple."),
    ("test_ragged", "Raise ValueError for rows of different lengths."),
    ("test_bool_dtype", "Return str(a.dtype), e.g. 'bool' or 'float64'."),
    ("test_3d", "size is the product of the shape entries."),
],
},
# ---------------------------------------------------------------- slicing-subgrid
{
"slug": "slicing-subgrid", "title": "Slicing a Sub-grid",
"difficulty": "beginner", "prereqs": ["array-info"], "packages": ["numpy"],
"objectives": ["Slice 2-D arrays with start:stop:step", "Distinguish views from copies",
               "Validate slice bounds"],
"tags": ["slicing", "views", "copies", "indexing"],
"sources": ["S007", "S006"], "entry": "crop(a, top, left, h, w); every_other(a); border_sum(a)",
"article": r'''
# Slicing, Views and Copies

## Intuition
Slicing cuts a rectangle out of a grid. In NumPy that rectangle is usually a **view**: a window
onto the same memory. Changing the view changes the original — powerful, but surprising.

## Precise explanation
* `a[r0:r1, c0:c1]` selects rows `r0..r1-1` and columns `c0..c1-1`.
* Steps: `a[::2, ::2]` takes every other row and column.
* Basic slicing returns a **view** (`np.shares_memory(view, a)` is True). Use `.copy()` to get
  independent data.
* Out-of-range slice ends are silently clipped (`a[0:100]` on 5 rows gives 5 rows) — validate if
  you need exact sizes.
* Negative indices count from the end: `a[-1]` is the last row; `a[1:-1, 1:-1]` is the interior.

## Worked example
```python
a = np.arange(16).reshape(4, 4)
a[1:3, 1:3]     # [[ 5,  6], [ 9, 10]]
a[::2, ::2]     # [[ 0,  2], [ 8, 10]]
a.sum() - a[1:-1, 1:-1].sum()   # border sum = 120 - 30 = 90
```

## Common mistakes
* `a[1:3][1:3]` — slices rows twice instead of rows then columns.
* Modifying a crop and accidentally editing the source image.
* Off-by-one: stop indices are exclusive.

## Why this matters
Cropping image patches (CV), selecting time windows and mini-batches are all slicing; view
semantics explain many "my data changed by itself" bugs.
''',
"statement": r'''
Implement for a 2-D array `a`:
* `crop(a, top, left, h, w)` → a **copy** of the `h × w` block starting at `(top, left)`;
  raise `ValueError` if the block does not fit inside `a` or `h`, `w` < 1 or top/left < 0.
* `every_other(a)` → `a[::2, ::2]` (a view is fine).
* `border_sum(a)` → sum of the elements on the outer border (for 1 or 2 rows/cols every element
  is on the border).

**Examples**
```python
a = np.arange(16).reshape(4, 4)
crop(a, 1, 1, 2, 2)   # array([[ 5,  6], [ 9, 10]])
every_other(a)        # array([[ 0,  2], [ 8, 10]])
border_sum(a)         # 90
```
''',
"starter": r'''
import numpy as np


def crop(a, top, left, h, w):
    # TODO
    pass


def every_other(a):
    # TODO
    pass


def border_sum(a):
    # TODO
    pass
''',
"hints": [
    "Check `top + h <= a.shape[0]` and `left + w <= a.shape[1]`.",
    "`a[top:top+h, left:left+w].copy()`.",
    "Border = total − interior `a[1:-1, 1:-1].sum()` (the interior is empty for small arrays).",
],
"solution": r'''
import numpy as np


def crop(a, top, left, h, w):
    if h < 1 or w < 1 or top < 0 or left < 0:
        raise ValueError("invalid crop parameters")
    if top + h > a.shape[0] or left + w > a.shape[1]:
        raise ValueError("crop does not fit")
    return a[top:top + h, left:left + w].copy()


def every_other(a):
    return a[::2, ::2]


def border_sum(a):
    return a.sum() - a[1:-1, 1:-1].sum()
''',
"explanation": r'''
`crop` validates bounds (slicing would silently clip) and returns a copy so callers can modify it
safely. `every_other` uses steps. `border_sum` subtracts the interior from the total; for arrays
with fewer than three rows or columns the interior slice is empty and sums to 0.
''',
"tests": r'''
import numpy as np

A = np.arange(16).reshape(4, 4)

class TestSlicing(unittest.TestCase):
    def test_crop(self):
        np.testing.assert_array_equal(S.crop(A, 1, 1, 2, 2), [[5, 6], [9, 10]])

    def test_crop_is_copy(self):
        a = A.copy()
        c = S.crop(a, 0, 0, 2, 2)
        c[0, 0] = 99
        self.assertEqual(a[0, 0], 0)

    def test_crop_out_of_bounds(self):
        with self.assertRaises(ValueError):
            S.crop(A, 3, 3, 2, 2)
        with self.assertRaises(ValueError):
            S.crop(A, -1, 0, 1, 1)

    def test_every_other(self):
        np.testing.assert_array_equal(S.every_other(A), [[0, 2], [8, 10]])

    def test_border(self):
        self.assertEqual(S.border_sum(A), 90)

    def test_border_small(self):
        self.assertEqual(S.border_sum(np.array([[1, 2], [3, 4]])), 10)
        self.assertEqual(S.border_sum(np.array([[5]])), 5)

    def test_full_crop(self):
        np.testing.assert_array_equal(S.crop(A, 0, 0, 4, 4), A)
''',
"feedback": [
    ("test_crop_is_copy", "Return `.copy()` of the slice so modifying the crop doesn't modify the input."),
    ("test_crop_out_of_bounds", "Slicing silently clips; check the bounds yourself."),
    ("test_border_small", "For 1×1 or 2×2 arrays the interior is empty, so the border is everything."),
    ("test_crop", "Use a[top:top+h, left:left+w] (one bracket, comma between axes)."),
],
},
# ---------------------------------------------------------------- boolean-mask
{
"slug": "boolean-mask", "title": "Boolean Masks",
"difficulty": "beginner", "prereqs": ["slicing-subgrid"], "packages": ["numpy"],
"objectives": ["Build boolean masks with comparisons", "Combine masks with & | ~",
               "Replace values with np.where without loops"],
"tags": ["boolean-indexing", "masks", "np.where", "vectorisation"],
"sources": ["S007"], "entry": "in_range(a, lo, hi); count_above(a, t); cap(a, t)",
"article": r'''
# Boolean Masks

## Intuition
A mask is a same-shaped array of True/False that marks which elements you care about. Indexing
with a mask keeps the True positions — the vectorised version of the filtering loop from [[filter-evens]].

## Precise explanation
* `a > 3` returns a boolean array. `a[a > 3]` returns a **1-D copy** of the selected values.
* Combine masks element-wise with `&` (and), `|` (or), `~` (not). Parentheses are required:
  `(a >= lo) & (a <= hi)` — `&` binds tighter than `>=`.
* Python's `and`/`or` do **not** work on arrays (they raise "truth value is ambiguous").
* `mask.sum()` counts True values (True = 1).
* `np.where(cond, x, y)` builds a new array taking `x` where cond is True and `y` elsewhere.
  `np.minimum(a, t)` is an alternative for capping.

## Worked example
```python
a = np.array([4, -1, 9, 3, 12])
a[(a >= 0) & (a <= 9)]   # [4, 9, 3]
(a > 5).sum()            # 2
np.where(a > 5, 5, a)    # [4, -1, 5, 3, 5]
```

## Common mistakes
* `a > 0 and a < 9` → `ValueError`.
* Missing parentheses: `a >= 0 & a <= 9` evaluates `0 & a` first.
* Modifying `a[a > 5]` expecting a view: `b = a[a > 5]; b[:] = 0` does not change `a`
  (but `a[a > 5] = 0` does, because it is an assignment through the mask).

## Why this matters
Masks select rows in pandas, threshold images ([[threshold-binary]]), build causal attention masks ([[causal-mask]]) and
apply ReLU (`np.where(z > 0, z, 0)`).
''',
"statement": r'''
Implement without Python loops:
* `in_range(a, lo, hi)` → 1-D array of the elements with `lo <= x <= hi` (in original order,
  row-major for 2-D).
* `count_above(a, t)` → number (Python `int`) of elements strictly greater than `t`.
* `cap(a, t)` → new array equal to `a` but with every element `> t` replaced by `t`; `a` must not
  change.

**Examples**
```python
a = np.array([4, -1, 9, 3, 12])
in_range(a, 0, 9)   # array([4, 9, 3])
count_above(a, 5)   # 2
cap(a, 5)           # array([ 4, -1,  5,  3,  5])
```
''',
"starter": r'''
import numpy as np


def in_range(a, lo, hi):
    # TODO
    pass


def count_above(a, t):
    # TODO
    pass


def cap(a, t):
    # TODO
    pass
''',
"hints": [
    "`mask = (a >= lo) & (a <= hi)` then `a[mask]`.",
    "`int((a > t).sum())`.",
    "`np.where(a > t, t, a)` returns a new array.",
],
"solution": r'''
import numpy as np


def in_range(a, lo, hi):
    a = np.asarray(a)
    return a[(a >= lo) & (a <= hi)]


def count_above(a, t):
    return int((np.asarray(a) > t).sum())


def cap(a, t):
    a = np.asarray(a)
    return np.where(a > t, t, a)
''',
"explanation": r'''
Comparisons produce masks; `&` combines them element-wise and boolean indexing extracts the
selected elements. Summing a mask counts Trues. `np.where` constructs a fresh array, leaving the
input untouched.
''',
"tests": r'''
import numpy as np

A = np.array([4, -1, 9, 3, 12])

class TestMasks(unittest.TestCase):
    def test_in_range(self):
        np.testing.assert_array_equal(S.in_range(A, 0, 9), [4, 9, 3])

    def test_in_range_2d(self):
        np.testing.assert_array_equal(S.in_range(np.array([[1, 5], [7, 2]]), 2, 6), [5, 2])

    def test_in_range_empty(self):
        self.assertEqual(S.in_range(A, 100, 200).size, 0)

    def test_count(self):
        self.assertEqual(S.count_above(A, 5), 2)
        self.assertIsInstance(S.count_above(A, 5), int)

    def test_count_strict(self):
        self.assertEqual(S.count_above(np.array([5, 5, 6]), 5), 1)

    def test_cap(self):
        np.testing.assert_array_equal(S.cap(A, 5), [4, -1, 5, 3, 5])

    def test_cap_no_mutation(self):
        a = A.copy()
        S.cap(a, 0)
        np.testing.assert_array_equal(a, A)

    def test_float(self):
        np.testing.assert_allclose(S.cap(np.array([0.5, 2.5]), 1.0), [0.5, 1.0])
''',
"feedback": [
    ("test_in_range", "Use & with parentheses: (a >= lo) & (a <= hi)."),
    ("test_count_strict", "Strictly greater: a > t."),
    ("test_cap_no_mutation", "Don't assign into a; use np.where or np.minimum to build a new array."),
    ("test_count", "Convert the result to a Python int."),
],
},
# ---------------------------------------------------------------- axis-aggregations
{
"slug": "axis-aggregations", "title": "Aggregations Along Axes",
"difficulty": "beginner", "prereqs": ["vectorized-math"], "packages": ["numpy"],
"objectives": ["Aggregate along axis 0 and axis 1", "Use argmax and unravel_index",
               "Keep dimensions with keepdims"],
"tags": ["aggregation", "axis", "argmax", "keepdims"],
"sources": ["S007", "S006"], "entry": "summarize(X)",
"article": r'''
# Aggregating Along Axes

## Intuition
For a table of shape `(students, subjects)`, "average per subject" collapses the student axis;
"total per student" collapses the subject axis. The `axis` argument says **which axis
disappears**.

## Precise explanation
* `X.mean(axis=0)` → one value per column (rows collapsed), shape `(n_cols,)`.
* `X.sum(axis=1)` → one value per row, shape `(n_rows,)`.
* `keepdims=True` keeps the collapsed axis with length 1: `X.mean(axis=1, keepdims=True)` has
  shape `(n_rows, 1)` and broadcasts back against `X` ([[broadcast-center]]).
* `X.argmax(axis=1)` → index of the max in each row (first occurrence on ties).
* `X.argmax()` with no axis indexes the *flattened* array; `np.unravel_index(i, X.shape)` turns
  it back into `(row, col)`.

## Worked example
```python
X = np.array([[1, 5, 2],
              [7, 0, 3]])
X.mean(axis=0)     # [4. , 2.5, 2.5]
X.sum(axis=1)      # [ 8, 10]
X.argmax(axis=1)   # [1, 0]
np.unravel_index(X.argmax(), X.shape)   # (1, 0)
```

## Common mistakes
* Mixing up axis 0 and 1 (remember: the named axis is the one removed).
* Using flat `argmax()` and treating it as a row index.
* Forgetting `keepdims` and then failing to broadcast.

## Why this matters
Per-feature means for scaling ([[standard-scaler]]), per-sample predicted classes (`argmax(axis=1)`), batch
statistics in batch norm ([[batchnorm-forward]]) — all are axis reductions.
''',
"statement": r'''
Write `summarize(X)` for a non-empty 2-D array, returning a dict:
* `"col_means"`: mean of each column (shape `(n_cols,)`),
* `"row_sums"`: sum of each row,
* `"row_argmax"`: index of the max in each row,
* `"max_pos"`: `(row, col)` tuple of Python ints of the overall maximum (first occurrence),
* `"row_means_keep"`: row means with shape `(n_rows, 1)`.

Raise `ValueError` if `X` is not 2-D or is empty. No Python loops.

**Example**
```python
s = summarize(np.array([[1, 5, 2], [7, 0, 3]]))
s["col_means"]   # array([4. , 2.5, 2.5])
s["max_pos"]     # (1, 0)
s["row_means_keep"].shape   # (2, 1)
```
''',
"starter": r'''
import numpy as np


def summarize(X):
    # TODO
    return {}
''',
"hints": [
    "Validate `X.ndim == 2 and X.size > 0`.",
    "Reductions: `X.mean(axis=0)`, `X.sum(axis=1)`, `X.argmax(axis=1)`.",
    "`r, c = np.unravel_index(X.argmax(), X.shape)` then `(int(r), int(c))`.",
],
"solution": r'''
import numpy as np


def summarize(X):
    X = np.asarray(X)
    if X.ndim != 2 or X.size == 0:
        raise ValueError("X must be a non-empty 2-D array")
    r, c = np.unravel_index(X.argmax(), X.shape)
    return {
        "col_means": X.mean(axis=0),
        "row_sums": X.sum(axis=1),
        "row_argmax": X.argmax(axis=1),
        "max_pos": (int(r), int(c)),
        "row_means_keep": X.mean(axis=1, keepdims=True),
    }
''',
"explanation": r'''
Each entry is one reduction along the appropriate axis. The global maximum's flat index is
converted to a 2-D position with `unravel_index`, and `keepdims=True` preserves a column shape
for later broadcasting.
''',
"tests": r'''
import numpy as np

X = np.array([[1, 5, 2], [7, 0, 3]])

class TestAxis(unittest.TestCase):
    def test_col_means(self):
        np.testing.assert_allclose(S.summarize(X)["col_means"], [4.0, 2.5, 2.5])

    def test_row_sums(self):
        np.testing.assert_array_equal(S.summarize(X)["row_sums"], [8, 10])

    def test_row_argmax(self):
        np.testing.assert_array_equal(S.summarize(X)["row_argmax"], [1, 0])

    def test_max_pos(self):
        self.assertEqual(S.summarize(X)["max_pos"], (1, 0))

    def test_keepdims(self):
        k = S.summarize(X)["row_means_keep"]
        self.assertEqual(k.shape, (2, 1))
        np.testing.assert_allclose(k[:, 0], [8 / 3, 10 / 3])

    def test_tie_first(self):
        self.assertEqual(S.summarize(np.array([[2, 9], [9, 1]]))["max_pos"], (0, 1))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            S.summarize(np.array([1, 2, 3]))
''',
"feedback": [
    ("test_col_means", "Column means collapse axis 0."),
    ("test_max_pos", "Use np.unravel_index on the flat argmax."),
    ("test_keepdims", "Pass keepdims=True so the shape is (n_rows, 1)."),
    ("test_bad_input", "Reject arrays with ndim != 2."),
],
},
# ---------------------------------------------------------------- broadcast-center
{
"slug": "broadcast-center", "title": "Centering Columns with Broadcasting",
"difficulty": "intermediate", "prereqs": ["axis-aggregations", "z-scores"], "packages": ["numpy"],
"objectives": ["Apply NumPy's broadcasting rules", "Centre and scale features without loops",
               "Use np.newaxis / reshape to align shapes"],
"tags": ["broadcasting", "standardization", "shapes"],
"sources": ["S007", "S006"], "entry": "center_columns(X); scale_rows(X, w); standardize(X)",
"article": r'''
# Broadcasting

## Intuition
Subtracting a per-column mean from every row should not need a loop: NumPy "stretches" the
smaller array across the larger one. That stretching is **broadcasting**, done without copying
memory.

## Precise explanation
Compare shapes from the **right**. Two dimensions are compatible if they are equal or one of
them is 1 (a missing leading dimension counts as 1). The result takes the larger size.
| X shape | other | result |
|---|---|---|
| (4, 3) | (3,) | (4, 3) — row vector stretched down |
| (4, 3) | (4, 1) | (4, 3) — column stretched across |
| (4, 3) | (4,) | **error** (3 vs 4) |

To scale row *i* by `w[i]` with `w.shape == (4,)`, reshape it to a column: `w[:, np.newaxis]`
(or `w[:, None]`, `w.reshape(-1, 1)`).

## Worked example
```python
X = np.array([[1., 2.], [3., 6.]])
X - X.mean(axis=0)            # [[-1, -2], [1, 2]]
X * np.array([10, 0.5])[:, None]   # [[10, 20], [1.5, 3]]
```

## Common mistakes
* Multiplying `(4, 3)` by `(4,)` and getting a shape error — reshape to `(4, 1)`.
* Accidental broadcasting: `(n,)` minus `(n, 1)` produces an `(n, n)` matrix silently!
* Dividing by a zero standard deviation for a constant column.

## Why this matters
Standardization ([[standard-scaler]]), adding bias vectors in neural layers ([[dense-forward]]), and pairwise distances
([[pairwise-distances]]) are all broadcasting.
''',
"statement": r'''
For a 2-D float array `X` of shape `(n, d)`, implement without loops:
* `center_columns(X)` → `X` minus its column means.
* `scale_rows(X, w)` → row `i` multiplied by `w[i]`; raise `ValueError` if `len(w) != n`.
* `standardize(X)` → `(X - mean) / std` per column (population std); columns with std 0 become
  all zeros (no division by zero, no NaN).

**Examples**
```python
X = np.array([[1., 2.], [3., 6.]])
center_columns(X)              # [[-1., -2.], [ 1.,  2.]]
scale_rows(X, [10, 0.5])       # [[10., 20.], [ 1.5, 3.]]
standardize(np.array([[1., 5.], [3., 5.]]))   # [[-1., 0.], [1., 0.]]
```
''',
"starter": r'''
import numpy as np


def center_columns(X):
    # TODO
    pass


def scale_rows(X, w):
    # TODO
    pass


def standardize(X):
    # TODO
    pass
''',
"hints": [
    "`X - X.mean(axis=0)` broadcasts a (d,) vector over rows.",
    "`np.asarray(w)[:, None]` turns w into an (n, 1) column.",
    "Replace zero stds with 1 before dividing: `std = np.where(std == 0, 1.0, std)` — the centred column is already 0.",
],
"solution": r'''
import numpy as np


def center_columns(X):
    X = np.asarray(X, dtype=float)
    return X - X.mean(axis=0)


def scale_rows(X, w):
    X = np.asarray(X, dtype=float)
    w = np.asarray(w, dtype=float)
    if w.shape != (X.shape[0],):
        raise ValueError("w must have one weight per row")
    return X * w[:, None]


def standardize(X):
    Xc = center_columns(X)
    std = Xc.std(axis=0)
    std = np.where(std == 0, 1.0, std)
    return Xc / std
''',
"explanation": r'''
Column statistics have shape (d,), which broadcasts across the n rows. Row weights need an
explicit column shape (n, 1). For constant columns the centred values are already zero, so
dividing by 1 instead of 0 yields zeros without NaN.
''',
"tests": r'''
import numpy as np

X = np.array([[1., 2.], [3., 6.]])

class TestBroadcast(unittest.TestCase):
    def test_center(self):
        np.testing.assert_allclose(S.center_columns(X), [[-1, -2], [1, 2]])

    def test_center_means_zero(self):
        Y = S.center_columns(np.array([[1., 9, 4], [2, 7, 1], [6, 2, 0], [3, 3, 3]]))
        np.testing.assert_allclose(Y.mean(axis=0), 0, atol=1e-12)

    def test_scale_rows(self):
        np.testing.assert_allclose(S.scale_rows(X, [10, 0.5]), [[10, 20], [1.5, 3]])

    def test_scale_rows_bad(self):
        with self.assertRaises(ValueError):
            S.scale_rows(X, [1, 2, 3])

    def test_standardize_constant(self):
        np.testing.assert_allclose(S.standardize(np.array([[1., 5.], [3., 5.]])), [[-1, 0], [1, 0]])

    def test_standardize_props(self):
        Z = S.standardize(np.array([[1., 10], [2, 30], [4, 20], [9, 0]]))
        np.testing.assert_allclose(Z.mean(axis=0), 0, atol=1e-12)
        np.testing.assert_allclose(Z.std(axis=0), 1, atol=1e-12)

    def test_no_nan(self):
        self.assertFalse(np.isnan(S.standardize(np.ones((3, 2)))).any())

    def test_shape_preserved(self):
        self.assertEqual(S.scale_rows(np.ones((5, 3)), np.arange(5)).shape, (5, 3))
''',
"feedback": [
    ("test_scale_rows", "Reshape w to (n, 1) with w[:, None] so it stretches across columns."),
    ("test_standardize_constant", "Avoid dividing by zero for constant columns; they should become 0."),
    ("test_standardize_props", "Use population std (np.std default ddof=0) per column."),
    ("test_scale_rows_bad", "Validate len(w) == number of rows."),
],
},
# ---------------------------------------------------------------- reshape-stack
{
"slug": "reshape-stack", "title": "Reshape and Stack",
"difficulty": "intermediate", "prereqs": ["slicing-subgrid"], "packages": ["numpy"],
"objectives": ["Reshape arrays with -1", "Stack and concatenate along axes",
               "Flatten image batches for linear models"],
"tags": ["reshape", "stack", "concatenate", "batching"],
"sources": ["S007"], "entry": "to_batches(x, batch_size); add_bias_column(X); flatten_images(imgs)",
"article": r'''
# Reshaping and Stacking

## Intuition
Reshaping reinterprets the same numbers in a different grid (12 numbers as 3×4 or 2×6), like
re-folding a strip of paper. Stacking glues arrays together along an axis.

## Precise explanation
* `a.reshape(r, c)` requires `r*c == a.size`; one dimension may be `-1` meaning "whatever fits".
  Reshape fills in **row-major (C) order** — the last axis varies fastest.
* `np.concatenate([a, b], axis=k)` joins along an existing axis; `np.stack` creates a new axis.
* `np.hstack` / `np.column_stack` join side by side; `np.vstack` on top of each other.
* A batch of images with shape `(N, H, W)` becomes a design matrix `(N, H*W)` with
  `imgs.reshape(N, -1)`.

## Worked example
```python
x = np.arange(10)
x[: (10 // 4) * 4].reshape(-1, 4)     # [[0,1,2,3],[4,5,6,7]] — remainder 8, 9 dropped
np.hstack([np.ones((2, 1)), [[3, 4], [5, 6]]])   # [[1,3,4],[1,5,6]]
```

## Common mistakes
* `reshape(4, -1)` vs `reshape(-1, 4)` — rows vs columns of size 4.
* Using reshape to transpose (it doesn't reorder data; use `.T`).
* Stacking 1-D arrays with `hstack` and getting one long vector instead of columns.

## Why this matters
Mini-batching, adding the intercept column in linear regression ([[least-squares-line]]), flattening images
before a dense layer (DL/CV) and splitting attention heads ([[multi-head-attention]]) are reshapes.
''',
"statement": r'''
Implement:
* `to_batches(x, batch_size)` → 1-D `x` reshaped to `(n // batch_size, batch_size)`, dropping the
  incomplete last batch. Raise `ValueError` if `batch_size < 1` or `> len(x)`.
* `add_bias_column(X)` → `X` (shape `(n, d)`) with a column of ones prepended → `(n, d+1)`.
* `flatten_images(imgs)` → `(N, H, W)` → `(N, H*W)`, row-major per image; raise `ValueError` if
  `imgs.ndim != 3`.

**Examples**
```python
to_batches(np.arange(10), 4)          # [[0, 1, 2, 3], [4, 5, 6, 7]]
add_bias_column(np.array([[3, 4], [5, 6]]))   # [[1., 3., 4.], [1., 5., 6.]]
flatten_images(np.arange(8).reshape(2, 2, 2)) # [[0, 1, 2, 3], [4, 5, 6, 7]]
```
''',
"starter": r'''
import numpy as np


def to_batches(x, batch_size):
    # TODO
    pass


def add_bias_column(X):
    # TODO
    pass


def flatten_images(imgs):
    # TODO
    pass
''',
"hints": [
    "`m = len(x) // batch_size; x[: m * batch_size].reshape(m, batch_size)`.",
    "`np.hstack([np.ones((n, 1)), X])`.",
    "`imgs.reshape(imgs.shape[0], -1)`.",
],
"solution": r'''
import numpy as np


def to_batches(x, batch_size):
    x = np.asarray(x)
    if batch_size < 1 or batch_size > len(x):
        raise ValueError("invalid batch_size")
    m = len(x) // batch_size
    return x[: m * batch_size].reshape(m, batch_size)


def add_bias_column(X):
    X = np.asarray(X, dtype=float)
    return np.hstack([np.ones((X.shape[0], 1)), X])


def flatten_images(imgs):
    imgs = np.asarray(imgs)
    if imgs.ndim != 3:
        raise ValueError("expected (N, H, W)")
    return imgs.reshape(imgs.shape[0], -1)
''',
"explanation": r'''
Truncating to a multiple of the batch size makes the reshape valid. The bias column is a
column of ones joined horizontally. Flattening keeps the batch axis and lets `-1` compute H·W.
''',
"tests": r'''
import numpy as np

class TestReshape(unittest.TestCase):
    def test_batches(self):
        np.testing.assert_array_equal(S.to_batches(np.arange(10), 4), [[0, 1, 2, 3], [4, 5, 6, 7]])

    def test_batches_exact(self):
        self.assertEqual(S.to_batches(np.arange(12), 3).shape, (4, 3))

    def test_batches_bad(self):
        with self.assertRaises(ValueError):
            S.to_batches(np.arange(3), 5)
        with self.assertRaises(ValueError):
            S.to_batches(np.arange(3), 0)

    def test_bias(self):
        np.testing.assert_allclose(S.add_bias_column(np.array([[3, 4], [5, 6]])), [[1, 3, 4], [1, 5, 6]])

    def test_bias_shape(self):
        self.assertEqual(S.add_bias_column(np.zeros((7, 3))).shape, (7, 4))

    def test_flatten(self):
        np.testing.assert_array_equal(S.flatten_images(np.arange(8).reshape(2, 2, 2)),
                                      [[0, 1, 2, 3], [4, 5, 6, 7]])

    def test_flatten_bad(self):
        with self.assertRaises(ValueError):
            S.flatten_images(np.zeros((4, 4)))
''',
"feedback": [
    ("test_batches", "Drop the remainder before reshaping to (-1, batch_size)."),
    ("test_bias", "The ones column comes first (prepended)."),
    ("test_flatten", "Keep axis 0 (the batch) and flatten the rest with reshape(N, -1)."),
    ("test_batches_bad", "Validate batch_size between 1 and len(x)."),
],
},
# ---------------------------------------------------------------- fancy-indexing
{
"slug": "fancy-indexing", "title": "Fancy Indexing and Gather",
"difficulty": "intermediate", "prereqs": ["boolean-mask", "axis-aggregations"], "packages": ["numpy"],
"objectives": ["Index with integer arrays", "Pick one element per row with paired index arrays",
               "Find top-k indices with argsort"],
"tags": ["fancy-indexing", "argsort", "gather", "top-k"],
"sources": ["S007"], "entry": "gather_rows(X, idx); pick_per_row(P, cols); top_k(v, k)",
"article": r'''
# Fancy (Integer-Array) Indexing

## Intuition
Sometimes you know exactly *which* positions you want — rows 3, 0 and 3 again, or "the
probability of the correct class in each row". Passing integer arrays as indices fetches exactly
those elements in that order.

## Precise explanation
* `X[[3, 0, 3]]` returns rows 3, 0, 3 (copies, repeats allowed).
* Paired index arrays select individual elements:
  `P[np.arange(n), cols]` returns `[P[0, cols[0]], P[1, cols[1]], …]`.
  This is **not** the same as `P[:, cols]`, which returns whole columns (an n × n block).
* `np.argsort(v)` returns indices that would sort `v` ascending. For top-k largest use
  `np.argsort(-v, kind="stable")[:k]`; the stable sort keeps the lower index first on ties.

## Worked example
```python
P = np.array([[0.1, 0.7, 0.2],
              [0.5, 0.3, 0.2]])
P[np.arange(2), [1, 0]]     # [0.7, 0.5]
np.argsort(-np.array([3, 9, 9, 1]), kind="stable")[:2]   # [1, 2]
```

## Common mistakes
* `P[:, cols]` instead of `P[np.arange(n), cols]`.
* Using `argsort(v)[::-1]` for top-k — reverses tie order too.
* Indices out of range raise `IndexError`.

## Why this matters
Cross-entropy picks the predicted probability of the true class per row ([[cross-entropy]]); k-NN and
retrieval pick top-k neighbours; embedding lookup in NLP/LLMs is `E[token_ids]`.
''',
"statement": r'''
Implement:
* `gather_rows(X, idx)` → rows of `X` at integer indices `idx` (order and repeats preserved).
* `pick_per_row(P, cols)` → 1-D array with `P[i, cols[i]]`; raise `ValueError` if
  `len(cols) != P.shape[0]`.
* `top_k(v, k)` → indices of the `k` largest values of 1-D `v`, largest first, ties broken by
  lower index; raise `ValueError` unless `1 <= k <= len(v)`.

**Examples**
```python
P = np.array([[0.1, 0.7, 0.2], [0.5, 0.3, 0.2]])
pick_per_row(P, [1, 0])           # array([0.7, 0.5])
top_k(np.array([3, 9, 9, 1]), 2)  # array([1, 2])
```
''',
"starter": r'''
import numpy as np


def gather_rows(X, idx):
    # TODO
    pass


def pick_per_row(P, cols):
    # TODO
    pass


def top_k(v, k):
    # TODO
    pass
''',
"hints": [
    "`X[np.asarray(idx)]`.",
    "`P[np.arange(P.shape[0]), cols]`.",
    "`np.argsort(-v, kind='stable')[:k]`.",
],
"solution": r'''
import numpy as np


def gather_rows(X, idx):
    return np.asarray(X)[np.asarray(idx, dtype=int)]


def pick_per_row(P, cols):
    P = np.asarray(P)
    cols = np.asarray(cols, dtype=int)
    if cols.shape != (P.shape[0],):
        raise ValueError("need one column index per row")
    return P[np.arange(P.shape[0]), cols]


def top_k(v, k):
    v = np.asarray(v)
    if not 1 <= k <= len(v):
        raise ValueError("k out of range")
    return np.argsort(-v, kind="stable")[:k]
''',
"explanation": r'''
Integer-array indexing gathers rows directly. Pairing `arange(n)` with the column indices picks
one element per row. Sorting the negated values with a stable algorithm yields descending order
with ties resolved by original position.
''',
"tests": r'''
import numpy as np

P = np.array([[0.1, 0.7, 0.2], [0.5, 0.3, 0.2]])

class TestFancy(unittest.TestCase):
    def test_gather(self):
        X = np.arange(12).reshape(4, 3)
        np.testing.assert_array_equal(S.gather_rows(X, [3, 0, 3]), [[9, 10, 11], [0, 1, 2], [9, 10, 11]])

    def test_pick(self):
        np.testing.assert_allclose(S.pick_per_row(P, [1, 0]), [0.7, 0.5])

    def test_pick_shape(self):
        self.assertEqual(S.pick_per_row(P, [2, 2]).shape, (2,))

    def test_pick_bad(self):
        with self.assertRaises(ValueError):
            S.pick_per_row(P, [0])

    def test_topk_ties(self):
        np.testing.assert_array_equal(S.top_k(np.array([3, 9, 9, 1]), 2), [1, 2])

    def test_topk_all(self):
        np.testing.assert_array_equal(S.top_k(np.array([0.2, 0.9, 0.5]), 3), [1, 2, 0])

    def test_topk_bad(self):
        with self.assertRaises(ValueError):
            S.top_k(np.array([1, 2]), 3)
''',
"feedback": [
    ("test_pick", "Use P[np.arange(n), cols], not P[:, cols]."),
    ("test_topk_ties", "argsort(-v, kind='stable') keeps lower indices first on ties; reversing argsort(v) does not."),
    ("test_gather", "Integer-array indexing keeps order and repeats."),
    ("test_pick_bad", "Validate one column index per row."),
],
},
# ---------------------------------------------------------------- seeded-generator
{
"slug": "seeded-generator", "title": "Seeded Random Generators",
"difficulty": "intermediate", "prereqs": ["fancy-indexing", "dice-lln"], "packages": ["numpy"],
"objectives": ["Use np.random.default_rng with a seed", "Generate synthetic regression data",
               "Create reproducible shuffled train/test indices"],
"tags": ["random", "reproducibility", "synthetic-data", "Generator"],
"sources": ["S007"], "entry": "make_regression(n, seed, noise=0.1); split_indices(n, test_frac, seed)",
"article": r'''
# Reproducible Randomness in NumPy

## Intuition
Experiments must be repeatable: the same seed should give the same "random" data, so a teammate
can reproduce your numbers. NumPy's modern API puts all randomness in a `Generator` object.

## Precise explanation
* `rng = np.random.default_rng(seed)` creates an independent generator (PCG64 by default).
* `rng.uniform(lo, hi, size=n)`, `rng.normal(mu, sigma, size=n)`, `rng.permutation(n)`,
  `rng.integers(lo, hi, size=n)`.
* Passing a generator around (rather than calling the legacy global `np.random.seed`) keeps
  different parts of a program from disturbing each other's streams.
* Same seed → same numbers *in the same NumPy version*. NumPy reserves the right to change some
  algorithms between versions, so never hard-code random outputs in tests; test properties.

Synthetic linear data: $x \sim U(0, 1)$, $y = 2x + 1 + \varepsilon$, $\varepsilon \sim N(0, \sigma^2)$.

## Worked example
```python
rng = np.random.default_rng(0)
idx = rng.permutation(10)       # some ordering of 0..9
test, train = idx[:3], idx[3:]  # 30 % test
```

## Common mistakes
* Calling `default_rng(seed)` inside a loop — every iteration restarts the same stream.
* Using the global `np.random.rand` in library code.
* Overlapping train and test indices.

## Why this matters
Seeded data generation, shuffling and weight initialisation make every later ML, DL and FL
exercise deterministic.
''',
"statement": r'''
Implement using `np.random.default_rng(seed)` (one generator per call):
* `make_regression(n, seed, noise=0.1)` → `(x, y)` with `x = rng.uniform(0, 1, n)` drawn first,
  then `eps = rng.normal(0, noise, n)`, and `y = 2 * x + 1 + eps`. Raise `ValueError` if `n < 1`
  or `noise < 0`.
* `split_indices(n, test_frac, seed)` → `(train_idx, test_idx)` from `rng.permutation(n)`; the
  first `round(n * test_frac)` permuted indices are the test set. Raise `ValueError` unless
  `0 < test_frac < 1`.

**Examples**
```python
x, y = make_regression(5, seed=0)
x.shape, y.shape                # ((5,), (5,))
tr, te = split_indices(10, 0.3, seed=1)
len(tr), len(te)                # (7, 3)
```
''',
"starter": r'''
import numpy as np


def make_regression(n, seed, noise=0.1):
    # TODO
    pass


def split_indices(n, test_frac, seed):
    # TODO
    pass
''',
"hints": [
    "`rng = np.random.default_rng(seed)` once at the top of each function.",
    "Draw x before the noise so the order of draws is as specified.",
    "`perm = rng.permutation(n); k = round(n * test_frac); return perm[k:], perm[:k]`.",
],
"solution": r'''
import numpy as np


def make_regression(n, seed, noise=0.1):
    if n < 1 or noise < 0:
        raise ValueError("invalid n or noise")
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, 1, n)
    eps = rng.normal(0, noise, n)
    return x, 2 * x + 1 + eps


def split_indices(n, test_frac, seed):
    if not 0 < test_frac < 1:
        raise ValueError("test_frac must be in (0, 1)")
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    k = round(n * test_frac)
    return perm[k:], perm[:k]
''',
"explanation": r'''
Each function owns one seeded generator, so results depend only on the arguments. Draw order is
fixed (x then noise). The permutation guarantees train and test indices are disjoint and cover
0..n−1.
''',
"tests": r'''
import numpy as np

class TestSeeded(unittest.TestCase):
    def test_shapes(self):
        x, y = S.make_regression(5, seed=0)
        self.assertEqual((x.shape, y.shape), ((5,), (5,)))

    def test_reproducible(self):
        a = S.make_regression(50, seed=7)
        b = S.make_regression(50, seed=7)
        np.testing.assert_array_equal(a[0], b[0])
        np.testing.assert_array_equal(a[1], b[1])

    def test_draw_order(self):
        x, y = S.make_regression(20, seed=3, noise=0.5)
        rng = np.random.default_rng(3)
        np.testing.assert_allclose(x, rng.uniform(0, 1, 20))
        np.testing.assert_allclose(y, 2 * x + 1 + rng.normal(0, 0.5, 20))

    def test_noise_free(self):
        x, y = S.make_regression(10, seed=1, noise=0.0)
        np.testing.assert_allclose(y, 2 * x + 1)

    def test_line_recovered(self):
        x, y = S.make_regression(5000, seed=2, noise=0.1)
        slope, intercept = np.polyfit(x, y, 1)
        self.assertAlmostEqual(slope, 2.0, delta=0.02)
        self.assertAlmostEqual(intercept, 1.0, delta=0.02)

    def test_split_disjoint_cover(self):
        tr, te = S.split_indices(10, 0.3, seed=1)
        self.assertEqual((len(tr), len(te)), (7, 3))
        self.assertEqual(sorted(np.concatenate([tr, te]).tolist()), list(range(10)))

    def test_split_reproducible_and_bad(self):
        np.testing.assert_array_equal(S.split_indices(20, 0.25, 4)[1], S.split_indices(20, 0.25, 4)[1])
        with self.assertRaises(ValueError):
            S.split_indices(10, 1.0, 0)
''',
"feedback": [
    ("test_draw_order", "Create one default_rng(seed); draw x = uniform first, then normal noise."),
    ("test_reproducible", "Don't use the global np.random functions."),
    ("test_split_disjoint_cover", "Use rng.permutation(n) and split it; the two parts must not overlap."),
    ("test_noise_free", "y = 2x + 1 + noise exactly."),
],
},
# ---------------------------------------------------------------- pairwise-distances
{
"slug": "pairwise-distances", "title": "Vectorized Pairwise Distances",
"difficulty": "advanced", "prereqs": ["broadcast-center", "matmul-dot"], "packages": ["numpy"],
"objectives": ["Compute all pairwise squared distances with broadcasting",
               "Use the expansion ‖a−b‖² = ‖a‖² + ‖b‖² − 2a·b", "Find nearest neighbours with argmin"],
"tags": ["distances", "broadcasting", "vectorisation", "nearest-neighbour"],
"sources": ["S007", "S006"], "entry": "pairwise_sq_dists(A, B); nearest(A, B)",
"article": r'''
# Pairwise Distances without Loops

## Intuition
k-NN, k-means and retrieval all need the distance from every query to every reference point. A
double Python loop over 1000 × 1000 points is a million slow iterations; one matrix expression
does it in milliseconds.

## Precise explanation
For rows $a_i$ of $A$ ($m\times d$) and $b_j$ of $B$ ($n\times d$):
$$D_{ij} = \lVert a_i - b_j\rVert^2 = \lVert a_i\rVert^2 + \lVert b_j\rVert^2 - 2\,a_i\cdot b_j.$$
In NumPy:
```python
aa = (A**2).sum(axis=1)[:, None]    # (m, 1)
bb = (B**2).sum(axis=1)[None, :]    # (1, n)
D = aa + bb - 2 * A @ B.T           # (m, n)
```
Rounding can make tiny entries slightly negative (e.g. −1e−15); clip with `np.maximum(D, 0)`.
An alternative, `((A[:, None, :] - B[None, :, :])**2).sum(-1)`, is simpler but builds an
`(m, n, d)` temporary that uses much more memory.

## Worked example
A = [[0, 0], [1, 1]], B = [[1, 0], [3, 4]]:
D = [[1, 25], [1, 13]]; nearest B-row for each A-row: [0, 0].

## Common mistakes
* Forgetting the transpose in `A @ B.T`.
* Taking `sqrt` of slightly negative values → NaN.
* Mixing up which axis to `argmin` over (axis=1 → nearest B for each A).

## Why this matters
This exact function is the engine of k-NN ([[knn-classifier]]), k-means ([[kmeans]]), embedding retrieval ([[cosine-retrieval]])
and non-max suppression ideas in CV.
''',
"statement": r'''
Implement (no Python loops over points):
* `pairwise_sq_dists(A, B)` → `(m, n)` array of squared Euclidean distances, clipped at 0.
  Raise `ValueError` if the feature dimensions differ or inputs are not 2-D.
* `nearest(A, B)` → for each row of `A`, the index of the closest row of `B` (lowest index on ties).

**Examples**
```python
A = np.array([[0., 0.], [1., 1.]]); B = np.array([[1., 0.], [3., 4.]])
pairwise_sq_dists(A, B)   # [[ 1., 25.], [ 1., 13.]]
nearest(A, B)             # array([0, 0])
```
''',
"starter": r'''
import numpy as np


def pairwise_sq_dists(A, B):
    # TODO
    pass


def nearest(A, B):
    # TODO
    pass
''',
"hints": [
    "Row norms: `(A ** 2).sum(axis=1)`, shaped `(m, 1)` and `(1, n)`.",
    "`D = aa + bb - 2 * A @ B.T`, then `np.maximum(D, 0)`.",
    "`D.argmin(axis=1)` returns the first index on ties.",
],
"solution": r'''
import numpy as np


def pairwise_sq_dists(A, B):
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    if A.ndim != 2 or B.ndim != 2 or A.shape[1] != B.shape[1]:
        raise ValueError("A and B must be 2-D with the same number of columns")
    aa = (A ** 2).sum(axis=1)[:, None]
    bb = (B ** 2).sum(axis=1)[None, :]
    return np.maximum(aa + bb - 2 * A @ B.T, 0.0)


def nearest(A, B):
    return pairwise_sq_dists(A, B).argmin(axis=1)
''',
"explanation": r'''
Expanding the squared distance turns the problem into two norm vectors and one matrix product,
combined by broadcasting into an m×n matrix. Clipping removes tiny negative rounding errors.
`argmin` along axis 1 picks the closest reference for each query.
''',
"tests": r'''
import numpy as np

class TestPairwise(unittest.TestCase):
    def test_example(self):
        A = np.array([[0., 0.], [1., 1.]]); B = np.array([[1., 0.], [3., 4.]])
        np.testing.assert_allclose(S.pairwise_sq_dists(A, B), [[1, 25], [1, 13]], atol=1e-12)

    def test_against_loops(self):
        rng = np.random.default_rng(0)
        A, B = rng.normal(size=(7, 3)), rng.normal(size=(5, 3))
        ref = np.array([[((a - b) ** 2).sum() for b in B] for a in A])
        np.testing.assert_allclose(S.pairwise_sq_dists(A, B), ref, rtol=1e-10, atol=1e-10)

    def test_self_zero_diag_nonneg(self):
        A = np.array([[1e8, 1.0], [1e8 + 1, 2.0]])
        D = S.pairwise_sq_dists(A, A)
        self.assertTrue((D >= 0).all())
        self.assertEqual(D.shape, (2, 2))

    def test_nearest(self):
        A = np.array([[0., 0.], [1., 1.]]); B = np.array([[1., 0.], [3., 4.]])
        np.testing.assert_array_equal(S.nearest(A, B), [0, 0])

    def test_nearest_tie(self):
        np.testing.assert_array_equal(S.nearest(np.array([[0., 0.]]), np.array([[1., 0.], [-1., 0.]])), [0])

    def test_dim_mismatch(self):
        with self.assertRaises(ValueError):
            S.pairwise_sq_dists(np.zeros((2, 3)), np.zeros((2, 2)))

    def test_shape(self):
        self.assertEqual(S.pairwise_sq_dists(np.zeros((4, 2)), np.zeros((9, 2))).shape, (4, 9))
''',
"feedback": [
    ("test_against_loops", "Check the sign of the −2·A@B.T term and the transpose."),
    ("test_self_zero_diag_nonneg", "Clip with np.maximum(D, 0) to remove rounding negatives."),
    ("test_nearest", "argmin along axis=1 gives the nearest B row for each A row."),
    ("test_dim_mismatch", "Feature dimensions (columns) must match."),
],
},
# ---------------------------------------------------------------- linalg-solve
{
"slug": "linalg-solve", "title": "Solve Linear Systems Safely",
"difficulty": "advanced", "prereqs": ["matmul-dot", "solve-2x2-cramer"], "packages": ["numpy"],
"objectives": ["Solve Ax=b with np.linalg.solve", "Detect ill-conditioned systems with np.linalg.cond",
               "Fit least squares with np.linalg.lstsq"],
"tags": ["linear-algebra", "conditioning", "least-squares"],
"sources": ["S007", "S009"], "entry": "solve(A, b, max_cond=1e12); residual_norm(A, x, b); fit_line(x, y)",
"article": r'''
# Solving Linear Systems in NumPy

## Intuition
[[solve-2x2-cramer]] solved 2×2 systems by hand. Real problems have hundreds of unknowns, and some systems are
*nearly* singular: tiny changes in the data cause huge changes in the answer. The **condition
number** measures that sensitivity.

## Precise explanation
* `np.linalg.solve(A, b)` solves square systems using an LU factorisation (more accurate and
  faster than `inv(A) @ b`). It raises `LinAlgError` for exactly singular matrices.
* `np.linalg.cond(A)` — ratio of largest to smallest singular value. Rule of thumb: you can lose
  about $\log_{10}(\text{cond})$ digits of accuracy; above ~1e12 in float64, answers are mostly
  noise.
* Residual $\lVert Ax - b\rVert_2$ (`np.linalg.norm(A @ x - b)`) checks a solution.
* Over-determined systems (more equations than unknowns) have no exact solution; least squares
  minimises the residual: `np.linalg.lstsq(X, y, rcond=None)`.

To fit $y \approx w_0 + w_1 x$, build $X = [\mathbf 1, x]$ and solve the least-squares problem.

## Worked example
A = [[3, 1], [1, 2]], b = [9, 8] → x = [2, 3]; residual 0.
Points (0, 1), (1, 3), (2, 5) → line intercept 1, slope 2.

## Common mistakes
* Using `np.linalg.inv` for solving.
* Ignoring warnings about near-singular matrices.
* Forgetting the column of ones (forcing the line through the origin).

## Why this matters
Least squares is linear regression ([[least-squares-line]]), ridge adds a stabilising term to fix
ill-conditioning ([[ridge-regression]]), and many ML solvers report condition problems as convergence warnings.
''',
"statement": r'''
Implement:
* `solve(A, b, max_cond=1e12)` → solution of square `A x = b`. Raise `ValueError` if `A` is not
  square, sizes mismatch, or `np.linalg.cond(A) > max_cond` (this also covers singular matrices,
  whose condition number is infinite or huge).
* `residual_norm(A, x, b)` → float `‖A x − b‖₂`.
* `fit_line(x, y)` → `(intercept, slope)` floats using `np.linalg.lstsq` on `[1, x]`.
  Raise `ValueError` for fewer than 2 points or mismatched lengths.

**Examples**
```python
solve(np.array([[3., 1.], [1., 2.]]), np.array([9., 8.]))   # array([2., 3.])
fit_line([0, 1, 2], [1, 3, 5])                               # (1.0, 2.0)
solve(np.array([[1., 2.], [2., 4.]]), np.array([1., 2.]))    # raises ValueError
```
''',
"starter": r'''
import numpy as np


def solve(A, b, max_cond=1e12):
    # TODO
    pass


def residual_norm(A, x, b):
    # TODO
    pass


def fit_line(x, y):
    # TODO
    pass
''',
"hints": [
    "Check `A.ndim == 2 and A.shape[0] == A.shape[1] == len(b)`.",
    "Compute `np.linalg.cond(A)` before calling `np.linalg.solve`.",
    "`X = np.column_stack([np.ones(len(x)), x]); w, *_ = np.linalg.lstsq(X, y, rcond=None)`.",
],
"solution": r'''
import numpy as np


def solve(A, b, max_cond=1e12):
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1] or b.shape[0] != A.shape[0]:
        raise ValueError("A must be square and match b")
    c = np.linalg.cond(A)
    if not np.isfinite(c) or c > max_cond:
        raise ValueError(f"ill-conditioned system (cond={c:.3g})")
    return np.linalg.solve(A, b)


def residual_norm(A, x, b):
    return float(np.linalg.norm(np.asarray(A) @ np.asarray(x) - np.asarray(b)))


def fit_line(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("need at least two matching points")
    X = np.column_stack([np.ones(len(x)), x])
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(w[0]), float(w[1])
''',
"explanation": r'''
`solve` validates shapes and refuses ill-conditioned systems before factorising. The residual is
a direct norm. `fit_line` builds the design matrix with an intercept column and lets `lstsq`
minimise the squared residual.
''',
"tests": r'''
import numpy as np

class TestLinalg(unittest.TestCase):
    def test_solve(self):
        np.testing.assert_allclose(S.solve(np.array([[3., 1.], [1., 2.]]), np.array([9., 8.])), [2, 3])

    def test_singular(self):
        with self.assertRaises(ValueError):
            S.solve(np.array([[1., 2.], [2., 4.]]), np.array([1., 2.]))

    def test_ill_conditioned(self):
        with self.assertRaises(ValueError):
            S.solve(np.array([[1., 1.], [1., 1 + 1e-14]]), np.array([2., 2.]))

    def test_shape(self):
        with self.assertRaises(ValueError):
            S.solve(np.ones((2, 3)), np.ones(2))

    def test_residual(self):
        A = np.array([[4., -2, 1], [3, 6, -4], [2, 1, 8]])
        b = np.array([12., -25, 32])
        x = S.solve(A, b)
        self.assertLess(S.residual_norm(A, x, b), 1e-10)
        self.assertIsInstance(S.residual_norm(A, x, b), float)

    def test_fit_line(self):
        i, s = S.fit_line([0, 1, 2], [1, 3, 5])
        self.assertAlmostEqual(i, 1.0)
        self.assertAlmostEqual(s, 2.0)

    def test_fit_line_noisy(self):
        i, s = S.fit_line([0, 1, 2, 3], [1, 2, 2, 4])
        self.assertAlmostEqual(s, 0.9)
        self.assertAlmostEqual(i, 0.9)

    def test_fit_bad(self):
        with self.assertRaises(ValueError):
            S.fit_line([1], [2])
''',
"feedback": [
    ("test_singular", "Check np.linalg.cond(A) (inf or huge for singular matrices) before solving."),
    ("test_fit_line", "Include a column of ones for the intercept; return (intercept, slope)."),
    ("test_fit_line_noisy", "Use np.linalg.lstsq(X, y, rcond=None)."),
    ("test_residual", "Residual is the 2-norm of A@x − b, as a Python float."),
],
},
# ---------------------------------------------------------------- one-hot
{
"slug": "one-hot", "title": "One-Hot Encoding",
"difficulty": "advanced", "prereqs": ["fancy-indexing"], "packages": ["numpy"],
"objectives": ["Encode integer labels as one-hot rows", "Decode with argmax",
               "Validate label ranges"],
"tags": ["one-hot", "encoding", "labels", "fancy-indexing"],
"sources": ["S007", "S013"], "entry": "one_hot(labels, num_classes=None); from_one_hot(Y)",
"article": r'''
# One-Hot Encoding

## Intuition
Class labels like 0 = cat, 1 = dog, 2 = bird are names, not quantities — "bird" is not "twice
dog". One-hot encoding turns each label into a row with a single 1 in its class column, so no
false ordering is implied.

## Precise explanation
For labels $y_i \in \{0,\dots,K-1\}$, the one-hot matrix $Y \in \{0,1\}^{n\times K}$ has
$Y_{i, y_i} = 1$ and zeros elsewhere. Vectorised construction:
```python
Y = np.zeros((n, K))
Y[np.arange(n), labels] = 1
```
(or `np.eye(K)[labels]`). Decoding: `Y.argmax(axis=1)`.

Validation: labels must be non-negative integers below K; if K is not given, use
`labels.max() + 1`.

## Worked example
labels [2, 0, 1] with K = 3 → [[0,0,1],[1,0,0],[0,1,0]].

## Common mistakes
* `Y[:, labels] = 1` — sets whole columns.
* Inferring K from a *batch* and getting different widths for different batches; pass K.
* Negative labels index from the end without error — validate.

## Why this matters
Softmax cross-entropy ([[cross-entropy]]) compares predictions to one-hot targets; categorical features are
one-hot encoded for linear models; tokens are one-hot before an embedding lookup.
''',
"statement": r'''
Implement:
* `one_hot(labels, num_classes=None)` → float array `(n, K)`. Default `K = max(labels) + 1`.
  Raise `ValueError` for empty labels, negative labels, non-integer labels, or labels `>= K`.
* `from_one_hot(Y)` → integer label array via argmax; raise `ValueError` unless every row has
  exactly one 1 and the rest zeros.

**Examples**
```python
one_hot([2, 0, 1])               # [[0,0,1],[1,0,0],[0,1,0]]
one_hot([1], num_classes=4)      # [[0,1,0,0]]
from_one_hot(one_hot([3, 1, 3])) # array([3, 1, 3])
```
''',
"starter": r'''
import numpy as np


def one_hot(labels, num_classes=None):
    # TODO
    pass


def from_one_hot(Y):
    # TODO
    pass
''',
"hints": [
    "`labels = np.asarray(labels)`; check `np.issubdtype(labels.dtype, np.integer)`.",
    "`Y = np.zeros((n, K)); Y[np.arange(n), labels] = 1.0`.",
    "Valid one-hot rows: all entries in {0, 1} and each row sums to 1.",
],
"solution": r'''
import numpy as np


def one_hot(labels, num_classes=None):
    labels = np.asarray(labels)
    if labels.size == 0:
        raise ValueError("labels must be non-empty")
    if not np.issubdtype(labels.dtype, np.integer):
        raise ValueError("labels must be integers")
    if labels.min() < 0:
        raise ValueError("labels must be non-negative")
    K = int(labels.max()) + 1 if num_classes is None else int(num_classes)
    if labels.max() >= K:
        raise ValueError("label out of range")
    Y = np.zeros((labels.size, K))
    Y[np.arange(labels.size), labels.ravel()] = 1.0
    return Y


def from_one_hot(Y):
    Y = np.asarray(Y)
    if Y.ndim != 2 or not np.isin(Y, (0, 1)).all() or not (Y.sum(axis=1) == 1).all():
        raise ValueError("not a valid one-hot matrix")
    return Y.argmax(axis=1)
''',
"explanation": r'''
After validating type and range, paired fancy indexing writes exactly one 1 per row. Decoding
checks the matrix really is one-hot (only zeros/ones, one 1 per row) and returns the argmax.
''',
"tests": r'''
import numpy as np

class TestOneHot(unittest.TestCase):
    def test_basic(self):
        np.testing.assert_array_equal(S.one_hot([2, 0, 1]), [[0, 0, 1], [1, 0, 0], [0, 1, 0]])

    def test_num_classes(self):
        np.testing.assert_array_equal(S.one_hot([1], num_classes=4), [[0, 1, 0, 0]])

    def test_roundtrip(self):
        np.testing.assert_array_equal(S.from_one_hot(S.one_hot([3, 1, 3])), [3, 1, 3])

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            S.one_hot([0, 3], num_classes=3)

    def test_negative(self):
        with self.assertRaises(ValueError):
            S.one_hot([-1, 0])

    def test_float_labels(self):
        with self.assertRaises(ValueError):
            S.one_hot([0.0, 1.0])

    def test_bad_decode(self):
        with self.assertRaises(ValueError):
            S.from_one_hot(np.array([[1, 1, 0]]))
        with self.assertRaises(ValueError):
            S.from_one_hot(np.array([[0.5, 0.5]]))

    def test_dtype_and_sum(self):
        Y = S.one_hot([0, 1, 1, 0])
        self.assertEqual(Y.dtype, np.float64)
        np.testing.assert_array_equal(Y.sum(axis=1), 1)
''',
"feedback": [
    ("test_basic", "Use Y[np.arange(n), labels] = 1, not Y[:, labels] = 1."),
    ("test_negative", "Negative indices silently wrap around in NumPy — validate labels >= 0."),
    ("test_bad_decode", "Check each row has exactly one 1 and only 0/1 entries."),
    ("test_float_labels", "Reject non-integer label dtypes."),
],
},
# ---------------------------------------------------------------- moving-average
{
"slug": "moving-average", "title": "Moving Average with cumsum",
"difficulty": "advanced", "prereqs": ["reshape-stack"], "packages": ["numpy"],
"objectives": ["Compute sliding-window means in O(n) with cumulative sums",
               "Relate moving averages to convolution", "Build sliding windows with sliding_window_view"],
"tags": ["cumsum", "convolution", "sliding-window", "time-series"],
"sources": ["S007"], "entry": "moving_average(x, w); windows(x, w)",
"article": r'''
# Moving Averages

## Intuition
A moving average smooths a noisy signal by replacing each point with the mean of the last *w*
points. Recomputing every window from scratch costs $O(nw)$; with a running total you add the
new value and subtract the one that left — $O(n)$.

## Precise explanation
Let $c_k = \sum_{i<k} x_i$ (with $c_0 = 0$). Then the sum of window $x_j..x_{j+w-1}$ is
$c_{j+w} - c_j$:
```python
c = np.concatenate([[0.0], np.cumsum(x)])
ma = (c[w:] - c[:-w]) / w          # length n - w + 1 ("valid" windows)
```
This equals `np.convolve(x, np.ones(w)/w, mode="valid")`: a moving average is convolution with a
box kernel — the 1-D version of image blurring ([[conv2d-filter]]).

`np.lib.stride_tricks.sliding_window_view(x, w)` returns an `(n-w+1, w)` **read-only view** of all
windows (no copy), handy for other window statistics (max, median).

## Worked example
x = [1, 2, 3, 4, 5], w = 2 → c = [0, 1, 3, 6, 10, 15] → sums [3, 5, 7, 9] → means
[1.5, 2.5, 3.5, 4.5].

## Common mistakes
* Forgetting the leading 0 in the cumulative sum (first window wrong).
* Returning length n with partial windows when "valid" was asked.
* Cumsum on huge float series accumulates rounding error (fine at this scale).

## Why this matters
Rolling features in pandas ([[rolling-features]]), smoothing training-loss curves, and 1-D convolutions in
neural networks ([[conv1d]]) share this structure.
''',
"statement": r'''
Implement:
* `moving_average(x, w)` → float array of length `n - w + 1` with the mean of each full window,
  computed with `np.cumsum` (no Python loops). Raise `ValueError` unless `1 <= w <= len(x)`.
* `windows(x, w)` → `(n - w + 1, w)` array of all windows (use `sliding_window_view`).

**Examples**
```python
moving_average([1, 2, 3, 4, 5], 2)   # array([1.5, 2.5, 3.5, 4.5])
moving_average([4, 8], 2)            # array([6.])
windows(np.arange(4), 3)             # [[0, 1, 2], [1, 2, 3]]
```
''',
"starter": r'''
import numpy as np


def moving_average(x, w):
    # TODO
    pass


def windows(x, w):
    # TODO
    pass
''',
"hints": [
    "`c = np.concatenate([[0.0], np.cumsum(x)])`.",
    "Window sums are `c[w:] - c[:-w]`.",
    "`np.lib.stride_tricks.sliding_window_view(x, w)`.",
],
"solution": r'''
import numpy as np


def moving_average(x, w):
    x = np.asarray(x, dtype=float)
    if not 1 <= w <= len(x):
        raise ValueError("w must satisfy 1 <= w <= len(x)")
    c = np.concatenate([[0.0], np.cumsum(x)])
    return (c[w:] - c[:-w]) / w


def windows(x, w):
    x = np.asarray(x)
    if not 1 <= w <= len(x):
        raise ValueError("w must satisfy 1 <= w <= len(x)")
    return np.lib.stride_tricks.sliding_window_view(x, w)
''',
"explanation": r'''
Prefix sums turn each window sum into one subtraction, so all n − w + 1 means come from two
vector slices. `sliding_window_view` exposes every window as a strided view without copying.
''',
"tests": r'''
import numpy as np

class TestMovingAverage(unittest.TestCase):
    def test_example(self):
        np.testing.assert_allclose(S.moving_average([1, 2, 3, 4, 5], 2), [1.5, 2.5, 3.5, 4.5])

    def test_full_window(self):
        np.testing.assert_allclose(S.moving_average([4, 8], 2), [6.0])

    def test_w1_identity(self):
        np.testing.assert_allclose(S.moving_average([3, -1, 2], 1), [3, -1, 2])

    def test_matches_convolve(self):
        x = np.random.default_rng(0).normal(size=200)
        np.testing.assert_allclose(S.moving_average(x, 7), np.convolve(x, np.ones(7) / 7, mode="valid"),
                                   rtol=1e-10, atol=1e-12)

    def test_bad_w(self):
        with self.assertRaises(ValueError):
            S.moving_average([1, 2], 3)
        with self.assertRaises(ValueError):
            S.moving_average([1, 2], 0)

    def test_windows(self):
        np.testing.assert_array_equal(S.windows(np.arange(4), 3), [[0, 1, 2], [1, 2, 3]])

    def test_windows_mean_consistent(self):
        x = np.arange(10.0) ** 2
        np.testing.assert_allclose(S.windows(x, 4).mean(axis=1), S.moving_average(x, 4))
''',
"feedback": [
    ("test_example", "Prepend 0 to the cumulative sum, then use c[w:] − c[:-w]."),
    ("test_matches_convolve", "Return only full ('valid') windows: length n − w + 1."),
    ("test_bad_w", "Validate 1 <= w <= len(x)."),
    ("test_windows", "Use np.lib.stride_tricks.sliding_window_view(x, w)."),
],
},
]
