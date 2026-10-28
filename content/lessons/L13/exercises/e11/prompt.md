# Break it: attention without the scale

Your softmax and its backward pass are provided. Implement `saturation(d, scaled, n=16, seed=0)`: draw queries and keys of shape `(n, d)` with unit-normal entries from `np.random.default_rng(seed)`, form the scores (divided by $\sqrt d$ if `scaled`), take the softmax, and return two numbers: the mean over rows of the largest weight, and the mean absolute value of `softmax_backward(P, G)` for a random upstream gradient `G` drawn next from the same generator.

Compare $d = 16$ and $d = 512$, scaled and unscaled. Unscaled, the weights become nearly one-hot and the gradient reaching the scores shrinks about tenfold.

## Hints

1. Draw `Q`, then `K`, then `G` with shape `(n, n)`.
2. `P.max(axis=1).mean()`.
3. Divide by `np.sqrt(d)` only when `scaled`.
