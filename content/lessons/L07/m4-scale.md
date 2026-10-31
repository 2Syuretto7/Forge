# Scale and measure: transfers, profiles and memory

Sections 1 and 2 of the capstone notebook (linked from Movement 7) measure the T4's real matmul and addition throughput and its copy bandwidth; run them when you reach this point and compare them with your models.

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::

::::predict{id=p4 kind=choice answer=c}
Activation checkpointing stores only the input of a block and recomputes the rest during the backward pass. For an MLP block $y = \operatorname{gelu}(xW_1)W_2$ with hidden width four times the input width, what does it cost?

- Nothing: the gradients are computed differently, and the result is cheaper.
- Twice the memory, half the compute.
- About one extra forward pass of compute in exchange for most of the block's activation memory.
- Approximate gradients.

:::reveal
The backward pass recomputes the hidden activations from the stored input, one extra forward pass, and the gradients are exactly the same. In exchange, the block no longer stores $h$ and $\operatorname{gelu}(h)$, each four times the size of the input. Exercise 10 measures both.
:::
::::

:::exercise{ref=e10}
:::
