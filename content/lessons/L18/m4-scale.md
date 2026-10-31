# Scale it: better rounding, drafts and latency targets

:::exercise{ref=e08}
:::

::::predict{id=p3 kind=numeric answer=3.36 tol=0.05}
A draft model's tokens are accepted 80% of the time, and it proposes 4 tokens per target pass. How many tokens does each target pass produce on average?

:::reveal
$(1 - 0.8^5)/(1 - 0.8) \approx 3.36$: the accepted prefix of the draft plus one token from the target (a correction or a bonus token). Raising acceptance to 0.9 gives 4.1. A draft distilled from the target, or one sharing its tokenizer and training data, accepts more often.
:::
::::

:::exercise{ref=e09}
:::

:::exercise{ref=e10}
:::
