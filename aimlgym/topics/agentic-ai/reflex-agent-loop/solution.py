r"""Reference solution for AG-04 Perceive-Act Loop.

The agent sees only its percept and applies condition–action rules. The environment owns the state
and dynamics. The loop alternates perception, decision and execution, scoring cleanliness and
penalising movement after every step.
"""
def reflex_vacuum_agent(percept):
    location, status = percept
    if status == "Dirty":
        return "Suck"
    return "Right" if location == "A" else "Left"


class VacuumWorld:
    def __init__(self, dirt, location):
        if location not in ("A", "B") or set(dirt) != {"A", "B"}:
            raise ValueError("invalid world")
        self.dirt = dict(dirt)
        self.location = location

    def percept(self):
        return (self.location, "Dirty" if self.dirt[self.location] else "Clean")

    def execute(self, action):
        if action == "Suck":
            self.dirt[self.location] = False
        elif action == "Left":
            self.location = "A"
        elif action == "Right":
            self.location = "B"
        else:
            raise ValueError(f"unknown action {action!r}")


def run(agent, env, steps):
    log, score = [], 0
    for _ in range(steps):
        p = env.percept()
        a = agent(p)
        env.execute(a)
        log.append((p, a))
        score += sum(not d for d in env.dirt.values()) - (1 if a in ("Left", "Right") else 0)
    return log, score
