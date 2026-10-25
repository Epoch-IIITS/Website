# LM-18 · Chat Prompt Templates

**Topic:** Large Language Models · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** LM-01 Vocabularies and Token IDs

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `render_chat(messages, add_generation_prompt=True)` using the template above. Raise
   `ValueError` for an unknown role, a `system` message that is not first, or an empty list.
2. `parse_chat(text)` — the inverse for text produced with `add_generation_prompt=False`:
   return the list of message dicts (raise `ValueError` if the text is not in this format).
3. `fill_template(template, values)` — `template.format(**values)`, but first raise `KeyError`
   naming the missing fields (sorted, in one message) and `ValueError` naming unused keys.
4. `quote_document(doc)` → `"<document>\n" + safe + "\n</document>"` where `safe` is `doc` with
   every `<document>` replaced by `&lt;document>` and every `</document>` by `&lt;/document>`.

## Hints

<details><summary>Hint 1</summary>

Validate while looping: `if m["role"] == "system" and i > 0: raise ValueError(...)`; build parts `f"<|{role}|>\n{content}<|end|>\n"`.

</details>

<details><summary>Hint 2</summary>

Parse by splitting on `"<|end|>\n"`; each non-empty chunk must start with `<|role|>\n` for a known role.

</details>

<details><summary>Hint 3</summary>

`fields = {name for _, name, _, _ in string.Formatter().parse(template) if name}`; compare with `set(values)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_render` | Each message is `<|role|>\n` + content + `<|end|>\n`; add `<|assistant|>\n` only with the generation prompt. |
| `test_validation` | Reject empty lists, unknown roles and a system message after the first position. |
| `test_round_trip` | Split on `<|end|>\n` and strip the role prefix from each chunk. |
| `test_template_errors` | Find field names with `string.Formatter().parse`; report missing names sorted and unused keys. |
| `test_quote_document` | Escape both `<document>` and `</document>` inside the document before wrapping it. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Rendering validates each message while building the string, so a malformed conversation never
reaches the model. Parsing splits on the end marker and recognises each role prefix, which makes
the format testable as a round trip. Template checking compares the parsed field names with the
supplied keys before formatting. Escaping both tag forms means the only real closing tag is the
one added by `quote_document`.

## References

- [Chat templates (Transformers docs)](https://huggingface.co/docs/transformers/main/en/chat_templating) — Hugging Face (`S098`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
- [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic (`S037`)
