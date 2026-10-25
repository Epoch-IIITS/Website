# Chat Prompts and Messages with LangChain

## Learning outcomes

After this lesson you can:

- Build chat prompts with ChatPromptTemplate and MessagesPlaceholder
- Represent conversations as SystemMessage, HumanMessage and AIMessage objects
- Compose prompt | model | output parser chains and test them with a fake chat model

## Intuition
Chat models take a list of **messages**, each with a role: the system message sets the rules, human
messages are the user's turns, AI messages are the model's earlier replies. Writing those lists by
hand gets repetitive; a **prompt template** fills in the variable parts and slots the conversation
history in the right place. LangChain also lets you swap a real model for a fake one in tests.

## Precise explanation
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a tutor for {subject}. Answer in at most {max_words} words."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
value = prompt.invoke({"subject": "Python", "max_words": 50, "history": [...], "question": "..."})
value.to_messages()             # [SystemMessage, ..., HumanMessage]
chain = prompt | model | StrOutputParser()
chain.invoke({...})             # the model's reply as a string
```

* Each message has `.type` (`"system"`, `"human"`, `"ai"`) and `.content`.
* `{name}` in a template is a variable; literal braces are written `{{` and `}}`. Variable **values**
  are inserted as plain text — braces inside a question are not interpreted.
* `prompt.input_variables` lists the variables the template needs.
* `|` composes **runnables**: the prompt's output goes to the model, the model's message to the parser.
* `FakeListChatModel(responses=[...])` returns its responses in order — deterministic, offline tests.
  A real provider (OpenAI, Anthropic, a local Ollama model) drops in with the same interface.

## Worked example
With subject "Python", 30 words and one earlier exchange, the prompt produces four messages: system,
human (earlier question), ai (earlier answer), human (new question). Piped into
`FakeListChatModel(responses=["A list is mutable."])`, the chain returns "A list is mutable."

## What the library does inside
It builds the role/content list that you assembled with a chat template in LM-18 (the
optional deep dive after this step); the model wrapper converts it to the provider's format.

## Common mistakes
* Putting the history into the system message as one long string instead of real messages.
* Forgetting a variable, which raises a `KeyError` when the prompt is invoked.
* Testing with a real, paid model where a fake one would make the test deterministic.

## Why this matters
Every LLM application — chatbots, RAG, agents — is built from prompts, messages and chains like these.

## References

- [Messages (LangChain docs)](https://docs.langchain.com/oss/python/langchain/messages) — LangChain (`S130`)
- [langchain-core prompts reference](https://reference.langchain.com/python/langchain-core/prompts) — LangChain (`S132`)
