r"""Reference solution for PY-22 Guessing Game Feedback.

Slicing `guesses[:max_attempts]` enforces the attempt budget up front. Each guess produces one
feedback string; on a correct guess the flag is set and the loop breaks, so later guesses are
never processed. Because exactly one string is appended per processed guess, `attempts` is just
the length of the feedback list.
"""
def guess_feedback(target, guesses, max_attempts=7):
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")
    feedback = []
    won = False
    for g in guesses[:max_attempts]:
        if g < target:
            feedback.append("too low")
        elif g > target:
            feedback.append("too high")
        else:
            feedback.append("correct")
            won = True
            break
    return {"feedback": feedback, "attempts": len(feedback), "won": won}
