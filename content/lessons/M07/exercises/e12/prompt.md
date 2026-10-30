# Rotary encodings at scale

Vectorize the rotary encoding with NumPy.

- `rope_batch(X, positions, base=10000)`: `X` has shape `(n, d)`, one vector per row, `positions` has length `n`; return the encoded array of the same shape, without a Python loop over rows (a loop over nothing at all is best: build the angle array of shape `(n, d/2)` at once).
- `relative_check(d, pairs, seed=0)`: draw a random query and key of length `d`, then for each of `pairs` random pairs of positions $(m, n)$ and a random shift $s$, compare the score at $(m, n)$ with the score at $(m + s, n + s)$. Return the largest absolute difference.

## Hints

1. `angles = positions[:, None] * freqs[None, :]`, with `freqs = base ** (-np.arange(0, d, 2) / d)`.
2. Split `X[:, 0::2]` and `X[:, 1::2]`, rotate, and interleave back with an empty array and slice assignment.
3. Encode a stack of copies of the query at all the positions at once.
