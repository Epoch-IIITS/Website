# NumPy

**You will be able to:** Replace Python loops with arrays: vectorised arithmetic, slicing, masks, reductions, matrix products, broadcasting, reshaping, gathers, seeded randomness and linear algebra.

**Topic prerequisites:** Statistics

NumPy replaces Python loops over numbers with operations on whole arrays. The topic starts by
creating and inspecting arrays and repeating the loops you wrote in Mathematics as vectorised
expressions, then covers slicing, masks, axis reductions, matrix products, broadcasting,
reshaping, gathers, seeded random generators, pairwise distances, linear solvers, one-hot
encoding and sliding windows.

**Packages:** `numpy` (validated on 2.2 and 2.5). Most tests check a NumPy implementation
against a plain-Python reference so you can see they compute the same thing.

**Project ideas:** ungraded briefs between steps suggest things to build with what you have learned so far.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | NP-01 | [Create an Array and Inspect It](array-info/problem.md) | beginner | PY-20 |
| 2 | NP-02 | [Vectorised Arithmetic and ufuncs](vectorized-math/problem.md) | beginner | NP-01, MA-03 |
| 3 | NP-03 | [Slicing a Sub-grid](slicing-subgrid/problem.md) | beginner | NP-01 |
| 4 | NP-04 | [Boolean Masks](boolean-mask/problem.md) | beginner | NP-03 |
| 5 | NP-05 | [Aggregations Along Axes](axis-aggregations/problem.md) | beginner | NP-02 |
| 6 | NP-06 | [Matrix Products with @](matmul-dot/problem.md) | intermediate | NP-05, MA-06 |
| 7 | NP-07 | [Centering Columns with Broadcasting](broadcast-center/problem.md) | intermediate | NP-05, ST-05 |
| 8 | NP-08 | [Reshape and Stack](reshape-stack/problem.md) | intermediate | NP-03 |
| 9 | NP-09 | [Fancy Indexing and Gather](fancy-indexing/problem.md) | intermediate | NP-04, NP-05 |
| 10 | NP-10 | [Seeded Random Generators](seeded-generator/problem.md) | intermediate | NP-09, ST-10 |
| 11 | NP-11 | [Vectorized Pairwise Distances](pairwise-distances/problem.md) | advanced | NP-07, NP-06 |
| 12 | NP-12 | [Solve Linear Systems Safely](linalg-solve/problem.md) | advanced | NP-06, MA-08 |
| 13 | NP-13 | [One-Hot Encoding](one-hot/problem.md) | advanced | NP-09 |
| 14 | NP-14 | [Moving Average with cumsum](moving-average/problem.md) | advanced | NP-08 |
| 15 | NP-P1 | [Project idea: Photo Filters with NumPy](numpy-photo-filters/project.md) | ungraded | NP-01, NP-02, NP-03, NP-05, NP-07, NP-14 |
