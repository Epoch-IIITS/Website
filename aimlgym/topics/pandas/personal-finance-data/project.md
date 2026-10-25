# PD-P2 · Project idea: Personal Finance Dashboard Data

**Topic:** Pandas · ungraded

## Brief

Turn messy bank-statement style CSV files into tidy monthly and category summaries — the data layer of
a personal-finance dashboard: income, spending by category, savings rate and unusual transactions.

## You will use

- PD-11 Cleaning Text Columns
- PD-12 Working with Dates
- PD-13 Weekly Resampling
- PD-14 Pivot Tables
- PD-15 Binning with pd.cut
- PD-16 Rolling-Window Features

## Milestones

1. Generate a year of fake transactions (date, description, amount) in two different CSV formats.
2. Load both, standardise column names, dates and signs, and combine them.
3. Assign categories from description keywords with string methods.
4. Build monthly totals per category with resample and a pivot table.
5. Flag unusual transactions with a rolling mean and standard deviation per category.

## Stretch goals

- Add budgets and compute the remaining amount per category each month.
- Draw the dashboard with matplotlib or a small web page.
- Write tests for the cleaning functions with unusual inputs.

## Data

Generate realistic fake data with NumPy and pandas (salary on the 1st, rent, groceries, occasional
large purchases). Never commit real bank statements to a repository.

## Run it yourself

```bash
pip install pandas numpy matplotlib
python finance.py statements/
```
