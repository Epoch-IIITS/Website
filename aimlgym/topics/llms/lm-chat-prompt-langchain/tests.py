"""Tests for LM-17 Chat Prompts and Messages with LangChain.

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


class TestChatPrompt(unittest.TestCase):
    def test_input_variables(self):
        self.assertEqual(sorted(S.make_tutor_prompt().input_variables), ["history", "max_words", "question", "subject"])

    def test_message_order_and_content(self):
        msgs = S.format_chat(S.make_tutor_prompt(), "Python", 30, [("human", "Hi"), ("ai", "Hello!")], "What is a list?")
        self.assertEqual([t for t, _ in msgs], ["system", "human", "ai", "human"])
        self.assertEqual(msgs[0][1], "You are a tutor for Python. Answer in at most 30 words.")
        self.assertEqual(msgs[-1][1], "What is a list?")

    def test_empty_history(self):
        msgs = S.format_chat(S.make_tutor_prompt(), "SQL", 10, [], "Explain JOIN.")
        self.assertEqual([t for t, _ in msgs], ["system", "human"])

    def test_braces_in_values_are_text(self):
        msgs = S.format_chat(S.make_tutor_prompt(), "Python", 20, [], "What does {x} mean in f'{x}'?")
        self.assertEqual(msgs[-1][1], "What does {x} mean in f'{x}'?")

    def test_chain_with_fake_model(self):
        model = FakeListChatModel(responses=["A list is mutable.", "Tuples are not."])
        prompt = S.make_tutor_prompt()
        self.assertEqual(S.ask(prompt, model, "Python", 30, [], "Lists?"), "A list is mutable.")
        self.assertEqual(S.ask(prompt, model, "Python", 30, [], "Tuples?"), "Tuples are not.")

    def test_invalid_role(self):
        with self.assertRaises(ValueError):
            S.format_chat(S.make_tutor_prompt(), "Python", 30, [("system", "x")], "q")


if __name__ == "__main__":
    unittest.main()
