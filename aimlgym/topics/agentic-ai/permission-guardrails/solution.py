r"""Reference solution for AG-19 Permission Guardrails.

The guard evaluates every model-proposed call against the policy in a fixed order and only updates
counters for calls that really run. The runner iterates over model calls alone: tool outputs are
recorded as data and never interpreted, so instructions injected into outputs cannot trigger actions.
"""
class Guard:
    def __init__(self, policy):
        if "allowed" not in policy:
            raise ValueError("policy must define 'allowed'")
        self.allowed = set(policy["allowed"])
        self.max_calls = dict(policy.get("max_calls", {}))
        self.costs = dict(policy.get("costs", {}))
        self.budget = policy.get("budget")
        self.needs_approval = set(policy.get("needs_approval", set()))
        self.counts = {}
        self.spent = 0

    def check(self, call):
        name = call.get("tool")
        if name not in self.allowed:
            return "deny: tool not allowed"
        if name in self.max_calls and self.counts.get(name, 0) >= self.max_calls[name]:
            return "deny: call limit reached"
        if self.budget is not None and self.spent + self.costs.get(name, 0) > self.budget:
            return "deny: budget exceeded"
        if name in self.needs_approval:
            return "needs_approval"
        return "allow"

    def record(self, call):
        name = call["tool"]
        self.counts[name] = self.counts.get(name, 0) + 1
        self.spent += self.costs.get(name, 0)


def run_guarded(model_calls, guard, tools, approve):
    log = []
    for call in model_calls:
        decision = guard.check(call)
        if decision.startswith("deny"):
            log.append({"call": call, "decision": decision})
            continue
        if decision == "needs_approval" and not approve(call):
            log.append({"call": call, "decision": "deny: not approved"})
            continue
        output = tools[call["tool"]](**call.get("args", {}))
        guard.record(call)
        log.append({"call": call, "decision": "executed", "output": output})
    return log
