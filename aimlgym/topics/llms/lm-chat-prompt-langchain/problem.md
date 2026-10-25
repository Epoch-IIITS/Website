# LM-17 · Chat Prompts and Messages with LangChain

**Topic:** Large Language Models · **Difficulty:** advanced · **Allowed packages:** langchain-core

**Builds on:** LM-16 A Tiny GPT in PyTorch

Read the lesson first: [article.md](article.md)

## Task

1. `make_tutor_prompt()` returns the `ChatPromptTemplate` from the lesson (system message, a
   `MessagesPlaceholder("history")`, then `("human", "{question}")`).
2. `format_chat(prompt, subject, max_words, history, question)` invokes the prompt and returns the
   messages as `(type, content)` pairs. `history` is a list of `(role, text)` pairs with role
   `"human"` or `"ai"`, converted to `HumanMessage` / `AIMessage`; any other role raises `ValueError`.
3. `ask(prompt, model, subject, max_words, history, question)` runs
   `prompt | model | StrOutputParser()` with the same inputs and returns the string.

## Hints

<details><summary>Hint 1</summary>

`ChatPromptTemplate.from_messages([("system", "..."), MessagesPlaceholder("history"), ("human", "{question}")])`.

</details>

<details><summary>Hint 2</summary>

Write a helper that turns the history pairs into message objects and builds the input dict.

</details>

<details><summary>Hint 3</summary>

`[(m.type, m.content) for m in prompt.invoke(inputs).to_messages()]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_input_variables` | The template needs subject, max_words, history and question. |
| `test_message_order_and_content` | System message, then the history placeholder, then the human question. |
| `test_chain_with_fake_model` | Compose prompt | model | StrOutputParser() and invoke it. |
| `test_invalid_role` | Only 'human' and 'ai' roles are allowed in the history. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The template fixes the structure; the placeholder inserts real message objects for the history.
Converting the role pairs once keeps both functions consistent, and the chain passes the formatted
messages to whichever chat model it is given.

## References

- [Messages (LangChain docs)](https://docs.langchain.com/oss/python/langchain/messages) — LangChain (`S130`)
- [langchain-core prompts reference](https://reference.langchain.com/python/langchain-core/prompts) — LangChain (`S132`)
