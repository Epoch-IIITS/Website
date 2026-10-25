# Retrieval-Augmented Generation

## Learning outcomes

After this lesson you can:

- Split documents into overlapping chunks
- Retrieve the most relevant chunks with TF-IDF cosine similarity
- Build a prompt that numbers its sources and asks for citations
- Check that a model's answer cites only retrieved sources, using a scripted model

## Intuition
A language model only knows what was in its training data. **Retrieval-augmented generation
(RAG)** looks up relevant passages from your own documents first and puts them in the prompt, so
the model can answer from them — and cite them, so a reader can check the answer.

## Precise explanation
Pipeline: **chunk → index → retrieve → prompt → generate → check**.

1. **Chunking**: split documents into windows of `size` words that overlap by `overlap` words,
   so a sentence cut at a boundary still appears whole in one chunk. Window starts are
   `0, size − overlap, 2(size − overlap), ...`; stop once a window reaches the end.
2. **Retrieval**: score each chunk against the query. Here: TF-IDF vectors
   (NL-09) with the smoothed IDF $\ln\frac{1 + N}{1 + df} + 1$, L2-normalised, scored by cosine
   similarity (NL-11). Real systems often use dense embeddings instead; the
   pipeline is the same.
3. **Prompt**: number the passages `[1] ...`, `[2] ...`, and instruct the model to answer only
   from them and cite numbers like `[1]`.
4. **Generate**: call the model. In tests the "model" is a scripted function, so behaviour is
   deterministic and no API is needed.
5. **Check**: extract cited numbers with a regex (NL-01). An answer is **grounded** here
   if it cites at least one source and every cited number refers to a retrieved passage. This is
   a necessary check, not proof the answer is faithful.

## Worked example
Chunks about "Paris is the capital of France" and "Bananas are yellow": the query "capital of
France" retrieves the first. The prompt shows `[1] Paris is the capital of France`; a reply
`"Paris [1]"` is grounded, `"Paris [3]"` is not.

## Common mistakes
* Chunks with no overlap that split the key sentence.
* Fitting IDF on the query plus chunks (the index is built from chunks only).
* Trusting citations without checking they exist.
* Putting retrieved text where instructions go, without delimiters (LM-18).

## Why this matters
RAG is the most common way LLMs are applied to private documents, and the same retrieve-then-act
loop appears in agents (AG-06).

## Library implementation

scikit-learn's `TfidfVectorizer` (defaults: raw counts, smoothed IDF $\ln\frac{1+N}{1+df}+1$, L2
normalisation) produces the same vectors when given the same tokeniser, and `linear_kernel` gives
the cosine scores. Frameworks such as LangChain or LlamaIndex wrap the full chunk → retrieve →
prompt pipeline. The test below checks your scores against scikit-learn when it is installed.

## References

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis et al. (`S097`)
- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
