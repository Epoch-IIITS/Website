import math
import re
from collections import Counter


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def chunk_words(text, size, overlap):
    # TODO
    return [text]


def retrieve(query, chunks, k):
    # TODO: TF-IDF + cosine
    return [(i, 0.0) for i in range(min(k, len(chunks)))]


def build_prompt(question, passages):
    # TODO
    return question


def answer(question, chunks, model, k=2):
    # TODO
    reply = model(question)
    return {"answer": reply, "sources": [], "cited": [], "grounded": False}
