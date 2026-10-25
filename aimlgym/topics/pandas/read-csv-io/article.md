# Reading and Writing CSV

## Learning outcomes

After this lesson you can:

- Read CSV text with pd.read_csv and an in-memory io.StringIO buffer
- Check the dtypes pandas inferred
- Write a DataFrame back to CSV without its index
- Compare pandas parsing with the csv module

## Intuition
In PY-23 you read a CSV with `csv.DictReader` and converted every number yourself.
`pd.read_csv` does the reading, splitting, quoting **and** type conversion in one call, and
returns a DataFrame ready for analysis.

## Precise explanation
```python
import io
import pandas as pd
text = "name,score,passed\nada,91,True\nbob,78,False\n"
df = pd.read_csv(io.StringIO(text))     # a file path works the same way
df.dtypes      # name: string-like, score: int64, passed: bool
df.to_csv(index=False)                  # back to CSV text
```
* `io.StringIO(text)` wraps a string so it behaves like an open file; tests use it so no files
  are needed. `pd.read_csv("data.csv")` reads from disk.
* pandas **infers** dtypes: whole numbers → `int64`, decimals → `float64`, `True`/`False` →
  `bool`, text → `object` (pandas 2) or `str` (pandas 3). An empty field becomes `NaN`, which
  turns an integer column into `float64`.
* Useful options: `sep=";"`, `usecols=[...]`, `dtype={"zip": str}` (keep leading zeros),
  `na_values=["?"]`.
* `df.to_csv(index=False)` omits the row numbers, which are rarely wanted in a file.

## Worked example
`"a,b\n1,2.5\n3,\n"` → column `a` is `int64` `[1, 3]`; column `b` is `float64` `[2.5, NaN]`.

## Common mistakes
* Forgetting `index=False` and getting an extra unnamed column when reading the file back.
* Leading zeros lost: `"007"` is read as the integer 7 unless you pass `dtype=str`.
* Checking `df.dtypes == object` for text, which fails on pandas 3; use
  `pd.api.types.is_string_dtype`.

## Why this matters
Almost every dataset in practice starts as a CSV; knowing what `read_csv` infers prevents silent
type bugs before modelling.

## References

- [IO tools (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/io.html) — pandas development team (`S085`)
- [csv — CSV file reading and writing](https://docs.python.org/3/library/csv.html) — Python Software Foundation (`S055`)
- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
