# Scale: a hundred million numbers and the small formats

Sum $10^8$ random numbers between 0 and 1. The truth is about $5 \times 10^7$.

::::predict{id=p4 kind=choice answer=b}
What does a plain sequential sum in float32 return?

- About $5 \times 10^7$, slightly off.
- About $1.7 \times 10^7$.
- About $10^8$.
- Infinity.

:::reveal
About $1.68 \times 10^7 = 2^{24}$. Once the total passes $2^{24}$, the gap between floats is 2 and every term below 1 rounds away, so the sum stalls at a third of the truth. Pairwise and Kahan summation in the same float32 land within a few units of $5 \times 10^7$.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

The same $0.001$ in each format: fp16 stores it within a few parts in ten thousand and bf16 within a few parts in a thousand; fp8 E5M2 can be off by up to 12 percent, and in fp8 E4M3 it falls among the subnormals and becomes $2^{-9} \approx 0.00195$, nearly double. A training step that changes a weight of 1 by $0.001$ disappears in bf16.

:::widget{name=FloatFormats value=0.001}
:::
