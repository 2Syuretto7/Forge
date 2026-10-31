# Logistic regression on a million rows

The starter's `make_data(n=10**6, d=8, seed=0)` returns `(X, y)` for a logistic model with known weights. Train it with three optimizers for two epochs of minibatches of 1,000 rows, in the same random order for all, and compare wall-clock time and final loss.

- `minibatch_grad(w, Xb, yb)`: the logistic gradient on a batch.
- `full_loss(w, X, y, chunk=100000)`: the average loss over all rows, computed chunk by chunk.
- `train(X, y, method, epochs=2, batch=1000, lr=0.1, seed=0)`: `method` is `"sgd"`, `"momentum"` (heavy ball with $\beta = 0.9$ and step `lr * (1 - 0.9)`) or `"adam"` (step `lr / 10`); shuffle with `np.random.default_rng(seed).permutation(n)` once per epoch; return `(w, seconds)` with the time from `time.perf_counter`.

The tests run a **gradient check** of `minibatch_grad`, then train all three and require each to come within 0.01 of the loss of the true weights.

## Hints

1. Index the shuffled order in slices of `batch`: `idx = order[i:i + batch]`.
2. Chunked loss: sum the per-chunk sums, divide by $n$ once.
3. Each epoch is one pass over the data: a thousand cheap steps instead of one expensive one.
