r"""Reference solution for ST-10 Dice Simulation and the Law of Large Numbers.

A private generator seeded once makes the whole simulation reproducible. Each die face comes from
a single `rng.random()` call (the only output Python guarantees across versions). One loop records
the sum, updates the frequency table and the running mean.
"""
import random


def roll(rng):
    return int(rng.random() * 6) + 1


def simulate_two_dice(n, seed):
    if n < 1:
        raise ValueError("n must be >= 1")
    rng = random.Random(seed)
    sums, running = [], []
    freq = {s: 0 for s in range(2, 13)}
    total = 0
    for i in range(n):
        s = roll(rng) + roll(rng)
        sums.append(s)
        freq[s] += 1
        total += s
        running.append(total / (i + 1))
    return {"sums": sums, "running_mean": running, "freq": freq}
