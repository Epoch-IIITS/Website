# Guardrails with Human Approval

## Learning outcomes

After this lesson you can:

- Pause a graph with interrupt() to ask a person for approval
- Resume it with Command(resume=...) on the same thread
- Allow safe actions, require approval for sensitive ones and block unknown ones

## Intuition
An agent that can send emails or delete records should not do so on its own judgement. A guardrail
checks each proposed action: harmless ones run, unknown ones are refused, and sensitive ones **pause**
until a person approves. The pause must survive while the person thinks — so the graph's state is
saved, and the run resumes exactly where it stopped.

## Precise explanation
```python
from langgraph.types import Command, interrupt

def guard(state):
    action = state["action"]
    if action["tool"] not in tools:
        return {"outcome": "blocked"}
    if action["tool"] in sensitive:
        decision = interrupt({"action": action})        # pauses here
        if decision != "approve":
            return {"outcome": "rejected"}
    return {"outcome": "approved"}

app = graph.compile(checkpointer=InMemorySaver())       # interrupts need a checkpointer
first = app.invoke({"action": action}, config)          # stops: first["__interrupt__"][0].value
final = app.invoke(Command(resume="approve"), config)   # continues; interrupt() returns "approve"
```

* `interrupt(payload)` saves the state and ends the current `invoke`; the result contains
  `"__interrupt__"`, whose `.value` is the payload shown to the person.
* `Command(resume=value)` on the **same thread** restarts the interrupted node; this time `interrupt`
  returns `value`. Code before the `interrupt` call runs again, so keep side effects after it.
* The decision is data from outside the program: compare it with an exact value and treat anything else
  as a rejection.

## Worked example
Tools: `read_calendar` (safe), `send_email` (sensitive). `read_calendar` runs at once.
`send_email` pauses with the payload `{"action": {...}}`; with "approve" it runs and the outcome is
"approved: sent"; with "reject" nothing is sent. `delete_all` is blocked.

## What the library does inside
The permission checks of AG-19 (the optional deep dive after this step), with a
checkpointed pause in place of a blocking `input()` call.

## Common mistakes
* No checkpointer: `interrupt` cannot pause.
* Resuming with a different `thread_id`, which starts a new run.
* Performing the side effect before the interrupt, so it happens twice on resume.
* Treating any non-empty reply as approval.

## Why this matters
Human approval is required by many organisations for agents that act on real systems; the
club-event-assistant project idea after this step uses it before sending announcements.

## References

- [Interrupts (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/interrupts) — LangChain (`S138`)
- [Persistence (LangGraph docs)](https://docs.langchain.com/oss/python/langgraph/persistence) — LangChain (`S137`)
