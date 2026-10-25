# Large Language Models

**You will be able to:** Map text to tokens, model and decode next tokens, build attention and transformer blocks, train a tiny GPT in PyTorch, and build LangChain prompts, structured output and RAG pipelines with citation checks.

**Topic prerequisites:** Deep Learning, Natural Language Processing

How a language model turns text into tokens and tokens into text: vocabularies and token IDs,
next-token probabilities, temperature, greedy decoding and perplexity, byte-pair encoding, then
the transformer — scaled dot-product attention, causal masks, positional encodings, multi-head
attention and a pre-norm block as a PyTorch `nn.Module` — then sampling (top-k/top-p), beam search,
KV caching and a tiny character-level GPT trained in PyTorch. The topic ends with LangChain: chat
prompts and messages, structured output with Pydantic and retries, and retrieval-augmented
generation with citation checks.

**Packages:** `numpy`, `torch` and `langchain-core`. No model weights are downloaded and no API is
called: LangChain steps use fake chat models, so tests are exact. The NumPy transformer block,
the hand-made chat template and RAG pipeline are **optional deep dives**. **Project ideas:** a poem
or name generator, a course FAQ chatbot and a prompt playground.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | LM-01 | [Vocabularies and Token IDs](token-ids/problem.md) | beginner | NL-07 |
| 2 | LM-02 | [Next-Token Probabilities (Add-k)](bigram-next-token/problem.md) | beginner | LM-01, NL-02 |
| 3 | LM-03 | [Logits, Temperature and Softmax](temperature-softmax/problem.md) | beginner | LM-02, DL-02 |
| 4 | LM-04 | [Greedy Decoding](greedy-decoding/problem.md) | beginner | LM-03 |
| 5 | LM-05 | [Perplexity](perplexity/problem.md) | beginner | LM-02, DL-03 |
| 6 | LM-06 | [Byte-Pair Encoding Merges](bpe-merges/problem.md) | intermediate | LM-01 |
| 7 | LM-07 | [Scaled Dot-Product Attention](scaled-dot-attention/problem.md) | intermediate | LM-03, NP-06 |
| 8 | LM-08 | [Causal Masking](causal-mask/problem.md) | intermediate | LM-07 |
| 9 | LM-09 | [Sinusoidal Positional Encoding](positional-encoding/problem.md) | intermediate | LM-07 |
| 10 | LM-10 | [Multi-Head Attention](multi-head-attention/problem.md) | intermediate | LM-07, LM-08 |
| 11 | LM-11 | [A Transformer Block as nn.Module](lm-transformer-module/problem.md) | intermediate | LM-10, DL-06 |
| 12 | LM-12 | [A Pre-Norm Transformer Block by Hand (optional deep dive)](transformer-block/problem.md) | intermediate | LM-10, LM-09 |
| 13 | LM-13 | [Top-k and Top-p Filtering](top-k-top-p/problem.md) | advanced | LM-03 |
| 14 | LM-14 | [Beam Search](beam-search/problem.md) | advanced | LM-04 |
| 15 | LM-15 | [Incremental Decoding with a KV Cache](kv-cache/problem.md) | advanced | LM-08, LM-10 |
| 16 | LM-16 | [A Tiny GPT in PyTorch](lm-tiny-gpt/problem.md) | advanced | LM-15, LM-11 |
| 17 | LM-P1 | [Project idea: Poem or Name Generator](poem-name-generator/project.md) | ungraded | LM-03, LM-13, LM-16, DL-26 |
| 18 | LM-17 | [Chat Prompts and Messages with LangChain](lm-chat-prompt-langchain/problem.md) | advanced | LM-16 |
| 19 | LM-18 | [Chat Prompt Templates (optional deep dive)](chat-prompt/problem.md) | advanced | LM-01 |
| 20 | LM-19 | [Structured Output with Pydantic and Retries](lm-structured-output/problem.md) | advanced | LM-17 |
| 21 | LM-20 | [Retrieval-Augmented Generation with LangChain](lm-langchain-rag/problem.md) | advanced | LM-19, NL-10 |
| 22 | LM-21 | [Retrieval-Augmented Generation by Hand (optional deep dive)](rag-pipeline/problem.md) | advanced | LM-18, NL-11 |
| 23 | LM-P2 | [Project idea: Course FAQ Chatbot](course-faq-chatbot/project.md) | ungraded | NL-10, LM-17, LM-19, LM-20 |
| 24 | LM-P3 | [Project idea: Prompt Playground](prompt-playground/project.md) | ungraded | LM-03, LM-13, LM-14, LM-17 |
