# Scale: 5,000 embeddings in 768 dimensions

A $5000 \times 768$ data matrix has 3.8 million entries. Its SVD tells you how many directions you really need, and a rank-$k$ factorization stores and applies it in a fraction of the space and time.

::::predict{id=p4 kind=numeric answer=42 tol=1}
Store the rank-16 truncated SVD of a $5000 \times 768$ matrix instead of the matrix: $16 \times (5000 + 768 + 1)$ numbers instead of $5000 \times 768$. About how many times smaller is it?

:::reveal
$3{,}840{,}000 / 92{,}304 \approx 41.6$. Multiplying a vector by the factors is cheaper by about the same ratio. LoRA uses exactly this to fine-tune a large model: the update to a $4096 \times 4096$ weight matrix is stored as two thin factors of rank 8 or 16.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

Embeddings rarely have a few clean directions: their singular values decay like a power law. With such a spectrum there is no obvious cut, and the choice of $k$ is a trade between size and error.

:::widget{name=SpectrumBars shape=power noise=0.1 k=10}
:::
