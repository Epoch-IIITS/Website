# RL-P2 · Project idea: Bandit-Based Recommender

**Topic:** Reinforcement Learning · ungraded

## Brief

Build a recommender that picks which article to show next, learning from simulated clicks. Compare
random choice, epsilon-greedy and UCB by their cumulative regret, and see what happens when reader
interests change over time.

## You will use

- RL-05 Epsilon-Greedy Action Selection
- RL-06 Incremental Value Estimates
- RL-07 UCB1 Bandit

## Milestones

1. Simulate 10 articles with hidden click probabilities and a reader who clicks with those probabilities.
2. Implement random, epsilon-greedy and UCB recommenders with the same interface.
3. Run each for 10,000 recommendations over 20 seeds and plot average cumulative regret.
4. Make the click probabilities drift slowly and add a sliding-window version of UCB.
5. Write up which strategy you would deploy and why.

## Stretch goals

- Implement Thompson sampling with Beta distributions.
- Add reader features (contextual bandits) with one linear model per article.
- Serve recommendations from a FastAPI endpoint that updates on click events.

## Data

Everything is simulated with seeded NumPy generators, so experiments are reproducible.

## Run it yourself

```bash
pip install numpy matplotlib
python bandits.py --strategy ucb --steps 10000
```
