# Build: kernel algorithms in NumPy

These exercises implement, in NumPy, exactly the algorithms the Triton kernels in the notebook run: the same loops over blocks, the same running statistics. Get them right here, where you can print every intermediate value.

## Blocks and memory

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

## Fused normalization

:::exercise{ref=e05}
:::

## FlashAttention

:::exercise{ref=e06}
:::

::::predict{id=p3 kind=choice answer=c}
Your tiled FlashAttention processes key blocks in order $1, 2, \dots$. What happens to the output if you process them in reverse order?

- It changes slightly, because the running maximum is different.
- It is wrong, because the rescaling assumes increasing positions.
- It is the same up to floating-point rounding.
- It is the same only without a causal mask.

:::reveal
The merge of two online-softmax summaries is symmetric and associative: whatever order the blocks arrive in, the final $m$ is the overall maximum and $l$ and the accumulator are rescaled to it exactly. Only rounding differs. This freedom is what lets kernels split the key dimension across programs and merge the partial results.
:::
::::

:::exercise{ref=e07}
:::

:::exercise{ref=e08}
:::
