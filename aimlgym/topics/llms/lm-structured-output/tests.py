"""Tests for LM-19 Structured Output with Pydantic and Retries.

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


from langchain_core.exceptions import OutputParserException
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.output_parsers import PydanticOutputParser

SEEN = []


class RecordingModel(FakeListChatModel):
    def _call(self, messages, stop=None, run_manager=None, **kwargs):
        SEEN.append(list(messages))
        return super()._call(messages, stop=stop, run_manager=run_manager, **kwargs)


GOOD = '{"answer": "4", "confidence": 0.95, "sources": [1]}'


class TestStructuredOutput(unittest.TestCase):
    def test_valid_first_time(self):
        answer, attempts = S.ask_structured(FakeListChatModel(responses=[GOOD]), "2 + 2?")
        self.assertEqual((answer.answer, answer.confidence, answer.sources, attempts), ("4", 0.95, [1], 1))

    def test_retry_after_prose(self):
        model = FakeListChatModel(responses=["Sure! The answer is 4.", GOOD])
        answer, attempts = S.ask_structured(model, "2 + 2?")
        self.assertEqual((answer.answer, attempts), ("4", 2))

    def test_out_of_range_is_invalid(self):
        model = FakeListChatModel(responses=['{"answer": "4", "confidence": 1.5}', '{"answer": "4", "confidence": 0.5}'])
        answer, attempts = S.ask_structured(model, "2 + 2?")
        self.assertEqual((answer.confidence, answer.sources, attempts), (0.5, [], 2))

    def test_gives_up(self):
        model = FakeListChatModel(responses=["no", "still no", "nope", "never"])
        with self.assertRaises(OutputParserException):
            S.ask_structured(model, "2 + 2?", max_retries=2)

    def test_messages_and_feedback(self):
        SEEN.clear()
        S.ask_structured(RecordingModel(responses=["oops", "```json\n" + GOOD + "\n```"]), "2 + 2?")
        first, second = SEEN
        self.assertEqual([m.type for m in first], ["system", "human"])
        self.assertIn("confidence", first[0].content)
        self.assertEqual([m.type for m in second], ["system", "human", "ai", "human"])
        self.assertIn("could not be parsed", second[-1].content)

    def test_answer_model(self):
        parser = PydanticOutputParser(pydantic_object=S.Answer)
        self.assertEqual(parser.parse('{"answer": "x", "confidence": 0}').sources, [])
        with self.assertRaises(OutputParserException):
            parser.parse('{"answer": "", "confidence": 0.2}')


if __name__ == "__main__":
    unittest.main()
