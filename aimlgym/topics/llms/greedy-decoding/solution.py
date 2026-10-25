r"""Reference solution for LM-04 Greedy Decoding.

Each iteration calls the model on the full current sequence, appends the argmax token and stops at
EOS. `np.argmax` returns the first maximum, giving the lowest-index tie-break. The step budget
guarantees termination.
"""
import numpy as np


def greedy_decode(next_logits, prompt, vocab, eos="</s>", max_new=20):
    if max_new < 0:
        raise ValueError("max_new must be >= 0")
    tokens = list(prompt)
    for _ in range(max_new):
        z = np.asarray(next_logits(tokens), dtype=float)
        if z.shape != (len(vocab),):
            raise ValueError("logits must align with vocab")
        t = vocab[int(np.argmax(z))]
        tokens.append(t)
        if t == eos:
            break
    return tokens
