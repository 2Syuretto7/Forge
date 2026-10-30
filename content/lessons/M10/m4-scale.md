# Scale: a batch of 64 products of size 512

A transformer layer is a few batched matrix products. Before timing one, predict how the cost grows.

::::predict{id=p4 kind=numeric answer=8 tol=1.5}
Multiplying two $n \times n$ matrices costs $2n^3$ operations. If $n$ doubles, by about what factor does the time grow?

:::reveal
About 8, since $(2n)^3 = 8n^3$. Measured times can differ at small sizes, where overheads dominate, or when the matrices stop fitting in the processor's cache, but for large matrices the cube law holds well. The exercises below measure it.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

The ellipse in the widget is the image of every unit vector at once. A batched product does this for 64 matrices and 512 vectors each, in one call.

:::widget{name=MatrixTransform a=1.4 b=0.6 c=-0.3 d=0.9}
:::
