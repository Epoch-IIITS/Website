# AG-P2 · Project idea: Club Event Assistant

**Topic:** Agentic AI · ungraded

## Brief

Build an assistant for a student club that answers questions about upcoming events, drafts
announcements and registration reminders — and never sends anything without a committee member's
approval.

## You will use

- LM-20 Retrieval-Augmented Generation with LangChain
- AG-08 A ReAct Agent in LangGraph
- AG-14 Validating Tool Arguments and Retrying
- AG-18 Guardrails with Human Approval

## Milestones

1. Put event details in a small JSON or CSV file and answer FAQ-style questions about them with retrieval.
2. Add a draft_announcement tool that returns text but sends nothing.
3. Add a send_message tool behind an approval interrupt; show the draft and ask approve or reject.
4. Validate tool arguments (dates in the future, known channels, length limits) and retry on errors.
5. Log every proposed and approved action with a timestamp for review.

## Stretch goals

- Support edits: the reviewer can change the draft before approving.
- Connect a real channel (email or a chat webhook) only after everything else is tested.
- Write evaluation cases for refusals: requests the assistant must not act on.

## Data

Use a sample events file you create (titles, dates, venues, registration links). Keep real contact lists
out of the project until the approval flow is reliable.

## Run it yourself

```bash
pip install langgraph langchain-core
python assistant.py
```
