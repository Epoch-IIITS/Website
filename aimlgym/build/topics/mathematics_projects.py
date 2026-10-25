"""Ungraded project ideas for the Mathematics topic (library revision, Phase 6)."""

PROBLEMS = [
{
"kind": "project", "slug": "gradient-descent-visualiser", "title": "Gradient-Descent Visualiser",
"tags": ["optimisation", "visualisation", "calculus"],
"brief": r'''
Build a tool that animates gradient descent on functions you choose — a bowl, a long narrow valley, a
function with two minima — so you can see how the learning rate, the starting point and the shape of
the function change the path.
''',
"uses": ["derivative-rules", "gradient-descent-1d", "numerical-gradient", "taylor-exp"],
"milestones": [
    "Write gradient descent for one variable and print the sequence of points for f(x) = (x - 3)².",
    "Extend it to two variables using numerical gradients, for any function you pass in.",
    "Plot contour lines of f(x, y) with matplotlib and draw the path on top.",
    "Compare learning rates that converge, oscillate and diverge on the same function.",
    "Show a function with two minima where the starting point decides which one is found.",
],
"stretch": [
    "Add momentum and compare its path in a narrow valley.",
    "Animate the path with matplotlib's animation module and save a GIF.",
    "Let the user type a formula and parse it safely.",
],
"data": r'''
No data: the functions are your own. See matplotlib's [animation guide](https://matplotlib.org/stable/users/explain/animations/animations.html).
''',
"setup": r'''
```bash
pip install numpy matplotlib
python descent.py
```
''',
},
]
