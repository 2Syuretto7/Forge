# Scale and measure: parameters, FLOPs and attention memory

A transformer's cost has two parts that grow differently: the weights grow with $d^2$, attention grows with the context length. These exercises put numbers on both.

:::exercise{ref=e09}
:::

::::predict{id=p4 kind=numeric answer=805 tol=20}
A model with 12 heads processes a batch of 8 sequences of 2048 tokens. How many megabytes ($10^6$ bytes) does one layer's matrix of attention weights take in fp16?

:::reveal
$8 \cdot 12 \cdot 2048^2 \cdot 2 \approx 805$ MB, for one layer, and the backward pass needs it again. A 12-layer model would hold almost 10 GB of attention weights alone if it kept them all, more than its 124 million weights by a factor of about 40. Quadratic memory in the context length is why long-context attention is computed in tiles that are never stored whole.
:::
::::

:::exercise{ref=e10}
:::

:::widget{name=Roofline hardware=t4 precision=fp16}
:::

On the roofline, the attention scores for a 2048-token context with 64-dimensional heads sit at about 60 FLOP per byte: below the T4's ridge, so memory-bound even before the softmax.
