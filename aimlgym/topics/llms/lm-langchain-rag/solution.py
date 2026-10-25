r"""Reference solution for LM-20 Retrieval-Augmented Generation with LangChain.

The embedding class satisfies LangChain's interface, so the in-memory store can index and search with
it. Retrieved passages are labelled with their ids in the prompt; after the model answers, the cited
ids are compared with the retrieved ones to decide whether the answer is grounded.
"""
import math
import re

from langchain_core.embeddings import Embeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Answer only from the context and cite sources as [id].\n\nContext:\n{context}"),
    ("human", "{question}"),
])


class KeywordEmbeddings(Embeddings):
    def __init__(self, vocabulary):
        self.vocabulary = list(vocabulary)

    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text):
        words = re.findall(r"[a-z]+", text.lower())
        counts = [float(words.count(w)) for w in self.vocabulary]
        norm = math.sqrt(sum(v * v for v in counts))
        return [v / norm for v in counts] if norm else counts


def build_store(docs, vocabulary):
    store = InMemoryVectorStore(KeywordEmbeddings(vocabulary))
    store.add_texts(list(docs.values()), ids=list(docs))
    return store


def rag_answer(store, model, question, k=2):
    found = store.similarity_search(question, k=k)
    context = "\n".join(f"[{d.id}] {d.page_content}" for d in found)
    answer = (PROMPT | model | StrOutputParser()).invoke({"context": context, "question": question})
    cited = []
    for ref in re.findall(r"\[([\w-]+)\]", answer):
        if ref not in cited:
            cited.append(ref)
    retrieved = [d.id for d in found]
    return {"answer": answer, "retrieved": retrieved, "cited": cited,
            "grounded": bool(cited) and set(cited) <= set(retrieved)}
