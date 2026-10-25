# ST-P2 · Project idea: Dice and Coin Simulator

**Topic:** Statistics · ungraded

## Brief

Build a simulator that rolls dice and flips coins thousands of times and shows, in numbers and
simple text charts, how averages settle down (the law of large numbers), how sums of dice become
bell-shaped (the central limit theorem), and how often "unlikely" streaks really happen.

## You will use

- ST-10 Dice Simulation and the Law of Large Numbers
- ST-04 Histogram with Equal-Width Bins
- ST-08 Binomial Probabilities
- ST-12 Sampling Distributions and Standard Error
- ST-14 Introducing scipy.stats

## Milestones

1. Simulate n fair coin flips with a seeded generator and print the running proportion of heads.
2. Roll k dice many times and print a text histogram of the sums.
3. Compare the simulated frequencies with the exact binomial probabilities from scipy.stats.
4. Measure the longest run of heads in 100 flips across many trials and report how often it is 6 or more.

## Stretch goals

- Add loaded dice and use a chi-square test to see how many rolls it takes to detect them.
- Plot the running mean with matplotlib and show the ±2 standard error band shrinking like 1/√n.
- Turn it into a small command-line game where players bet on outcomes.

## Data

No data is needed: everything is simulated with `numpy.random.default_rng(seed)`, so every run with
the same seed gives the same results.

## Run it yourself

```bash
pip install numpy scipy
python simulator.py --dice 3 --rolls 10000 --seed 1
```
Optional: `pip install matplotlib` for charts.
