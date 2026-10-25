# LM-P1 · Project idea: Poem or Name Generator

**Topic:** Large Language Models · ungraded

## Brief

Train your tiny GPT on text you choose — public-domain poems, Indian city names, invented
character names — and generate new samples. Explore how context length, model size and
sampling temperature change the results.

## You will use

- LM-03 Logits, Temperature and Softmax
- LM-13 Top-k and Top-p Filtering
- LM-16 A Tiny GPT in PyTorch
- DL-26 Saving, Loading and Reproducibility

## Milestones

1. Collect a text file of at least 50 KB (or a list of a few thousand names, one per line).
2. Train the tiny GPT with a train/validation split and plot both losses.
3. Add temperature and top-k sampling to generate, and compare greedy with sampled output.
4. Scale up: more layers, a longer context, a wider model — and note the validation loss each time.
5. Save the best model and write a script that prints ten new samples.

## Stretch goals

- Switch from characters to a BPE tokenizer (see the BPE step).
- Add a key–value cache to generation and measure the speed-up.
- Filter generated names that already appear in the training data.

## Data

Public-domain books from [Project Gutenberg](https://www.gutenberg.org/) (download a plain-text file),
your own writing, or name lists you assemble. Keep the text in one UTF-8 file.

## Run it yourself

```bash
pip install torch
python train_gpt.py --text poems.txt --steps 5000
```
A laptop CPU is enough for a model with a few hundred thousand parameters.
