"""Tests for LM-20 Retrieval-Augmented Generation with LangChain.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import importlib
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = importlib.import_module(os.environ.get("AIMLGYM_TARGET", "solution"))


from langchain_core.language_models.fake_chat_models import FakeListChatModel

DOCS = {
    "faq-1": "Run checks visible tests in the browser",
    "faq-2": "Submit grades all tests on the server",
    "faq-3": "Progress counts passed problems",
}
VOCAB = ["run", "visible", "tests", "browser", "submit", "grades", "server", "progress", "passed", "problems"]


class TestRag(unittest.TestCase):
    def test_embeddings(self):
        emb = S.KeywordEmbeddings(["a", "b"])
        self.assertEqual(emb.embed_query("a a b"), [2 / 5 ** 0.5, 1 / 5 ** 0.5])
        self.assertEqual(emb.embed_query("zzz"), [0.0, 0.0])
        self.assertEqual(emb.embed_documents(["a", "b"]), [[1.0, 0.0], [0.0, 1.0]])

    def test_retrieval_order(self):
        store = S.build_store(DOCS, VOCAB)
        found = store.similarity_search("how does submit grade on the server", k=2)
        self.assertEqual(found[0].id, "faq-2")

    def test_grounded_answer(self):
        store = S.build_store(DOCS, VOCAB)
        model = FakeListChatModel(responses=["Submit runs every test on the server [faq-2]."])
        r = S.rag_answer(store, model, "how are tests graded on submit", k=2)
        self.assertEqual(r["retrieved"][0], "faq-2")
        self.assertEqual(r["cited"], ["faq-2"])
        self.assertTrue(r["grounded"])

    def test_ungrounded_citation(self):
        store = S.build_store(DOCS, VOCAB)
        r = S.rag_answer(store, FakeListChatModel(responses=["It is magic [faq-9]."]), "submit server", k=1)
        self.assertFalse(r["grounded"])
        self.assertEqual(r["cited"], ["faq-9"])

    def test_no_citation_not_grounded(self):
        store = S.build_store(DOCS, VOCAB)
        r = S.rag_answer(store, FakeListChatModel(responses=["I think so."]), "progress problems")
        self.assertEqual((r["cited"], r["grounded"]), ([], False))

    def test_repeated_citations_once(self):
        store = S.build_store(DOCS, VOCAB)
        reply = "Visible tests [faq-1] run in the browser [faq-1]; submit uses the server [faq-2]."
        r = S.rag_answer(store, FakeListChatModel(responses=[reply]), "visible tests browser submit server", k=3)
        self.assertEqual(r["cited"], ["faq-1", "faq-2"])
        self.assertTrue(r["grounded"])


if __name__ == "__main__":
    unittest.main()
