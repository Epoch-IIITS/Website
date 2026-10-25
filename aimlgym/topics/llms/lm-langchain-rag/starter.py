import math
import re

from langchain_core.embeddings import Embeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore


class KeywordEmbeddings(Embeddings):
    def __init__(self, vocabulary):
        # TODO
        pass

    def embed_documents(self, texts):
        # TODO
        pass

    def embed_query(self, text):
        # TODO
        pass


def build_store(docs, vocabulary):
    # TODO
    pass


def rag_answer(store, model, question, k=2):
    # TODO
    pass
