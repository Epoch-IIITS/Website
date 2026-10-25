# LM-20 · Retrieval-Augmented Generation with LangChain

**Topic:** Large Language Models · **Difficulty:** advanced · **Allowed packages:** langchain-core

**Builds on:** LM-19 Structured Output with Pydantic and Retries, NL-10 Search with TfidfVectorizer and Cosine Similarity

Read the lesson first: [article.md](article.md)

## Task

1. `class KeywordEmbeddings(Embeddings)` with `__init__(self, vocabulary)`: `embed_query(text)` counts
   how often each vocabulary word appears among `re.findall(r"[a-z]+", text.lower())`, L2-normalises the
   counts (a zero vector stays zero) and returns a list of floats; `embed_documents(texts)` maps
   `embed_query` over the texts.
2. `build_store(docs, vocabulary)` takes a dict `{id: text}` and returns an `InMemoryVectorStore`
   with the texts added under their ids.
3. `rag_answer(store, model, question, k=2)` retrieves `k` documents, builds a
   `ChatPromptTemplate` with system message
   `"Answer only from the context and cite sources as [id].\n\nContext:\n{context}"` (context lines
   `"[id] text"`) and human message `"{question}"`, runs `prompt | model | StrOutputParser()` and returns
   `{"answer": str, "retrieved": [ids], "cited": [ids in order of first appearance], "grounded": bool}`.

## Hints

<details><summary>Hint 1</summary>

Count words with a dict over the vocabulary; the norm is `math.sqrt(sum(v * v for v in counts))`.

</details>

<details><summary>Hint 2</summary>

`store = InMemoryVectorStore(KeywordEmbeddings(vocabulary))`; `store.add_texts(list(docs.values()), ids=list(docs))`.

</details>

<details><summary>Hint 3</summary>

Citations: `re.findall(r"\[([\w-]+)\]", answer)`, keeping the first occurrence of each.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_embeddings` | Count vocabulary words, L2-normalise, and keep an all-zero vector as zeros. |
| `test_retrieval_order` | Add the texts with ids=list(docs) and search with similarity_search. |
| `test_grounded_answer` | Grounded means at least one citation and every cited id was retrieved. |
| `test_repeated_citations_once` | List each cited id once, in order of first appearance. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The embedding class satisfies LangChain's interface, so the in-memory store can index and search with
it. Retrieved passages are labelled with their ids in the prompt; after the model answers, the cited
ids are compared with the retrieved ones to decide whether the answer is grounded.

## References

- [langchain-core vector stores reference](https://reference.langchain.com/python/langchain-core/vectorstores) — LangChain (`S133`)
- [Messages (LangChain docs)](https://docs.langchain.com/oss/python/langchain/messages) — LangChain (`S130`)
