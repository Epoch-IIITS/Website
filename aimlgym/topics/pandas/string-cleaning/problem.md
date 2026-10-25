# PD-11 · Cleaning Text Columns

**Topic:** Pandas · **Difficulty:** intermediate · **Allowed packages:** pandas, numpy

**Builds on:** PD-06 Finding and Handling Missing Values

Read the lesson first: [article.md](article.md)

## Task

Write `clean_contacts(df)` for columns `name`, `phone`, `email` (strings, may be missing).
Return a new DataFrame with:
* `name`: stripped, internal whitespace collapsed to one space, title case;
* `phone`: digits only;
* `email`: stripped and lower-cased;
* `domain`: the part after `@` in the cleaned email (missing if there is no `@`).
Missing inputs must remain missing (check with `pd.isna`).

**Example**
```python
clean_contacts(pd.DataFrame({"name": ["  ann   LEE "], "phone": ["+91 98-765 43210"],
                             "email": [" Ann.Lee@Example.COM "]})).iloc[0].tolist()
# ['Ann Lee', '919876543210', 'ann.lee@example.com', 'example.com']
```

## Hints

<details><summary>Hint 1</summary>

`df['name'].str.strip().str.replace(r'\s+', ' ', regex=True).str.title()`.

</details>

<details><summary>Hint 2</summary>

`df['phone'].str.replace(r'\D', '', regex=True)`.

</details>

<details><summary>Hint 3</summary>

`email.str.split('@').str[1]` — NaN when there is no '@'.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_row0` | Collapse whitespace with str.replace(r'\s+', ' ', regex=True) after strip. |
| `test_phone_digits` | Remove all non-digits with the regex \D. |
| `test_no_at_domain_missing` | If there is no '@', domain must be missing, not the whole email. |
| `test_missing_stays_missing` | Don't use astype(str); .str methods keep NaN as NaN. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each column is cleaned with a chain of vectorised `.str` operations. The domain is the second
element after splitting on '@'; `.where(len > 1)` keeps it missing when there was no '@'. Missing
inputs propagate as missing through every `.str` call.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
