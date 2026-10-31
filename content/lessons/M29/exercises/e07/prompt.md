# Minibatch gradients: unbiased, with variance 1/B

A minibatch gradient is an average of per-example gradients, so it is an unbiased estimate of the full gradient with variance proportional to $1/B$ (M24).

- `example_grads(X, y, w)`: the `(n, d)` array of per-example gradients of $\frac12(x_i^\top w - y_i)^2$.
- `full_grad(X, y, w)` and `loss(X, y, w)`: the average gradient and the average loss.
- `minibatch_variance(X, y, w, batch, draws, rng)`: the total variance (trace of the covariance) of `draws` minibatch gradients drawn with replacement.

The tests run a **gradient check** of `full_grad`, confirm that averaging the minibatch gradients over every disjoint batch gives the full gradient exactly, and that the variance falls like $1/B$.

## Hints

1. Row $i$ of the per-example gradients is $(x_i^\top w - y_i)x_i$: `X * r[:, None]`.
2. Total variance: `np.sum(np.var(G, axis=0))` for a `(draws, d)` array of gradients.
3. With replacement, the variance is exactly the per-example variance over $B$.
