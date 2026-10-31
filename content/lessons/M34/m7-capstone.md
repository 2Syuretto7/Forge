# Capstone: compress embeddings, check the derivations

Compress 100 embeddings from 2,048 dimensions with a random projection that keeps every pairwise distance within 10 percent, find the smallest target dimension that does it, and compare it with the lemma's. Then check two derivations of this lesson by measurement: the variance of scaled attention scores and the variance factor of He initialization over 50 layers.

:::exercise{ref=capstone}
:::

## When you finish

You can predict what random vectors and random matrices do in high dimension and use it to explain attention scaling, initialization and dimension reduction. L09 applies the scaling in attention, L06 the variance argument in normalization, and M38 the geometry in efficient models.

:::edge{to=L09 text="the 1/sqrt(d) in attention."}
:::

:::edge{to=L06 text="initialization, normalization and variance preservation."}
:::
