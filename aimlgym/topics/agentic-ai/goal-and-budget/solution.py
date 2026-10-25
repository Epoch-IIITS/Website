r"""Reference solution for AG-05 Goal Tests and Step Budgets.

The goal is tested before each action so solved tasks stop immediately. After every action the cost is
accumulated and compared with the budget. When the step limit is reached, a final goal test decides
between success and step_limit.
"""
def run_with_budget(state, policy, transition, goal_test, max_steps, max_cost=None):
    if max_steps < 0:
        raise ValueError("max_steps must be >= 0")
    actions, total = [], 0.0

    def result(status):
        return {"status": status, "state": state, "actions": actions, "cost": total}

    for _ in range(max_steps):
        if goal_test(state):
            return result("success")
        a = policy(state)
        state, cost = transition(state, a)
        actions.append(a)
        total += cost
        if max_cost is not None and total > max_cost:
            return result("cost_exceeded")
    return result("success" if goal_test(state) else "step_limit")
