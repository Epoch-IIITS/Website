r"""Reference solution for AG-09 Conversation Memory with trim_messages.

One helper holds the policy — keep the latest turns, the system message, and start on a human turn —
and the two public functions differ only in how size is measured: number of messages or number of
words.
"""
from langchain_core.messages import trim_messages


def _trim(messages, budget, counter):
    if budget < 1:
        raise ValueError("budget must be at least 1")
    return trim_messages(messages, max_tokens=budget, token_counter=counter,
                         strategy="last", include_system=True, start_on="human")


def trim_history(messages, max_messages):
    return _trim(messages, max_messages, len)


def count_words(messages):
    return sum(len(str(m.content).split()) for m in messages)


def trim_by_words(messages, max_words):
    return _trim(messages, max_words, count_words)
