# Scale: searching 100,000 vectors

A semantic search engine stores one embedding per document and answers a query by finding the stored vectors with the largest cosine similarity. Brute force computes all of them. That is $N \times d$ multiply-adds per query: for 100,000 vectors of 32 numbers, 3.2 million, which a vectorized loop does in milliseconds and a Python loop in seconds.

::::predict{id=p4 kind=choice answer=c}
Computing 100,000 cosine similarities in a Python loop versus one NumPy matrix-vector product: roughly how much faster is NumPy?

- About 2 times.
- About 10 times.
- About 100 times or more.
- No faster: the arithmetic is the same.

:::reveal
Typically 100 times or more. The arithmetic is identical, but a Python loop pays for interpreting every operation and every number, while NumPy runs one compiled loop over contiguous memory. Vectorizing is the first and largest optimization in numerical Python; the GPU lessons apply the same idea once more, with thousands of cores.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

The widget previews M10: a matrix applied to all the unit vectors at once turns the circle into an ellipse. Searching with a matrix product is that machine applied to the query: one dot product per stored vector, all at once.

:::widget{name=MatrixTransform a=1.4 b=0.3 c=0.2 d=0.8}
:::
