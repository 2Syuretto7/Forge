# Puzzle: why is generation slow?

A 7-billion-parameter model on an A100 can do over 300 trillion 16-bit operations per second, and generating one token takes about 14 billion of them.

::::predict{id=p1 kind=choice answer=b}
How many tokens per second can one sequence generate?

- About 20,000: 300 trillion divided by 14 billion.
- About 150: every token reads all 13.5 GB of weights from memory, at about 2 TB/s.
- About 1, because attention is quadratic.
- It depends only on the length of the prompt.

:::reveal
Generating a token touches every weight once but does only two operations per weight: an arithmetic intensity of about 1 FLOP per byte, far below the A100's ridge point of about 150 (L07). The bandwidth sets the speed, about 150 tokens per second, using under 1% of the arithmetic. Serving many sequences at once reuses each weight read for every sequence in the batch, which is where all of inference's tricks begin.
:::
::::

The widget adds the cache of keys and values that every sequence keeps, and shows how it limits how many sequences fit.

:::widget{name=KVCacheMeter model=llama7}
:::

::::predict{id=p2 kind=numeric answer=2 tol=0.05}
Llama 2 7B stores 0.5 MiB of keys and values per token. How many GiB does the cache of one 4,096-token sequence take?

:::reveal
$4096 \times 0.5$ MiB $= 2$ GiB. Thirty such sequences take 60 GiB, more than the model itself. Grouped-query attention, which shares each key-value head among several query heads, divides this by the group size: Mistral 7B and Llama 2 70B use 8 key-value heads.
:::
::::
