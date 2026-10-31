# Scale and measure: block sizes and fused losses

Sections 4 and 5 of the notebook time your FlashAttention against unfused attention on a T4. Before that, decide what fits on chip, and apply the same fusion to the largest memory consumer at the end of a language model: the cross-entropy over a large vocabulary.

:::exercise{ref=e09}
:::

::::predict{id=p4 kind=numeric answer=3.29 tol=0.1}
A language model with a vocabulary of 50,257 computes the loss for a batch of 16 sequences of 1024 tokens. How many gigabytes ($10^9$ bytes) do the fp32 logits take?

:::reveal
$16 \cdot 1024 \cdot 50257 \cdot 4 \approx 3.3$ GB. An unfused loss also materializes the probabilities and their gradient, each as large, for about 10 GB in all; a fused cross-entropy computes each row's log-sum-exp with running statistics and writes only the gradient. At this size the loss, not the model, can dominate memory.
:::
::::

:::exercise{ref=e10}
:::
