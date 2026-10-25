# RL-P1 · Project idea: Grid Game Agent

**Topic:** Reinforcement Learning · ungraded

## Brief

Design a small grid game of your own — collect keys and reach the door, avoid moving guards, or push a
box onto a target — as a Gymnasium environment, then train a Q-learning agent to play it and watch it
improve.

## You will use

- RL-01 Discounted Return
- RL-04 Gymnasium Environments
- RL-13 Tabular Q-Learning
- RL-14 Q-Learning on FrozenLake
- RL-15 SARSA

## Milestones

1. Define the rules, the state encoding and the rewards on paper; keep the state space small.
2. Implement the game as a gymnasium.Env and pass check_env.
3. Print the grid as text after each step so you can play it yourself with the keyboard.
4. Train Q-learning and plot the success rate and average return per 100 episodes.
5. Compare Q-learning with SARSA and explain any difference in the learned behaviour.

## Stretch goals

- Make the game stochastic (slippery moves, random guards) and compare again.
- Replace the table with a small neural network (deep Q-learning) for a larger grid.
- Record and replay an episode as an animated GIF.

## Data

No data is needed: the agent learns from playing your game. See the
[FrozenLake documentation](https://gymnasium.farama.org/environments/toy_text/frozen_lake/) for a
text-based environment to imitate.

## Run it yourself

```bash
pip install gymnasium numpy matplotlib
python train_agent.py
```
