r"""Reference solution for LM-18 Chat Prompt Templates.

Rendering validates each message while building the string, so a malformed conversation never
reaches the model. Parsing splits on the end marker and recognises each role prefix, which makes
the format testable as a round trip. Template checking compares the parsed field names with the
supplied keys before formatting. Escaping both tag forms means the only real closing tag is the
one added by `quote_document`.
"""
import string

ROLES = ("system", "user", "assistant")


def render_chat(messages, add_generation_prompt=True):
    if not messages:
        raise ValueError("no messages")
    parts = []
    for i, m in enumerate(messages):
        role = m["role"]
        if role not in ROLES:
            raise ValueError(f"unknown role {role!r}")
        if role == "system" and i > 0:
            raise ValueError("system message must come first")
        parts.append(f"<|{role}|>\n{m['content']}<|end|>\n")
    if add_generation_prompt:
        parts.append("<|assistant|>\n")
    return "".join(parts)


def parse_chat(text):
    if not text.endswith("<|end|>\n"):
        raise ValueError("text must end with <|end|>")
    messages = []
    for chunk in text.split("<|end|>\n")[:-1]:
        for role in ROLES:
            prefix = f"<|{role}|>\n"
            if chunk.startswith(prefix):
                messages.append({"role": role, "content": chunk[len(prefix):]})
                break
        else:
            raise ValueError(f"bad chunk {chunk[:20]!r}")
    return messages


def fill_template(template, values):
    fields = {name for _, name, _, _ in string.Formatter().parse(template) if name}
    missing = sorted(fields - set(values))
    unused = sorted(set(values) - fields)
    if missing:
        raise KeyError(f"missing fields: {', '.join(missing)}")
    if unused:
        raise ValueError(f"unused values: {', '.join(unused)}")
    return template.format(**values)


def quote_document(doc):
    safe = doc.replace("</document>", "&lt;/document>").replace("<document>", "&lt;document>")
    return "<document>\n" + safe + "\n</document>"
