"""Large language models with PyTorch and LangChain (library revision, Phase 4).

Library steps are followed by the from-scratch versions they replace on the required path, kept as
optional deep dives: [[transformer-block]], [[chat-prompt]], [[rag-pipeline]].
"""

PROBLEMS = [
# ---------------------------------------------------------------- lm-transformer-module
{
"slug": "lm-transformer-module", "title": "A Transformer Block as nn.Module",
"difficulty": "intermediate", "prereqs": ["multi-head-attention", "torch-mlp-module"], "packages": ["torch"],
"objectives": ["Build a pre-norm transformer block from nn.MultiheadAttention, LayerNorm and an MLP",
               "Apply a causal attention mask so positions cannot see the future",
               "Check the block against nn.TransformerEncoderLayer"],
"tags": ["pytorch", "transformer", "attention", "layer-norm", "residual-connections"],
"sources": ["S129", "S128"], "entry": "class TransformerBlock(nn.Module)",
"article": r'''
# A Transformer Block as nn.Module

## Intuition
A transformer is a stack of identical blocks. Each block lets every position gather information
from the others (attention) and then transforms each position on its own (an MLP). Residual
connections add each sub-layer's output to its input, and layer normalisation keeps the scale
stable — so blocks can be stacked dozens deep.

## Precise explanation
The **pre-norm** block used by GPT-style models:

```python
h = self.norm1(x)
a, _ = self.self_attn(h, h, h, attn_mask=mask, need_weights=False)
x = x + a                                                     # residual
x = x + self.linear2(F.gelu(self.linear1(self.norm2(x))))     # MLP with a 4× wider hidden layer
```

* `nn.MultiheadAttention(d_model, n_heads, batch_first=True)` takes (batch, time, d_model) tensors and
  holds the query/key/value projections for all heads in `in_proj_weight`, plus `out_proj`.
* A **causal** mask is a boolean (T, T) tensor that is `True` above the diagonal:
  `torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)`. `True` means "may not attend".
* `nn.LayerNorm(d_model)` normalises each position's vector; GELU is the usual activation.
* `nn.TransformerEncoderLayer(d_model, n_heads, 4 * d_model, dropout=0.0, activation="gelu",
  batch_first=True, norm_first=True)` is the same block; with the attribute names above its
  `state_dict` loads into yours.

## Worked example
With d_model = 16 and 2 heads, a (2, 5, 16) input gives a (2, 5, 16) output. Changing token 4 changes
the outputs at position 4 only — positions 0–3 cannot see it through the causal mask.

## What the library does inside
`nn.MultiheadAttention` performs the projections, scaled dot products, masking and head
concatenation that you wrote in [[multi-head-attention]]; your NumPy [[transformer-block]] (the
optional deep dive after this step) is the same computation without autograd.

## Common mistakes
* Forgetting `batch_first=True` and mixing up (time, batch) and (batch, time).
* A mask with `True` on the allowed positions (the meaning is reversed).
* Post-norm ordering by accident (normalising after adding the residual).

## Why this matters
The tiny GPT next stacks these blocks; large language models differ mostly in size.
''',
"statement": r'''
Write `class TransformerBlock(nn.Module)` with `__init__(self, d_model, n_heads)` creating exactly
these attributes:

* `self.norm1`, `self.norm2`: `nn.LayerNorm(d_model)`;
* `self.self_attn`: `nn.MultiheadAttention(d_model, n_heads, dropout=0.0, batch_first=True)`;
* `self.linear1`: `nn.Linear(d_model, 4 * d_model)`; `self.linear2`: `nn.Linear(4 * d_model, d_model)`.

`forward(self, x, causal=True)` computes the pre-norm block from the lesson with `F.gelu`, using the
causal mask when `causal` is true and no mask otherwise. Raise `ValueError` in `__init__` if
`d_model` is not divisible by `n_heads`.
''',
"starter": r'''
import torch
import torch.nn.functional as F
from torch import nn


class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        # TODO

    def forward(self, x, causal=True):
        # TODO
        pass
''',
"hints": [
    "Check `d_model % n_heads == 0` before creating the layers.",
    "`T = x.shape[1]`; `mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), diagonal=1) if causal else None`.",
    "Attention returns `(output, weights)`; add the output to x, then add the MLP of `norm2(x)`.",
],
"solution": r'''
import torch
import torch.nn.functional as F
from torch import nn


class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        if d_model % n_heads != 0:
            raise ValueError("d_model must be divisible by n_heads")
        self.norm1 = nn.LayerNorm(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, n_heads, dropout=0.0, batch_first=True)
        self.norm2 = nn.LayerNorm(d_model)
        self.linear1 = nn.Linear(d_model, 4 * d_model)
        self.linear2 = nn.Linear(4 * d_model, d_model)

    def forward(self, x, causal=True):
        T = x.shape[1]
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), diagonal=1) if causal else None
        h = self.norm1(x)
        a, _ = self.self_attn(h, h, h, attn_mask=mask, need_weights=False)
        x = x + a
        return x + self.linear2(F.gelu(self.linear1(self.norm2(x))))
''',
"explanation": r'''
Each sub-layer reads a normalised copy of the residual stream and adds its result back. The boolean
upper-triangular mask blocks attention to later positions. Using PyTorch's attribute names makes the
block weight-compatible with `nn.TransformerEncoderLayer` in pre-norm mode.
''',
"tests": r'''
import torch
from torch import nn


class TestTransformerBlock(unittest.TestCase):
    def test_shape(self):
        torch.manual_seed(0)
        block = S.TransformerBlock(16, 2)
        self.assertEqual(tuple(block(torch.randn(2, 5, 16)).shape), (2, 5, 16))

    def test_causal(self):
        torch.manual_seed(1)
        block = S.TransformerBlock(8, 2)
        x = torch.randn(1, 6, 8)
        y = x.clone(); y[0, 4] += torch.randn(8)
        a, b = block(x), block(y)
        self.assertTrue(torch.allclose(a[0, :4], b[0, :4], atol=1e-6))
        self.assertFalse(torch.allclose(a[0, 4], b[0, 4]))

    def test_non_causal_sees_everything(self):
        torch.manual_seed(2)
        block = S.TransformerBlock(8, 2)
        x = torch.randn(1, 4, 8)
        y = x.clone(); y[0, 3] += torch.randn(8)
        self.assertFalse(torch.allclose(block(x, causal=False)[0, 0], block(y, causal=False)[0, 0]))

    def test_matches_encoder_layer(self):
        torch.manual_seed(3)
        ref = nn.TransformerEncoderLayer(16, 4, 64, dropout=0.0, activation="gelu", batch_first=True, norm_first=True)
        block = S.TransformerBlock(16, 4)
        block.load_state_dict(ref.state_dict())
        x = torch.randn(3, 7, 16)
        mask = torch.triu(torch.ones(7, 7, dtype=torch.bool), diagonal=1)
        ref.train()
        self.assertTrue(torch.allclose(block(x), ref(x, src_mask=mask), atol=1e-5))

    def test_parameter_count(self):
        d = 32
        block = S.TransformerBlock(d, 4)
        expected = 2 * (2 * d) + (3 * d * d + 3 * d) + (d * d + d) + (d * 4 * d + 4 * d) + (4 * d * d + d)
        self.assertEqual(sum(p.numel() for p in block.parameters()), expected)

    def test_invalid_heads(self):
        with self.assertRaises(ValueError):
            S.TransformerBlock(10, 3)
''',
"feedback": [
    ("test_causal", "The mask is True above the diagonal: torch.triu(ones, diagonal=1)."),
    ("test_matches_encoder_layer", "Use pre-norm order, GELU and the attribute names norm1, self_attn, norm2, linear1, linear2."),
    ("test_parameter_count", "The MLP hidden layer is 4 × d_model wide."),
    ("test_invalid_heads", "Raise ValueError when d_model is not divisible by n_heads."),
],
},
# ---------------------------------------------------------------- lm-tiny-gpt
{
"slug": "lm-tiny-gpt", "title": "A Tiny GPT in PyTorch",
"difficulty": "advanced", "prereqs": ["kv-cache", "lm-transformer-module"], "packages": ["torch"],
"objectives": ["Assemble token and position embeddings, transformer blocks and an output head into a GPT",
               "Train it on character windows with next-token cross-entropy",
               "Generate text greedily with a context window"],
"tags": ["pytorch", "language-model", "gpt", "transformer", "text-generation"],
"sources": ["S128", "S129"], "entry": "class TinyGPT(nn.Module); train_tiny_gpt(text, context=16, steps=200, batch_size=32, lr=3e-3, seed=0); generate(model, stoi, itos, prompt, n_new)",
"article": r'''
# A Tiny GPT in PyTorch

## Intuition
A GPT reads a window of tokens and predicts, at every position, the next token. Train it on
windows of text with cross-entropy and it learns the patterns of that text; generate by repeatedly
predicting a token and appending it. A character-level model with one block, trained for a few
hundred steps on a CPU, already reproduces simple text.

## Precise explanation
```python
x = self.tok_emb(idx) + self.pos_emb(torch.arange(T))        # (B, T, d)
x = self.blocks(x, mask=causal_mask, is_causal=True)          # nn.TransformerEncoder, pre-norm layers
logits = self.head(self.ln_f(x))                              # (B, T, vocab)
loss = F.cross_entropy(logits.view(-1, V), targets.view(-1))  # targets = inputs shifted by one
```

* Training pairs come from random windows: `x = data[i:i+T]`, `y = data[i+1:i+T+1]`. Every position
  is a training example, so one window of 16 characters gives 16 predictions.
* Positions are learned with `nn.Embedding(context, d)`; the model cannot read more than `context`
  tokens, so generation crops the input to the last `context` tokens.
* The causal mask ([[lm-transformer-module]]) prevents position t from seeing tokens after t.
* Greedy generation takes the argmax of the last position's logits; [[top-k-top-p]] sampling gives
  more varied text.
* An untrained model has loss ≈ ln(V); a model that has learned repetitive text approaches 0.

## Worked example
Trained for 200 steps on "hello world. " repeated, the loss drops from about ln(9) ≈ 2.2 to below 0.2,
and greedy generation from "hello w" continues "orld. hello world".

## Common mistakes
* Targets not shifted by one, so the model learns to copy its input.
* Generating with prompts longer than the context without cropping.
* Forgetting `model.eval()` and `torch.no_grad()` while generating.

## Why this matters
This is the architecture of GPT-2 and its successors in miniature; scaling up the data, context and
number of blocks is most of the remaining difference. The poem-generator project idea trains it on
your own text.
''',
"statement": r'''
1. `class TinyGPT(nn.Module)` with `__init__(self, vocab_size, context, d_model=32, n_heads=2, n_layers=1)`
   storing `self.context`, `self.tok_emb = nn.Embedding(vocab_size, d_model)`,
   `self.pos_emb = nn.Embedding(context, d_model)`, `self.blocks = nn.TransformerEncoder(nn.TransformerEncoderLayer(d_model, n_heads, 4 * d_model, dropout=0.0, activation="gelu", batch_first=True, norm_first=True), n_layers, enable_nested_tensor=False)`,
   `self.ln_f = nn.LayerNorm(d_model)` and `self.head = nn.Linear(d_model, vocab_size)`.
   `forward(idx)` returns logits `(B, T, vocab)` using the causal mask
   `nn.Transformer.generate_square_subsequent_mask(T)` with `is_causal=True`.
2. `train_tiny_gpt(text, context=16, steps=200, batch_size=32, lr=3e-3, seed=0)`: vocabulary
   `chars = sorted(set(text))`; `torch.manual_seed(seed)`; model; AdamW; each step draws `batch_size`
   start positions with `torch.randint(len(data) - context - 1, (batch_size,), generator=g)`
   (`g = torch.Generator().manual_seed(seed)`). Return `(model, stoi, itos, losses)` with the model in
   `eval()` mode, `stoi` a dict and `itos` a list.
3. `generate(model, stoi, itos, prompt, n_new)` returns the prompt plus `n_new` greedily generated
   characters, feeding at most the last `model.context` characters. Raise `ValueError` for prompt
   characters outside the vocabulary.
''',
"starter": r'''
import torch
import torch.nn.functional as F
from torch import nn


class TinyGPT(nn.Module):
    def __init__(self, vocab_size, context, d_model=32, n_heads=2, n_layers=1):
        super().__init__()
        # TODO

    def forward(self, idx):
        # TODO
        pass


def train_tiny_gpt(text, context=16, steps=200, batch_size=32, lr=3e-3, seed=0):
    # TODO
    pass


def generate(model, stoi, itos, prompt, n_new):
    # TODO
    pass
''',
"hints": [
    "In forward: `T = idx.shape[1]`, add `self.pos_emb(torch.arange(T))` to the token embeddings, run the encoder with the mask, then `self.head(self.ln_f(x))`.",
    "Build a batch with `torch.stack([data[i:i + context] for i in ix])` and the targets shifted by one.",
    "Generation loop: crop `ids[-model.context:]`, take `logits[0, -1].argmax()`, append; use `torch.no_grad()`.",
],
"solution": r'''
import torch
import torch.nn.functional as F
from torch import nn


class TinyGPT(nn.Module):
    def __init__(self, vocab_size, context, d_model=32, n_heads=2, n_layers=1):
        super().__init__()
        self.context = context
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(context, d_model)
        layer = nn.TransformerEncoderLayer(d_model, n_heads, 4 * d_model, dropout=0.0, activation="gelu",
                                           batch_first=True, norm_first=True)
        self.blocks = nn.TransformerEncoder(layer, n_layers, enable_nested_tensor=False)
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size)

    def forward(self, idx):
        T = idx.shape[1]
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        mask = nn.Transformer.generate_square_subsequent_mask(T, device=idx.device)
        x = self.blocks(x, mask=mask, is_causal=True)
        return self.head(self.ln_f(x))


def train_tiny_gpt(text, context=16, steps=200, batch_size=32, lr=3e-3, seed=0):
    itos = sorted(set(text))
    stoi = {ch: i for i, ch in enumerate(itos)}
    data = torch.tensor([stoi[ch] for ch in text], dtype=torch.long)
    torch.manual_seed(seed)
    model = TinyGPT(len(itos), context)
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    g = torch.Generator().manual_seed(seed)
    losses = []
    model.train()
    for _ in range(steps):
        ix = torch.randint(len(data) - context - 1, (batch_size,), generator=g)
        x = torch.stack([data[i:i + context] for i in ix])
        y = torch.stack([data[i + 1:i + context + 1] for i in ix])
        logits = model(x)
        loss = F.cross_entropy(logits.view(-1, len(itos)), y.view(-1))
        opt.zero_grad()
        loss.backward()
        opt.step()
        losses.append(loss.item())
    model.eval()
    return model, stoi, itos, losses


def generate(model, stoi, itos, prompt, n_new):
    if any(ch not in stoi for ch in prompt):
        raise ValueError("prompt contains characters outside the vocabulary")
    ids = [stoi[ch] for ch in prompt]
    model.eval()
    with torch.no_grad():
        for _ in range(n_new):
            window = torch.tensor([ids[-model.context:]], dtype=torch.long)
            ids.append(int(model(window)[0, -1].argmax()))
    return "".join(itos[i] for i in ids)
''',
"explanation": r'''
Embeddings turn characters and positions into vectors, the causal encoder layers mix information from
earlier positions only, and the head scores every possible next character. Training samples random
windows and their one-step-shifted targets; greedy generation repeatedly appends the most likely
next character within the context window.
''',
"tests": r'''
import torch
from torch import nn

TEXT = "hello world. " * 40
TRAINED = []


def trained():
    """Train once and share the result, so each test reports its own failure."""
    if not TRAINED:
        TRAINED.append(S.train_tiny_gpt(TEXT, context=16, steps=200))
    return TRAINED[0]


class TestTinyGPT(unittest.TestCase):
    def test_loss_falls(self):
        losses = trained()[3]
        self.assertGreater(losses[0], 1.5)
        self.assertLess(sum(losses[-10:]) / 10, 0.3)

    def test_generates_pattern(self):
        model, stoi, itos, _ = trained()
        self.assertEqual(S.generate(model, stoi, itos, "hello w", 11), "hello world. hello")

    def test_vocab_and_mode(self):
        model, stoi, itos, _ = trained()
        self.assertEqual(itos, sorted(set(TEXT)))
        self.assertEqual(stoi["h"], itos.index("h"))
        self.assertFalse(model.training)

    def test_output_shape_and_causality(self):
        torch.manual_seed(0)
        model = S.TinyGPT(10, 8)
        idx = torch.randint(0, 10, (2, 8))
        out = model(idx)
        self.assertEqual(tuple(out.shape), (2, 8, 10))
        changed = idx.clone(); changed[:, 5] = (changed[:, 5] + 1) % 10
        self.assertTrue(torch.allclose(out[:, :5], model(changed)[:, :5], atol=1e-5))

    def test_long_prompt_is_cropped(self):
        model, stoi, itos, _ = trained()
        text = S.generate(model, stoi, itos, TEXT[:40], 3)
        self.assertEqual(len(text), 43)

    def test_unknown_prompt_character(self):
        with self.assertRaises(ValueError):
            model, stoi, itos, _ = trained()
            S.generate(model, stoi, itos, "HELLO", 2)
''',
"feedback": [
    ("test_loss_falls", "Targets are the inputs shifted by one; use cross-entropy over all positions."),
    ("test_generates_pattern", "Greedy generation takes argmax of the last position's logits."),
    ("test_output_shape_and_causality", "Pass the causal mask and is_causal=True to the encoder."),
    ("test_long_prompt_is_cropped", "Feed only the last model.context ids when generating."),
],
},
# ---------------------------------------------------------------- lm-chat-prompt-langchain
{
"slug": "lm-chat-prompt-langchain", "title": "Chat Prompts and Messages with LangChain",
"difficulty": "advanced", "prereqs": ["lm-tiny-gpt"], "packages": ["langchain-core"],
"objectives": ["Build chat prompts with ChatPromptTemplate and MessagesPlaceholder",
               "Represent conversations as SystemMessage, HumanMessage and AIMessage objects",
               "Compose prompt | model | output parser chains and test them with a fake chat model"],
"tags": ["langchain", "prompts", "chat-models", "messages"],
"sources": ["S130", "S132"], "entry": "make_tutor_prompt(); format_chat(prompt, subject, max_words, history, question); ask(prompt, model, subject, max_words, history, question)",
"article": r'''
# Chat Prompts and Messages with LangChain

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
It builds the role/content list that you assembled with a chat template in [[chat-prompt]] (the
optional deep dive after this step); the model wrapper converts it to the provider's format.

## Common mistakes
* Putting the history into the system message as one long string instead of real messages.
* Forgetting a variable, which raises a `KeyError` when the prompt is invoked.
* Testing with a real, paid model where a fake one would make the test deterministic.

## Why this matters
Every LLM application — chatbots, RAG, agents — is built from prompts, messages and chains like these.
''',
"statement": r'''
1. `make_tutor_prompt()` returns the `ChatPromptTemplate` from the lesson (system message, a
   `MessagesPlaceholder("history")`, then `("human", "{question}")`).
2. `format_chat(prompt, subject, max_words, history, question)` invokes the prompt and returns the
   messages as `(type, content)` pairs. `history` is a list of `(role, text)` pairs with role
   `"human"` or `"ai"`, converted to `HumanMessage` / `AIMessage`; any other role raises `ValueError`.
3. `ask(prompt, model, subject, max_words, history, question)` runs
   `prompt | model | StrOutputParser()` with the same inputs and returns the string.
''',
"starter": r'''
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def make_tutor_prompt():
    # TODO
    pass


def format_chat(prompt, subject, max_words, history, question):
    # TODO
    pass


def ask(prompt, model, subject, max_words, history, question):
    # TODO
    pass
''',
"hints": [
    "`ChatPromptTemplate.from_messages([(\"system\", \"...\"), MessagesPlaceholder(\"history\"), (\"human\", \"{question}\")])`.",
    "Write a helper that turns the history pairs into message objects and builds the input dict.",
    "`[(m.type, m.content) for m in prompt.invoke(inputs).to_messages()]`.",
],
"solution": r'''
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
''',
"explanation": r'''
The template fixes the structure; the placeholder inserts real message objects for the history.
Converting the role pairs once keeps both functions consistent, and the chain passes the formatted
messages to whichever chat model it is given.
''',
"tests": r'''
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
''',
"feedback": [
    ("test_input_variables", "The template needs subject, max_words, history and question."),
    ("test_message_order_and_content", "System message, then the history placeholder, then the human question."),
    ("test_chain_with_fake_model", "Compose prompt | model | StrOutputParser() and invoke it."),
    ("test_invalid_role", "Only 'human' and 'ai' roles are allowed in the history."),
],
},
# ---------------------------------------------------------------- lm-structured-output
{
"slug": "lm-structured-output", "title": "Structured Output with Pydantic and Retries",
"difficulty": "advanced", "prereqs": ["lm-chat-prompt-langchain"], "packages": ["langchain-core"],
"objectives": ["Describe the expected answer with a Pydantic model and format instructions",
               "Parse model replies with PydanticOutputParser and catch OutputParserException",
               "Retry with the error message when the reply is invalid"],
"tags": ["langchain", "structured-output", "pydantic", "output-parsing", "retries"],
"sources": ["S131", "S140"], "entry": "class Answer(BaseModel); build_messages(question, parser); ask_structured(model, question, max_retries=2)",
"article": r'''
# Structured Output with Pydantic and Retries

## Intuition
Programs need data, not prose: an answer, a confidence, a list of sources. Describe that shape with a
Pydantic model, tell the language model to reply in that JSON shape, and validate the reply. Models
sometimes break the format, so when parsing fails, show the model the error and ask again — a few
times at most.

## Precise explanation
```python
class Answer(BaseModel):
    answer: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    sources: list[int] = []

parser = PydanticOutputParser(pydantic_object=Answer)
parser.get_format_instructions()      # text with the JSON schema, to put in the prompt
parser.parse(reply.content)           # an Answer, or OutputParserException
```

* The parser accepts plain JSON or JSON inside a ```json fence, then validates it with Pydantic:
  wrong types, missing fields and out-of-range values all raise `OutputParserException`.
* Retry loop: keep the conversation, append the failed reply and a human message quoting the error,
  invoke again. Stop after a fixed number of retries and re-raise the last error.
* Many providers also offer native structured output (`model.with_structured_output(Answer)`);
  the validation-and-retry idea is the same.

## Worked example
Reply 1: "Sure! The answer is 4." → not JSON, parse fails. The model is told
"Your reply could not be parsed: … Reply again with only the JSON object." Reply 2:
`{"answer": "4", "confidence": 0.95, "sources": [1]}` → `Answer(answer='4', confidence=0.95, sources=[1])`
after two attempts.

## What the library does inside
It extracts the JSON, then runs Pydantic's validation ([[pydantic-bodies]]). The retry loop is the
validate-and-retry pattern you will meet again with agents.

## Common mistakes
* Trusting `json.loads` alone, without range and type validation.
* Retrying without telling the model what was wrong.
* Retrying forever (or catching every exception and hiding real bugs).

## Why this matters
Structured output connects language models to the rest of a program: databases, APIs, tool calls
and user interfaces all need validated data.
''',
"statement": r'''
1. `class Answer(BaseModel)` with `answer: str = Field(min_length=1)`, `confidence: float = Field(ge=0, le=1)`
   and `sources: list[int] = []`.
2. `build_messages(question, parser)` returns
   `[SystemMessage("Answer the question.\n" + parser.get_format_instructions()), HumanMessage(question)]`.
3. `ask_structured(model, question, max_retries=2)` makes a `PydanticOutputParser(pydantic_object=Answer)`,
   invokes `model` with the messages and tries to parse the reply's `content`. On
   `OutputParserException`, append the reply and
   `HumanMessage(f"Your reply could not be parsed: {error}\nReply again with only the JSON object.")`
   and try again, up to `max_retries` retries. Return `(answer, attempts)`; if every attempt fails,
   raise the last `OutputParserException`.
''',
"starter": r'''
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Answer(BaseModel):
    # TODO
    pass


def build_messages(question, parser):
    # TODO
    pass


def ask_structured(model, question, max_retries=2):
    # TODO
    pass
''',
"hints": [
    "`Field(ge=0, le=1)` bounds the confidence; `Field(min_length=1)` forbids an empty answer.",
    "Loop `for attempt in range(max_retries + 1)`: `reply = model.invoke(messages)`, then `parser.parse(reply.content)` inside try.",
    "In the except branch save the error and extend the message list with the reply and a corrective HumanMessage.",
],
"solution": r'''
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Answer(BaseModel):
    answer: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    sources: list[int] = []


def build_messages(question, parser):
    return [SystemMessage("Answer the question.\n" + parser.get_format_instructions()), HumanMessage(question)]


def ask_structured(model, question, max_retries=2):
    parser = PydanticOutputParser(pydantic_object=Answer)
    messages = build_messages(question, parser)
    last_error = None
    for attempt in range(max_retries + 1):
        reply = model.invoke(messages)
        try:
            return parser.parse(reply.content), attempt + 1
        except OutputParserException as error:
            last_error = error
            messages = messages + [reply, HumanMessage(
                f"Your reply could not be parsed: {error}\nReply again with only the JSON object.")]
    raise last_error
''',
"explanation": r'''
The Pydantic model is the contract; its format instructions go into the system message. Each reply is
parsed and validated; a failure becomes feedback in the conversation so the next attempt can correct
it, and the loop gives up after a fixed number of retries.
''',
"tests": r'''
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
''',
"feedback": [
    ("test_retry_after_prose", "Catch OutputParserException and invoke the model again."),
    ("test_out_of_range_is_invalid", "Bound confidence with Field(ge=0, le=1); sources defaults to []."),
    ("test_gives_up", "After max_retries retries, raise the last OutputParserException."),
    ("test_messages_and_feedback", "Append the failed reply and a HumanMessage containing 'could not be parsed'."),
],
},
# ---------------------------------------------------------------- lm-langchain-rag
{
"slug": "lm-langchain-rag", "title": "Retrieval-Augmented Generation with LangChain",
"difficulty": "advanced", "prereqs": ["lm-structured-output", "nlp-tfidf-retrieval"], "packages": ["langchain-core"],
"objectives": ["Implement the Embeddings interface and index documents in InMemoryVectorStore",
               "Retrieve context for a question and build a grounded prompt with source ids",
               "Check that an answer cites only the retrieved sources"],
"tags": ["langchain", "rag", "retrieval", "vector-store", "citations"],
"sources": ["S133", "S130"], "entry": "class KeywordEmbeddings(Embeddings); build_store(docs, vocabulary); rag_answer(store, model, question, k=2)",
"article": r'''
# Retrieval-Augmented Generation with LangChain

## Intuition
A language model knows only what it was trained on. Retrieval-augmented generation (RAG) first finds
the passages relevant to a question in your own documents, then asks the model to answer **from those
passages**, citing them. Checking the citations catches answers that are not supported by what was
retrieved.

## Precise explanation
1. **Embeddings** turn text into vectors. In LangChain any class with `embed_documents(texts)` and
   `embed_query(text)` is an `Embeddings`. Real systems use neural sentence embeddings; here a keyword
   count vector over a fixed vocabulary, L2-normalised, keeps everything offline and deterministic.
2. **Vector store**: `InMemoryVectorStore(embedding)`; `add_texts(texts, ids=ids)`;
   `similarity_search(question, k)` returns the k most similar `Document`s (with `.id` and
   `.page_content`) by cosine similarity.
3. **Prompt**: put the retrieved passages into the system message, each prefixed with its id:
   `[faq-2] Submissions are graded on the VPS.` and instruct the model to answer only from them and
   cite ids in brackets.
4. **Check**: extract `[id]` citations from the answer; the answer is *grounded* if it cites at least
   one source and every cited id was retrieved.

## Worked example
Documents faq-1 "Run checks visible tests in the browser", faq-2 "Submit grades all tests on the
server", faq-3 "Progress counts passed problems". The question "how are tests graded on submit" retrieves
faq-2 first. An answer "Submit runs every test on the server [faq-2]." is grounded; one citing [faq-9]
is not.

## What the library does inside
The vector store keeps the vectors and ranks them with cosine similarity — your TF-IDF search in
[[nlp-tfidf-retrieval]] and the pipeline of [[rag-pipeline]] (the optional deep dive after this step),
behind interfaces that let you swap in a real embedding model and database.

## Common mistakes
* Retrieving too few passages (the answer is missing) or too many (the prompt fills with noise).
* Not giving passages ids, so citations cannot be checked.
* Trusting fluent answers that cite nothing.

## Why this matters
Most production LLM applications — documentation assistants, support bots, the course-FAQ project idea
after this step — are RAG systems.
''',
"statement": r'''
1. `class KeywordEmbeddings(Embeddings)` with `__init__(self, vocabulary)`: `embed_query(text)` counts
   how often each vocabulary word appears among `re.findall(r"[a-z]+", text.lower())`, L2-normalises the
   counts (a zero vector stays zero) and returns a list of floats; `embed_documents(texts)` maps
   `embed_query` over the texts.
2. `build_store(docs, vocabulary)` takes a dict `{id: text}` and returns an `InMemoryVectorStore`
   with the texts added under their ids.
3. `rag_answer(store, model, question, k=2)` retrieves `k` documents, builds a
   `ChatPromptTemplate` with system message
   `"Answer only from the context and cite sources as [id].\n\nContext:\n{context}"` (context lines
   `"[id] text"`) and human message `"{question}"`, runs `prompt | model | StrOutputParser()` and returns
   `{"answer": str, "retrieved": [ids], "cited": [ids in order of first appearance], "grounded": bool}`.
''',
"starter": r'''
import math
import re

from langchain_core.embeddings import Embeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore


class KeywordEmbeddings(Embeddings):
    def __init__(self, vocabulary):
        # TODO
        pass

    def embed_documents(self, texts):
        # TODO
        pass

    def embed_query(self, text):
        # TODO
        pass


def build_store(docs, vocabulary):
    # TODO
    pass


def rag_answer(store, model, question, k=2):
    # TODO
    pass
''',
"hints": [
    "Count words with a dict over the vocabulary; the norm is `math.sqrt(sum(v * v for v in counts))`.",
    "`store = InMemoryVectorStore(KeywordEmbeddings(vocabulary))`; `store.add_texts(list(docs.values()), ids=list(docs))`.",
    "Citations: `re.findall(r\"\\[([\\w-]+)\\]\", answer)`, keeping the first occurrence of each.",
],
"solution": r'''
import math
import re

from langchain_core.embeddings import Embeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Answer only from the context and cite sources as [id].\n\nContext:\n{context}"),
    ("human", "{question}"),
])


class KeywordEmbeddings(Embeddings):
    def __init__(self, vocabulary):
        self.vocabulary = list(vocabulary)

    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text):
        words = re.findall(r"[a-z]+", text.lower())
        counts = [float(words.count(w)) for w in self.vocabulary]
        norm = math.sqrt(sum(v * v for v in counts))
        return [v / norm for v in counts] if norm else counts


def build_store(docs, vocabulary):
    store = InMemoryVectorStore(KeywordEmbeddings(vocabulary))
    store.add_texts(list(docs.values()), ids=list(docs))
    return store


def rag_answer(store, model, question, k=2):
    found = store.similarity_search(question, k=k)
    context = "\n".join(f"[{d.id}] {d.page_content}" for d in found)
    answer = (PROMPT | model | StrOutputParser()).invoke({"context": context, "question": question})
    cited = []
    for ref in re.findall(r"\[([\w-]+)\]", answer):
        if ref not in cited:
            cited.append(ref)
    retrieved = [d.id for d in found]
    return {"answer": answer, "retrieved": retrieved, "cited": cited,
            "grounded": bool(cited) and set(cited) <= set(retrieved)}
''',
"explanation": r'''
The embedding class satisfies LangChain's interface, so the in-memory store can index and search with
it. Retrieved passages are labelled with their ids in the prompt; after the model answers, the cited
ids are compared with the retrieved ones to decide whether the answer is grounded.
''',
"tests": r'''
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
''',
"feedback": [
    ("test_embeddings", "Count vocabulary words, L2-normalise, and keep an all-zero vector as zeros."),
    ("test_retrieval_order", "Add the texts with ids=list(docs) and search with similarity_search."),
    ("test_grounded_answer", "Grounded means at least one citation and every cited id was retrieved."),
    ("test_repeated_citations_once", "List each cited id once, in order of first appearance."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "poem-name-generator", "title": "Poem or Name Generator",
"tags": ["language-model", "text-generation", "gpt"],
"brief": r'''
Train your tiny GPT on text you choose — public-domain poems, Indian city names, invented
character names — and generate new samples. Explore how context length, model size and
sampling temperature change the results.
''',
"uses": ["temperature-softmax", "top-k-top-p", "lm-tiny-gpt", "torch-save-load"],
"milestones": [
    "Collect a text file of at least 50 KB (or a list of a few thousand names, one per line).",
    "Train the tiny GPT with a train/validation split and plot both losses.",
    "Add temperature and top-k sampling to generate, and compare greedy with sampled output.",
    "Scale up: more layers, a longer context, a wider model — and note the validation loss each time.",
    "Save the best model and write a script that prints ten new samples.",
],
"stretch": [
    "Switch from characters to a BPE tokenizer (see the BPE step).",
    "Add a key–value cache to generation and measure the speed-up.",
    "Filter generated names that already appear in the training data.",
],
"data": r'''
Public-domain books from [Project Gutenberg](https://www.gutenberg.org/) (download a plain-text file),
your own writing, or name lists you assemble. Keep the text in one UTF-8 file.
''',
"setup": r'''
```bash
pip install torch
python train_gpt.py --text poems.txt --steps 5000
```
A laptop CPU is enough for a model with a few hundred thousand parameters.
''',
},
{
"kind": "project", "slug": "course-faq-chatbot", "title": "Course FAQ Chatbot",
"tags": ["rag", "chatbot", "langchain"],
"brief": r'''
Build a chatbot that answers questions about this course — what a step covers, how Run and Submit
differ, which step to do next — using RAG over the course's lesson text, and that cites the lessons it
used. It should say "I don't know" when the answer is not in the material.
''',
"uses": ["nlp-tfidf-retrieval", "lm-chat-prompt-langchain", "lm-structured-output", "lm-langchain-rag"],
"milestones": [
    "Split lesson texts into passages of a few paragraphs, each with an id and its lesson title.",
    "Index the passages with TF-IDF or a sentence-embedding model and test retrieval on 20 questions.",
    "Connect a chat model (a local model through Ollama or a hosted API) with a prompt that requires citations.",
    "Return structured answers (answer, cited ids, confidence) and reject ungrounded ones.",
    "Build a tiny evaluation set of question/expected-lesson pairs and report retrieval and answer accuracy.",
],
"stretch": [
    "Keep conversation history so follow-up questions work.",
    "Serve it with FastAPI and add a chat box to a web page.",
    "Log questions the bot could not answer to find gaps in the lessons.",
],
"data": r'''
Use the lesson articles of this course (each step's lesson) or notes from your own classes. For a local
model without API keys, install [Ollama](https://ollama.com/) and pull a small model.
''',
"setup": r'''
```bash
pip install langchain-core langchain-ollama scikit-learn
python faq_bot.py
```
''',
},
{
"kind": "project", "slug": "prompt-playground", "title": "Prompt Playground",
"tags": ["prompting", "decoding", "evaluation"],
"brief": r'''
Build a small tool that sends the same task to a model with different prompts and decoding settings,
shows the outputs side by side, and scores them — so you can see what temperature, top-p, system
messages and few-shot examples actually change.
''',
"uses": ["temperature-softmax", "top-k-top-p", "beam-search", "lm-chat-prompt-langchain"],
"milestones": [
    "Define three tasks (summarise, classify, extract fields) with a few test inputs each.",
    "Write prompt variants: plain, with a system message, with two few-shot examples.",
    "Run each variant at temperatures 0, 0.7 and 1.2 and store the outputs in a table.",
    "Score outputs automatically where possible (exact match for classification, valid JSON for extraction).",
    "Summarise which settings work best per task, with examples of failures.",
],
"stretch": [
    "Repeat each setting five times to measure variability.",
    "Use your tiny GPT for the decoding experiments and a chat model for the prompting ones.",
    "Turn the table into an HTML report.",
],
"data": r'''
Write your own small task inputs (10–20 per task). A local model through [Ollama](https://ollama.com/)
avoids API costs.
''',
"setup": r'''
```bash
pip install langchain-core langchain-ollama pandas
python playground.py
```
''',
},
]
