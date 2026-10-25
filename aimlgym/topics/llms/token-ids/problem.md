# LM-01 · Vocabularies and Token IDs

**Topic:** Large Language Models · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** NL-07 Bag-of-Words Vectors

Read the lesson first: [article.md](article.md)

## Task

Tokenise by lowercasing and `str.split()`. Implement:

1. `build_vocab(texts, min_count=1)` → dict token → ID with `SPECIALS = ["<pad>", "<unk>",
   "<bos>", "<eos>"]` at IDs 0–3, then tokens with count ≥ `min_count`, sorted by count
   (descending) then alphabetically.
2. `encode(text, vocab, add_special=True)` → list of IDs, unknown tokens → `<unk>`; with
   `add_special` wrap in `<bos>` … `<eos>`.
3. `decode(ids, vocab, skip_special=True)` → tokens joined by single spaces; skip special tokens
   when `skip_special` is true.
4. `pad_batch(seqs, pad_id=0)` → `(padded, mask)` lists of lists, padding on the right to the
   longest length.

## Hints

<details><summary>Hint 1</summary>

`counts = Counter(tok for t in texts for tok in t.lower().split())`; sort items with `key=lambda kv: (-kv[1], kv[0])`.

</details>

<details><summary>Hint 2</summary>

`vocab.get(tok, vocab["<unk>"])`; decode with an inverse dict `{i: t for t, i in vocab.items()}`.

</details>

<details><summary>Hint 3</summary>

`L = max(len(s) for s in seqs)` (0 for an empty batch); `s + [pad_id] * (L - len(s))` and `[1] * len(s) + [0] * (L - len(s))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_vocab_order` | Put the four specials first, then sort tokens by count descending and alphabetically. |
| `test_min_count` | Skip tokens whose count is below `min_count`. |
| `test_encode_unknown` | Lowercase, map unknown tokens to `<unk>` and wrap with `<bos>`/`<eos>`. |
| `test_round_trip` | Invert the vocabulary for decoding and drop special tokens only when asked. |
| `test_pad_batch` | Pad on the right to the longest sequence; the mask is 1 for real tokens. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Special tokens are inserted first so their IDs never change; frequency-then-alphabetical sorting
makes the remaining IDs reproducible. Encoding falls back to `<unk>`, decoding uses the inverted
mapping, and padding builds the ID matrix and its mask in the same pass.

## References

- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
