# Minibatch gradient noise

Section 6 claims a minibatch gradient is an unbiased estimate of the full gradient whose variance falls like $1/B$. Measure it for softmax regression on the spiral (weights only, at a fixed random `W`).

- `per_example_grads(W, X, y)`: shape `(n, d, K)`, the gradient of each example's loss.
- `minibatch_grad_stats(W, X, y, B, draws, seed)`: draw `draws` minibatches of size `B` with replacement (`rng.integers(0, n, size=(draws, B))`), compute each minibatch-average gradient, and return `(mean_error, total_variance)`: the norm of the difference between the average of those estimates and the full gradient, and the average squared distance of an estimate from the full gradient.

The tests check that `total_variance * B` is roughly constant across batch sizes.

## Hints

1. One example: $x_i^\top(p_i - e_{y_i})$, an outer product of shape `(d, K)`.
2. Average per-example gradients over the sampled indices: `G[idx].mean(axis=1)`.
3. Sampling with replacement makes the variance exactly proportional to $1/B$.
