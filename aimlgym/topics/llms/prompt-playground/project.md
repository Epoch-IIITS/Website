# LM-P3 · Project idea: Prompt Playground

**Topic:** Large Language Models · ungraded

## Brief

Build a small tool that sends the same task to a model with different prompts and decoding settings,
shows the outputs side by side, and scores them — so you can see what temperature, top-p, system
messages and few-shot examples actually change.

## You will use

- LM-03 Logits, Temperature and Softmax
- LM-13 Top-k and Top-p Filtering
- LM-14 Beam Search
- LM-17 Chat Prompts and Messages with LangChain

## Milestones

1. Define three tasks (summarise, classify, extract fields) with a few test inputs each.
2. Write prompt variants: plain, with a system message, with two few-shot examples.
3. Run each variant at temperatures 0, 0.7 and 1.2 and store the outputs in a table.
4. Score outputs automatically where possible (exact match for classification, valid JSON for extraction).
5. Summarise which settings work best per task, with examples of failures.

## Stretch goals

- Repeat each setting five times to measure variability.
- Use your tiny GPT for the decoding experiments and a chat model for the prompting ones.
- Turn the table into an HTML report.

## Data

Write your own small task inputs (10–20 per task). A local model through [Ollama](https://ollama.com/)
avoids API costs.

## Run it yourself

```bash
pip install langchain-core langchain-ollama pandas
python playground.py
```
