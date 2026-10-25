# PD-10 · Merging Tables

**Topic:** Pandas · **Difficulty:** intermediate · **Allowed packages:** pandas, numpy

**Builds on:** PD-08 Group-by Aggregation

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `orders_with_customers(orders, customers)` → left join of `orders` (`order_id, customer_id,
  amount`) with `customers` (`customer_id, name`) on `customer_id`, `validate="many_to_one"`,
  missing names filled with `"unknown"`, rows in original order with index 0..n−1.
  Duplicate customer ids must raise (pandas raises `pd.errors.MergeError`).
* `spend_per_customer(orders, customers)` → DataFrame `name, total` (sum of amounts per name,
  including `"unknown"`), sorted by `total` descending then `name` ascending.

**Example**
```python
orders = pd.DataFrame({"order_id": [1, 2, 3, 4], "customer_id": [1, 2, 9, 1], "amount": [50, 20, 5, 10]})
customers = pd.DataFrame({"customer_id": [1, 2], "name": ["Ann", "Bob"]})
orders_with_customers(orders, customers)["name"].tolist()   # ['Ann', 'Bob', 'unknown', 'Ann']
spend_per_customer(orders, customers)  # Ann 60, Bob 20, unknown 5
```

## Hints

<details><summary>Hint 1</summary>

`pd.merge(orders, customers, on='customer_id', how='left', validate='many_to_one')`.

</details>

<details><summary>Hint 2</summary>

`merged.assign(name=merged['name'].fillna('unknown'))`.

</details>

<details><summary>Hint 3</summary>

Group by name, sum amount, then sort_values(['total', 'name'], ascending=[False, True]).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_row_count_kept` | Use how='left' so orders without a customer are kept. |
| `test_duplicate_customer` | Pass validate='many_to_one' to merge. |
| `test_names` | Fill missing names with 'unknown' after the merge. |
| `test_spend_tie` | Sort by total descending, then name ascending. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A left join keeps every order; `validate` guards against duplicate customers, and missing
matches are labelled "unknown". The spend table groups the merged rows by name and sorts with a
deterministic tie-break.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
