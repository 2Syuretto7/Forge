# Build: three normalizations and a deep stack

## Normalization layers

:::exercise{ref=e01}
:::

::::predict{id=p3 kind=choice answer=b}
Batch norm (with $\gamma = 1$, $\beta = 0$, tiny $\epsilon$) receives a batch of exactly two examples. What are its outputs?

- The inputs unchanged.
- For every feature, $+1$ for the example with the larger value and $-1$ for the other (or 0 for both if they are equal).
- Zeros.
- Values that depend on the magnitude of the difference.

:::reveal
With two values $a > b$, the mean is $(a + b)/2$ and the standard deviation is $(a - b)/2$, so the normalized values are exactly $+1$ and $-1$. Whatever the input, a batch of two keeps only the sign of each difference: batch norm's statistics are only as good as the batch is large.
:::
::::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

:::exercise{ref=e04}
:::

## Residual streams

:::exercise{ref=e05}
:::

## A deep stack in five variants

:::exercise{ref=e06}
:::

:::exercise{ref=e07}
:::
