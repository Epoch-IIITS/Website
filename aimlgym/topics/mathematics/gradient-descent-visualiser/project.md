# MA-P1 · Project idea: Gradient-Descent Visualiser

**Topic:** Mathematics for AI/ML · ungraded

## Brief

Build a tool that animates gradient descent on functions you choose — a bowl, a long narrow valley, a
function with two minima — so you can see how the learning rate, the starting point and the shape of
the function change the path.

## You will use

- MA-11 Derivative Rules and the Chain Rule
- MA-13 Gradient Descent in 1D
- MA-14 Numerical Gradient of f(x1..xn)
- MA-15 Taylor Series for exp(x)

## Milestones

1. Write gradient descent for one variable and print the sequence of points for f(x) = (x - 3)².
2. Extend it to two variables using numerical gradients, for any function you pass in.
3. Plot contour lines of f(x, y) with matplotlib and draw the path on top.
4. Compare learning rates that converge, oscillate and diverge on the same function.
5. Show a function with two minima where the starting point decides which one is found.

## Stretch goals

- Add momentum and compare its path in a narrow valley.
- Animate the path with matplotlib's animation module and save a GIF.
- Let the user type a formula and parse it safely.

## Data

No data: the functions are your own. See matplotlib's [animation guide](https://matplotlib.org/stable/users/explain/animations/animations.html).

## Run it yourself

```bash
pip install numpy matplotlib
python descent.py
```
