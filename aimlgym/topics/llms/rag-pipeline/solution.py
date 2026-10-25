r"""Reference solution for LM-21 Retrieval-Augmented Generation by Hand.

Chunking advances by `size - overlap` and stops after the window that reaches the end, so no
trailing chunk is a subset of the previous one. Retrieval builds smoothed-IDF weights from the
chunks only, normalises every vector, and ranks by dot product (cosine) with a deterministic
tie-break. The pipeline makes exactly one model call and checks citations against the numbered
passages it actually provided.
"""
import math
import re
from collections import Counter


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def chunk_words(text, size, overlap):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("need size > 0 and 0 <= overlap < size")
    words = text.split()
    chunks = []
    for start in range(0, len(words), size - overlap):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
    return chunks


def _unit(vec):
    norm = math.sqrt(sum(v * v for v in vec.values()))
    return {t: v / norm for t, v in vec.items()} if norm else {}


def retrieve(query, chunks, k):
    docs = [Counter(tokens(c)) for c in chunks]
    n = len(docs)
    df = Counter(t for d in docs for t in d)
    idf = {t: math.log((1 + n) / (1 + df[t])) + 1 for t in df}
    vecs = [_unit({t: c * idf[t] for t, c in d.items()}) for d in docs]
    q = _unit({t: c * idf[t] for t, c in Counter(tokens(query)).items() if t in idf})
    scores = [(i, float(sum(w * v.get(t, 0.0) for t, w in q.items()))) for i, v in enumerate(vecs)]
    scores.sort(key=lambda s: (-s[1], s[0]))
    return scores[:k]


def build_prompt(question, passages):
    lines = ["Answer using only the sources below. Cite sources like [1]."]
    lines += [f"[{i}] {p}" for i, p in enumerate(passages, 1)]
    lines.append(f"Question: {question}")
    return "\n".join(lines)


def answer(question, chunks, model, k=2):
    hits = retrieve(question, chunks, k)
    sources = [i for i, _ in hits]
    reply = model(build_prompt(question, [chunks[i] for i in sources]))
    cited = sorted({int(x) for x in re.findall(r"\[(\d+)\]", reply)})
    grounded = bool(cited) and all(1 <= c <= len(sources) for c in cited)
    return {"answer": reply, "sources": sources, "cited": cited, "grounded": grounded}
