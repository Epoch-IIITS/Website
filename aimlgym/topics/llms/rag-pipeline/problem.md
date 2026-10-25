# LM-21 · Retrieval-Augmented Generation by Hand

**Topic:** Large Language Models · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** LM-18 Chat Prompt Templates, NL-11 Cosine Similarity Retrieval

Read the lesson first: [article.md](article.md)

## Task

Tokenise with `re.findall(r"[a-z0-9]+", text.lower())`. Implement:

1. `chunk_words(text, size, overlap)` → list of chunk strings (words joined by spaces). Raise
   `ValueError` unless `size > 0` and `0 <= overlap < size`. Empty text → `[]`.
2. `retrieve(query, chunks, k)` → list of `(index, score)` for the top `k` chunks by cosine
   similarity of TF-IDF vectors (raw counts × smoothed IDF from the chunks, L2-normalised; query
   terms not in any chunk are ignored). Sort by score descending, then index ascending. Scores are
   floats.
3. `build_prompt(question, passages)` → exactly:
   ```
   Answer using only the sources below. Cite sources like [1].
   [1] <passage 1>
   [2] <passage 2>
   Question: <question>
   ```
4. `answer(question, chunks, model, k=2)` → retrieve, build the prompt from the retrieved chunk
   texts (best first), call `model(prompt)` once, and return
   `{"answer": reply, "sources": [chunk indices in prompt order], "cited": sorted unique cited
   numbers, "grounded": bool}`.

## Hints

<details><summary>Hint 1</summary>

Chunking: `step = size - overlap`; loop `start` over `range(0, len(words), step)`, append `words[start:start + size]`, and `break` once `start + size >= len(words)`.

</details>

<details><summary>Hint 2</summary>

IDF: `df` counts chunks containing each term; `idf[t] = math.log((1 + N) / (1 + df[t])) + 1`. Build each vector as a dict term → count * idf, then divide by its length.

</details>

<details><summary>Hint 3</summary>

Cited numbers: `{int(n) for n in re.findall(r"\[(\d+)\]", reply)}`; grounded if non-empty and all between 1 and the number of passages.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_chunking` | Advance by `size - overlap` and stop after the chunk that reaches the last word. |
| `test_retrieve_ranking` | Use smoothed IDF from the chunks, L2-normalise, and rank by cosine with index as tie-break. |
| `test_retrieve_scores_are_cosines` | Chunks sharing no query term score exactly 0 and keep index order. |
| `test_prompt` | Match the prompt text exactly, numbering passages from 1. |
| `test_answer_grounded` | Call the model exactly once with the prompt built from the retrieved chunks, best first. |
| `test_answer_ungrounded` | An answer is grounded only if it cites something and every citation is in range. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Chunking advances by `size - overlap` and stops after the window that reaches the end, so no
trailing chunk is a subset of the previous one. Retrieval builds smoothed-IDF weights from the
chunks only, normalises every vector, and ranks by dot product (cosine) with a deterministic
tie-break. The pipeline makes exactly one model call and checks citations against the numbered
passages it actually provided.

## References

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis et al. (`S097`)
- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
