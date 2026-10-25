r"""Reference solution for LM-14 Beam Search.

Each step expands every unfinished beam by every token, adds log-probabilities, carries finished
beams forward, and keeps the top B by score with a deterministic tie-break. The loop ends at the
length limit or when every surviving beam has produced EOS.
"""
import numpy as np


def beam_search(next_logprobs, prompt, vocab, beam_width=2, max_new=5, eos="</s>"):
    if beam_width < 1 or max_new < 1:
        raise ValueError("beam_width and max_new must be >= 1")
    beams = [(list(prompt), 0.0)]
    for _ in range(max_new):
        candidates = []
        for seq, score in beams:
            if seq and seq[-1] == eos:
                candidates.append((seq, score))
                continue
            lp = np.asarray(next_logprobs(seq), dtype=float)
            for t, l in zip(vocab, lp):
                candidates.append((seq + [t], score + float(l)))
        candidates.sort(key=lambda c: (-c[1], c[0]))
        beams = candidates[:beam_width]
        if all(seq and seq[-1] == eos for seq, _ in beams):
            break
    return beams[0][0], beams[0][1]
