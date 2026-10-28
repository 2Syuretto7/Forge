# Puzzle: a softmax that never sees the whole row

A softmax normalizes by the sum of $e^{x_j}$ over the whole row, and the numerically safe version first subtracts the row's maximum. Both seem to require the entire row before any output can be written. For attention over 32,000 positions, a row of scores does not fit in a GPU core's fast memory.

::::predict{id=p1 kind=choice answer=b}
Can you compute a numerically stable softmax by reading the row once, in blocks, keeping only a few numbers between blocks?

- No: the maximum is needed before any exponential can be computed.
- Yes: keep a running maximum and a running sum, and rescale the sum whenever the maximum grows.
- Only if the row is sorted.
- Only approximately.

:::reveal
Keep $m$, the largest value seen so far, and $l = \sum e^{x_j - m}$ over the values seen so far. When a block raises the maximum to $m'$, multiply the old $l$ by $e^{m - m'}$, which converts every old term to the new reference, and add the block's terms. After the last block, $l$ is the exact normalizer. This **online softmax** is the idea behind FlashAttention.
:::
::::

::::predict{id=p2 kind=numeric answer=11.09 tol=0.05}
In fp16, the largest finite number is 65504. Above what input does $e^x$ overflow to infinity?

:::reveal
$\ln 65504 \approx 11.09$. Attention scores beyond 11 are common, so an fp16 softmax that exponentiates without subtracting the maximum, or that accumulates in fp16, produces infinities and NaNs. Kernels load fp16 and compute in fp32.
:::
::::
