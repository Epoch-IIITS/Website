# LM-14 · Beam Search

**Topic:** Large Language Models · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** LM-04 Greedy Decoding

Read the lesson first: [article.md](article.md)

## Task

Write `beam_search(next_logprobs, prompt, vocab, beam_width=2, max_new=5, eos="</s>")` returning
`(best_tokens, best_score)`. `next_logprobs(tokens)` returns a 1-D array of log-probabilities aligned
with `vocab`. Follow the pseudocode exactly (ties → lexicographically smaller token list). Raise
`ValueError` if `beam_width < 1` or `max_new < 1`.

**Example**
```python
vocab = ["a", "b", "</s>"]
def f(t):
    last = t[-1]
    table = {"<s>": [0.6, 0.4, 1e-9], "a": [0.3, 0.3, 0.4], "b": [0.05, 0.05, 0.9]}
    return np.log(np.array(table.get(last, [1e-9, 1e-9, 1.0])))
beam_search(f, ["<s>"], vocab, beam_width=2, max_new=3)
# (['<s>', 'b', '</s>'], log(0.36))
```

## Hints

<details><summary>Hint 1</summary>

Store beams as `(tokens_list, score)`; finished beams are carried over unchanged.

</details>

<details><summary>Hint 2</summary>

Sort candidates with `key=lambda c: (-c[1], c[0])` and keep `[:beam_width]`.

</details>

<details><summary>Hint 3</summary>

Break when every beam's last token is `eos`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_beats_greedy` | Keep the top beam_width candidates by summed log-probability. |
| `test_finished_not_extended` | Carry finished (EOS) beams forward without calling the model. |
| `test_tie_break` | Sort with key (-score, tokens) for deterministic ties. |
| `test_max_new_limit` | Stop after max_new expansion steps. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each step expands every unfinished beam by every token, adds log-probabilities, carries finished
beams forward, and keeps the top B by score with a deterministic tie-break. The loop ends at the
length limit or when every surviving beam has produced EOS.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
