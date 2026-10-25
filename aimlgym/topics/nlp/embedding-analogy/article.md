# Word Embeddings and Analogies

## Learning outcomes

After this lesson you can:

- Find nearest neighbours in embedding space
- Solve analogies with vector arithmetic (3CosAdd)
- Exclude query words from results

## Intuition
Embeddings place words as points so that similar words are close. Remarkably, consistent
*directions* can appear: the offset from "man" to "woman" resembles the offset from "king" to
"queen". "a is to b as c is to ?" becomes vector arithmetic.

## Precise explanation
**Nearest neighbours:** rank words by cosine similarity (NL-11) to a query vector.
**3CosAdd analogy:** answer $d^* = \arg\max_{d \notin \{a,b,c\}} \cos(v_d,\ v_b - v_a + v_c)$.
Excluding a, b, c is essential: the target vector is usually closest to b or c themselves.
Real embeddings (word2vec, GloVe) have 100–300 dimensions; analogies work for some relations and
fail for many — they are a probe, not a guarantee.

## Worked example
Toy 3-D embeddings: man [1,0,0], woman [1,1,0], king [1,0,1], queen [1,1,1]:
woman − man + king = [1,1,1] → queen (cos 1).

## Common mistakes
* Not excluding the input words.
* Euclidean distance on unnormalised vectors (frequency effects dominate).
* Over-interpreting analogy results as "understanding".

## Why this matters
Embedding lookup is the first layer of every LLM; similarity search over embeddings drives
semantic retrieval.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
