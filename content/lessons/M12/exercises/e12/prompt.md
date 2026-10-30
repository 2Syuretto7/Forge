# Least squares on a stream

A million rows do not need to sit in memory at once: the normal equations only need $A^\top A$ ($n \times n$) and $A^\top b$ (length $n$), which are sums over rows.

- `accumulate(chunks)`: for an iterable of `(A_chunk, b_chunk)` pairs, return `(G, h)`, the sums of `A_chunk.T @ A_chunk` and `A_chunk.T @ b_chunk`.
- `stream_fit(chunks)`: solve $G x = h$.
- `make_chunks(n_rows, n_cols, chunk, seed=0)`: a generator yielding chunks of a synthetic regression problem $b = A x^\star + 0.1\,\text{noise}$ with $x^\star = (1, 2, \dots, n)$, drawn chunk by chunk from `np.random.default_rng(seed)`.

The tests fit a million rows in chunks of 50,000 and recover $x^\star$. This is the one place where the normal equations earn their keep, when the problem is well conditioned.

## Hints

1. Start from zeros and add each chunk's contribution.
2. A generator uses `yield`, so only one chunk exists at a time.
3. With a million rows of noise 0.1, the estimate is within about $10^{-3}$ of $x^\star$.
