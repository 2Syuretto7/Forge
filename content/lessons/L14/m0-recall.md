# Recall bridge: cross-entropy and the transformer

From M27: the cross-entropy of a model on data is the average number of nats (or bits) it needs per symbol, it is never below the data's entropy, and $e^{\text{loss}}$ is the perplexity. From L13: a decoder-only transformer maps a sequence of token ids to next-token logits at every position. This lesson supplies the two missing pieces: where the tokens come from, and how to turn the logits back into text. Reviews due from M27 and L13 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
A model that assigns probability $1/65$ to every one of 65 characters has a cross-entropy of $\ln 65 \approx$ [[4.174|tol=0.002]] nats per character.
:::
:::step
In bits, that is $\log_2 65 \approx$ [[6.022|tol=0.002]].
:::
:::step
A loss of 1 nat corresponds to a perplexity of $e \approx$ [[2.718|tol=0.002]].
:::
::::
