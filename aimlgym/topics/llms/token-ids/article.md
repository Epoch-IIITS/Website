# Vocabularies and Token IDs

## Learning outcomes

After this lesson you can:

- Build a vocabulary with reserved special tokens
- Encode text to integer IDs with an unknown-token fallback and decode it back
- Pad a batch of sequences and build its attention mask

## Intuition
A language model never sees letters or words — it sees integers. A **vocabulary** maps each
token to an ID; encoding turns text into a list of IDs, and decoding turns IDs back into text.
Batches of different-length sequences are padded to the same length, with a **mask** recording
which positions are real.

## Precise explanation
* **Special tokens** get fixed, small IDs: `<pad>` (padding) 0, `<unk>` (unknown) 1, `<bos>`
  (beginning of sequence) 2, `<eos>` (end) 3.
* Regular tokens follow, ordered by frequency (most frequent first) with alphabetical tie-break,
  so the vocabulary is deterministic. Rare tokens (count below `min_count`) are left out and will
  encode as `<unk>`.
* `encode("the cat")` → `[<bos>, id("the"), id("cat"), <eos>]`.
* **Padding**: append `<pad>` until every sequence has the batch's maximum length. The
  **attention mask** has 1 for real tokens and 0 for padding so attention ignores the pads
  (LM-08 combines this with causality).
* Real LLM tokenisers split words into **subwords** (LM-06) so that almost nothing is
  unknown; this step uses whole words to keep the bookkeeping visible.

## Worked example
Texts `["the cat sat", "the dog"]` (lower-cased, split on whitespace): counts the 2, cat 1, dog 1,
sat 1 → IDs the 4, cat 5, dog 6, sat 7. `encode("the bird")` → `[2, 4, 1, 3]`.
`pad_batch([[2, 4, 3], [2, 3]])` → `[[2, 4, 3], [2, 3, 0]]` with mask `[[1, 1, 1], [1, 1, 0]]`.

## Common mistakes
* Assigning IDs in set order, which changes between runs.
* Forgetting `<unk>`, so an unseen word raises `KeyError`.
* Decoding padding and special tokens into the output text.
* Padding on the left for some sequences and the right for others.

## Why this matters
Every model input in this topic — next-token tables, attention, decoding — is a sequence of IDs,
and the embedding table of a real model has exactly one row per vocabulary entry.

## Library implementation

Hugging Face tokenisers (`AutoTokenizer.from_pretrained(...)`) do the same jobs — `encode`,
`decode`, special tokens, `padding=True` returning `input_ids` and `attention_mask` — with
subword vocabularies of tens of thousands of entries. They download vocabulary files, so they are
used only in the optional notebook for this topic, not in graded tests.

## References

- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
