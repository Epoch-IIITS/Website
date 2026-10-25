# PD-P1 · Project idea: Exploratory Analysis of a Public Dataset

**Topic:** Pandas · ungraded

## Brief

Pick a public dataset that interests you and answer three questions about it with pandas: clean it,
group and merge it, chart the findings and write them up as a short report a non-programmer can read.

## You will use

- PD-03 Reading and Writing CSV
- PD-04 Select and Filter Rows
- PD-06 Finding and Handling Missing Values
- PD-08 Group-by Aggregation
- PD-10 Merging Tables

## Milestones

1. Choose a dataset and write down three questions before looking at the numbers.
2. Load it, inspect dtypes and missing values, and fix types and obvious errors.
3. Answer each question with groupby, filtering or a merge with a second table.
4. Make one clear chart per question with pandas plotting or matplotlib.
5. Write a one-page summary with the answers, the charts and the caveats.

## Stretch goals

- Add a time-series view with resampling.
- Turn the analysis into a script that regenerates the report from the raw file.
- Publish the report as an HTML page.

## Data

* [Bike Sharing dataset](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset) (UCI): hourly
  rentals with weather and calendar data.
* [Our World in Data](https://ourworldindata.org/): many downloadable CSVs on health, energy and more.

## Run it yourself

```bash
pip install pandas matplotlib
python eda.py
```
See the [pandas visualisation guide](https://pandas.pydata.org/docs/user_guide/visualization.html).
