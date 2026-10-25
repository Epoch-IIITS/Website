# Retrieval-Augmented Generation with LangChain

## Learning outcomes

After this lesson you can:

- Implement the Embeddings interface and index documents in InMemoryVectorStore
- Retrieve context for a question and build a grounded prompt with source ids
- Check that an answer cites only the retrieved sources

## Intuition
A language model knows only what it was trained on. Retrieval-augmented generation (RAG) first finds
the passages relevant to a question in your own documents, then asks the model to answer **from those
passages**, citing them. Checking the citations catches answers that are not supported by what was
retrieved.

## Precise explanation
1. **Embeddings** turn text into vectors. In LangChain any class with `embed_documents(texts)` and
   `embed_query(text)` is an `Embeddings`. Real systems use neural sentence embeddings; here a keyword
   count vector over a fixed vocabulary, L2-normalised, keeps everything offline and deterministic.
2. **Vector store**: `InMemoryVectorStore(embedding)`; `add_texts(texts, ids=ids)`;
   `similarity_search(question, k)` returns the k most similar `Document`s (with `.id` and
   `.page_content`) by cosine similarity.
3. **Prompt**: put the retrieved passages into the system message, each prefixed with its id:
   `[faq-2] Submissions are graded on the VPS.` and instruct the model to answer only from them and
   cite ids in brackets.
4. **Check**: extract `[id]` citations from the answer; the answer is *grounded* if it cites at least
   one source and every cited id was retrieved.

## Worked example
Documents faq-1 "Run checks visible tests in the browser", faq-2 "Submit grades all tests on the
server", faq-3 "Progress counts passed problems". The question "how are tests graded on submit" retrieves
faq-2 first. An answer "Submit runs every test on the server [faq-2]." is grounded; one citing [faq-9]
is not.

## What the library does inside
The vector store keeps the vectors and ranks them with cosine similarity — your TF-IDF search in
NL-10 and the pipeline of LM-21 (the optional deep dive after this step),
behind interfaces that let you swap in a real embedding model and database.

## Common mistakes
* Retrieving too few passages (the answer is missing) or too many (the prompt fills with noise).
* Not giving passages ids, so citations cannot be checked.
* Trusting fluent answers that cite nothing.

## Why this matters
Most production LLM applications — documentation assistants, support bots, the course-FAQ project idea
after this step — are RAG systems.

## References

- [langchain-core vector stores reference](https://reference.langchain.com/python/langchain-core/vectorstores) — LangChain (`S133`)
- [Messages (LangChain docs)](https://docs.langchain.com/oss/python/langchain/messages) — LangChain (`S130`)
