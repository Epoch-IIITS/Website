"""Ungraded project ideas for the pandas topic (library revision, Phase 6)."""

PROBLEMS = [
{
"kind": "project", "slug": "public-dataset-eda", "title": "Exploratory Analysis of a Public Dataset",
"tags": ["exploratory-data-analysis", "cleaning", "reporting"],
"brief": r'''
Pick a public dataset that interests you and answer three questions about it with pandas: clean it,
group and merge it, chart the findings and write them up as a short report a non-programmer can read.
''',
"uses": ["read-csv-io", "select-filter", "missing-values", "groupby-agg", "merge-tables"],
"milestones": [
    "Choose a dataset and write down three questions before looking at the numbers.",
    "Load it, inspect dtypes and missing values, and fix types and obvious errors.",
    "Answer each question with groupby, filtering or a merge with a second table.",
    "Make one clear chart per question with pandas plotting or matplotlib.",
    "Write a one-page summary with the answers, the charts and the caveats.",
],
"stretch": [
    "Add a time-series view with resampling.",
    "Turn the analysis into a script that regenerates the report from the raw file.",
    "Publish the report as an HTML page.",
],
"data": r'''
* [Bike Sharing dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) (UCI): hourly
  rentals with weather and calendar data.
* [Our World in Data](https://ourworldindata.org/): many downloadable CSVs on health, energy and more.
''',
"setup": r'''
```bash
pip install pandas matplotlib
python eda.py
```
See the [pandas visualisation guide](https://pandas.pydata.org/docs/user_guide/visualization.html).
''',
},
{
"kind": "project", "slug": "personal-finance-data", "title": "Personal Finance Dashboard Data",
"tags": ["time-series", "pivot-tables", "cleaning"],
"brief": r'''
Turn messy bank-statement style CSV files into tidy monthly and category summaries — the data layer of
a personal-finance dashboard: income, spending by category, savings rate and unusual transactions.
''',
"uses": ["string-cleaning", "datetime-basics", "resample-weekly", "pivot-table", "binning-cut", "rolling-features"],
"milestones": [
    "Generate a year of fake transactions (date, description, amount) in two different CSV formats.",
    "Load both, standardise column names, dates and signs, and combine them.",
    "Assign categories from description keywords with string methods.",
    "Build monthly totals per category with resample and a pivot table.",
    "Flag unusual transactions with a rolling mean and standard deviation per category.",
],
"stretch": [
    "Add budgets and compute the remaining amount per category each month.",
    "Draw the dashboard with matplotlib or a small web page.",
    "Write tests for the cleaning functions with unusual inputs.",
],
"data": r'''
Generate realistic fake data with NumPy and pandas (salary on the 1st, rent, groceries, occasional
large purchases). Never commit real bank statements to a repository.
''',
"setup": r'''
```bash
pip install pandas numpy matplotlib
python finance.py statements/
```
''',
},
]
