# Beam Search

## Learning outcomes

After this lesson you can:

- Keep the B best partial sequences by total log-probability
- Handle finished hypotheses (EOS)
- See why beam search can beat greedy decoding

## Intuition
Greedy decoding commits to the best next token even if it leads into a poor continuation. Beam search
keeps the B most promising partial sentences at every step, so a slightly worse first word can still
win if it leads to a much better whole sentence.

## Precise explanation
Score of a sequence = sum of the log-probabilities of its generated tokens.
```text
beams = [(prompt, 0.0)]
repeat max_new times:
    candidates = []
    for (seq, score) in beams:
        if seq ends with EOS: keep (seq, score) as a candidate unchanged
        else: for every token t: candidates.append((seq + [t], score + logp(t | seq)))
    beams = best B candidates (ties: lexicographically smaller token list)
    stop early if all beams end with EOS
return the best beam
```
B = 1 is greedy decoding. Without length normalisation, beam search prefers shorter outputs because
every token adds a negative log-probability — real systems often divide by length^α.

## Worked example
Step 1: P(a) = 0.6, P(b) = 0.4. After a: best next 0.4; after b: best next 0.9.
Greedy: a → 0.6·0.4 = 0.24. Beam (B = 2): b → 0.4·0.9 = 0.36 — better.

## Common mistakes
* Multiplying probabilities (underflow) instead of adding log-probabilities.
* Expanding finished hypotheses past EOS.
* Comparing beams of different lengths without considering the length bias.

## Why this matters
Beam search is standard in machine translation, speech recognition and constrained generation.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
