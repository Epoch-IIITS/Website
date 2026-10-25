r"""Reference solution for LM-17 Chat Prompts and Messages with LangChain.

The template fixes the structure; the placeholder inserts real message objects for the history.
Converting the role pairs once keeps both functions consistent, and the chain passes the formatted
messages to whichever chat model it is given.
"""
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

ROLES = {"human": HumanMessage, "ai": AIMessage}


def make_tutor_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are a tutor for {subject}. Answer in at most {max_words} words."),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ])


def _inputs(subject, max_words, history, question):
    messages = []
    for role, text in history:
        if role not in ROLES:
            raise ValueError("history roles must be 'human' or 'ai'")
        messages.append(ROLES[role](content=text))
    return {"subject": subject, "max_words": max_words, "history": messages, "question": question}


def format_chat(prompt, subject, max_words, history, question):
    value = prompt.invoke(_inputs(subject, max_words, history, question))
    return [(m.type, m.content) for m in value.to_messages()]


def ask(prompt, model, subject, max_words, history, question):
    chain = prompt | model | StrOutputParser()
    return chain.invoke(_inputs(subject, max_words, history, question))
