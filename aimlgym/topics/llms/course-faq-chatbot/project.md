# LM-P2 · Project idea: Course FAQ Chatbot

**Topic:** Large Language Models · ungraded

## Brief

Build a chatbot that answers questions about this course — what a step covers, how Run and Submit
differ, which step to do next — using RAG over the course's lesson text, and that cites the lessons it
used. It should say "I don't know" when the answer is not in the material.

## You will use

- NL-10 Search with TfidfVectorizer and Cosine Similarity
- LM-17 Chat Prompts and Messages with LangChain
- LM-19 Structured Output with Pydantic and Retries
- LM-20 Retrieval-Augmented Generation with LangChain

## Milestones

1. Split lesson texts into passages of a few paragraphs, each with an id and its lesson title.
2. Index the passages with TF-IDF or a sentence-embedding model and test retrieval on 20 questions.
3. Connect a chat model (a local model through Ollama or a hosted API) with a prompt that requires citations.
4. Return structured answers (answer, cited ids, confidence) and reject ungrounded ones.
5. Build a tiny evaluation set of question/expected-lesson pairs and report retrieval and answer accuracy.

## Stretch goals

- Keep conversation history so follow-up questions work.
- Serve it with FastAPI and add a chat box to a web page.
- Log questions the bot could not answer to find gaps in the lessons.

## Data

Use the lesson articles of this course (each step's lesson) or notes from your own classes. For a local
model without API keys, install [Ollama](https://ollama.com/) and pull a small model.

## Run it yourself

```bash
pip install langchain-core langchain-ollama scikit-learn
python faq_bot.py
```
