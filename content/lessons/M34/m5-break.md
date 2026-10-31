# Break it: scales that compound

::::predict{id=p5 kind=choice answer=d}
Attention with $d = 1024$ and 64 keys, scores $q\cdot k$ without the division by $\sqrt d$. On average, how much weight does the softmax give its favourite key?

- About 5 percent.
- About 20 percent.
- About 50 percent.
- More than 90 percent.

:::reveal
More than 90 percent (about 94 in e13): with scores of standard deviation 32, the best key usually beats the second by many units. With the scaling the favourite gets about 11 percent at every width, and the softmax's Jacobian is more than a hundred times larger for the typical query.
:::
::::

:::exercise{ref=e13}
:::

:::exercise{ref=e14}
:::

## Vectors that are not random

:::exercise{ref=e15}
:::

## What to take away

- Scale dot products by $1/\sqrt d$ whenever their width can change.
- Check the per-layer variance factor of an initialization against the activation it feeds.
- Center embeddings before trusting cosine similarities, and read a spectrum against the Marchenko-Pastur bulk before calling a direction signal.
