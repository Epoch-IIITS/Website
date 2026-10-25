r"""Reference solution for LM-16 A Tiny GPT in PyTorch.

Embeddings turn characters and positions into vectors, the causal encoder layers mix information from
earlier positions only, and the head scores every possible next character. Training samples random
windows and their one-step-shifted targets; greedy generation repeatedly appends the most likely
next character within the context window.
"""
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
