# What communication costs

The alpha-beta model charges every message step a latency $\alpha$ and every byte $1/\text{bandwidth}$. A ring reduce-scatter or all-gather over $P$ ranks takes $P - 1$ steps in which each rank sends $(P-1)/P$ of the data; an all-reduce is both.

1. `collective_time(op, n_bytes, P, alpha, bandwidth)` for `op` in `"reduce_scatter"`, `"all_gather"`, `"all_reduce"`; zero when $P = 1$.
2. `dp_step_time(n_params, P, alpha, bandwidth, compute_seconds, overlap)`: compute plus the all-reduce of 2-byte gradients; with `overlap`, communication runs during the backward pass and the step takes the longer of the two.

## Hints

1. All-reduce: $2(P-1)\alpha + 2\frac{P-1}{P}\frac{n}{\text{bandwidth}}$.
2. For large $P$ the bandwidth term tends to $2n/\text{bandwidth}$: adding ranks barely adds traffic per rank, but every rank adds latency.
3. Overlap works because gradients of the last layers are ready first: their all-reduce can start while earlier layers are still in backward.
