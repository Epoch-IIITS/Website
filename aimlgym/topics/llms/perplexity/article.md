# Perplexity

## Learning outcomes

After this lesson you can:

- Compute average negative log-likelihood per token
- Convert it to perplexity
- Interpret perplexity as an effective branching factor

## Intuition
If a model is as uncertain as rolling a fair 10-sided die for every token, its perplexity is 10.
Lower perplexity means the model finds the text less surprising.

## Precise explanation
Given the probabilities the model assigned to the **actual** next tokens, $p_1,\dots,p_N$:
$$\text{NLL} = -\frac1N\sum_i \ln p_i,\qquad \text{PPL} = e^{\text{NLL}}.$$
(Equivalently $2^{H}$ with $H$ in bits.) NLL is exactly the mean cross-entropy training loss
(DL-03), so PPL = exp(loss). If any $p_i = 0$, the NLL is infinite and so is perplexity — one reason
smoothing (LM-02) matters. Perplexities are only comparable for the **same tokenisation** and test
set.

## Worked example
p = [0.5, 0.25, 0.125]: NLL = (ln 2 + ln 4 + ln 8)/3 = 2 ln 2 → PPL = 4.
A uniform model over V tokens has PPL = V.

## Common mistakes
* Averaging probabilities instead of log-probabilities.
* Comparing perplexity across different tokenisers.
* Including padding tokens.

## Why this matters
Perplexity is the standard intrinsic metric for language models and appears in LLM technical
reports.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
