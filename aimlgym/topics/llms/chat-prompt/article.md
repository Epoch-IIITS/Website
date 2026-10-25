# Chat Prompt Templates

## Learning outcomes

After this lesson you can:

- Render a list of role-tagged messages into the single string a chat model reads
- Validate message roles and order
- Fill prompt templates and detect missing or unused fields
- Quote untrusted documents so they cannot close their own delimiters

## Intuition
A chat model is still a next-token predictor. Before it sees a conversation, the list of
messages — system instructions, user turns, assistant turns — is **rendered** into one string
with special markers between roles. The model was trained on one exact format; using a different
one quietly degrades its answers. Templates also separate *instructions* from *data*, which
matters when the data is untrusted.

## Precise explanation
**Messages** are dicts `{"role": ..., "content": ...}` with roles `system` (optional, first
only), `user` and `assistant`.

A simple template (design choice for this course; each model family defines its own):
```
<|system|>
You are helpful.<|end|>
<|user|>
Hi<|end|>
<|assistant|>
```
Each message is `<|role|>\n` + content + `<|end|>\n`. With **generation prompt** on, the text ends
with `<|assistant|>\n`, telling the model it is its turn.

**Templates with fields**: `"Summarise {topic} for {audience}"` filled with values. Report missing
fields clearly, and treat extra values as a bug (often a typo in a field name).
`string.Formatter().parse(template)` lists the field names.

**Untrusted text**: a retrieved web page might contain "Ignore previous instructions...". Put it
inside explicit delimiters such as `<document> ... </document>`, tell the model that content
inside is data, and make sure the document cannot contain the closing tag itself (escape `<` in
any `<document>`/`</document>` it contains). Delimiting reduces, but does not eliminate, prompt
injection; tools must still enforce permissions (AG-19).

## Worked example
`render_chat([{"role": "user", "content": "Hi"}])` →
`"<|user|>\nHi<|end|>\n<|assistant|>\n"`.

## Common mistakes
* Adding the generation prompt during training data preparation (or forgetting it at inference).
* Allowing a system message in the middle of a conversation when the template does not support it.
* Building prompts with `+` from user input without delimiting it.

## Why this matters
Every LLM application, including RAG (LM-21) and agents, constructs prompts this way.

## Library implementation

Hugging Face tokenisers implement chat formatting as `tokenizer.apply_chat_template(messages,
add_generation_prompt=True, tokenize=False)`, using a Jinja template stored with each model, so
every model family gets its own markers. Python's `string.Template` and `str.format` handle field
substitution. Model-specific templates need a downloaded tokenizer, so they are not part of the
graded tests.

## References

- [Chat templates (Transformers docs)](https://huggingface.co/docs/transformers/main/en/chat_templating) — Hugging Face (`S098`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
