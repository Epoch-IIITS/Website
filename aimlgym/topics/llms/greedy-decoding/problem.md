# LM-04 · Greedy Decoding

**Topic:** Large Language Models · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** LM-03 Logits, Temperature and Softmax

Read the lesson first: [article.md](article.md)

## Task

Write `greedy_decode(next_logits, prompt, vocab, eos="</s>", max_new=20)`:
* `next_logits(tokens)` returns a 1-D array of scores aligned with `vocab` (a list).
* Generate until the chosen token is `eos` (it is appended) or `max_new` tokens were added.
* Return the full token list (prompt + generated). Ties → lowest vocabulary index.
* Raise `ValueError` if `max_new < 0` or the logits length differs from `len(vocab)`.

**Example**
```python
vocab = ["i", "like", "tea", "</s>"]
table = {"i": [0, 5, 1, 0], "like": [0, 0, 3, 1], "tea": [0, 0, 0, 9]}
f = lambda toks: np.array(table[toks[-1]], float)
greedy_decode(f, ["i"], vocab)    # ['i', 'like', 'tea', '</s>']
```

## Hints

<details><summary>Hint 1</summary>

`tokens = list(prompt)`; loop `for _ in range(max_new)`.

</details>

<details><summary>Hint 2</summary>

`z = np.asarray(next_logits(tokens))`; `t = vocab[int(np.argmax(z))]` (argmax returns the first max).

</details>

<details><summary>Hint 3</summary>

Append, then `break` if `t == eos`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Append the argmax token and stop after appending EOS. |
| `test_max_new` | Generate at most max_new new tokens. |
| `test_uses_full_context` | Pass the whole current sequence to the model. |
| `test_prompt_not_mutated` | Copy the prompt before appending. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each iteration calls the model on the full current sequence, appends the argmax token and stops at
EOS. `np.argmax` returns the first maximum, giving the lowest-index tie-break. The step budget
guarantees termination.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
