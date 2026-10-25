# PY-P1 · Project idea: Expense Tracker CLI

**Topic:** Python · ungraded

## Brief

Build a command-line program that records your expenses, saves them to a JSON file between runs, and
prints summaries: total this month, spending by category and your biggest purchases.

## You will use

- PY-04 Reading Input
- PY-09 For Loops and range: FizzBuzz
- PY-18 Gradebook Aggregation
- PY-21 Safe Division with Exceptions
- PY-23 Files, CSV and JSON

## Milestones

1. Ask for an amount, a category and a note with input() and keep the expense in a list of dicts.
2. Save the list to expenses.json when the program exits and load it when it starts.
3. Add a menu: add, list, summary, quit.
4. Summarise totals per category with a dict, sorted from largest to smallest.
5. Handle bad input (letters for an amount, an empty category) without crashing.

## Stretch goals

- Use argparse so commands like `python expenses.py add 120 food lunch` work without a menu.
- Export a month to CSV.
- Set monthly budgets per category and warn when one is exceeded.

## Data

Your own expenses — or invent a week of them to test with. See the [json module](https://docs.python.org/3/library/json.html)
and [argparse](https://docs.python.org/3/library/argparse.html) documentation.

## Run it yourself

```bash
python expenses.py
```
Only the standard library is needed.
