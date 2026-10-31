# Batch dependence and batch noise

Your batch norm and layer norm forward passes are provided.

1. `batch_dependence(norm, x, batch_a, batch_b)`: put example `x` (a vector) on top of `batch_a`, normalize with `norm` (`"batch"` for training-mode batch norm, `"layer"` for layer norm, with $\gamma = 1$, $\beta = 0$), keep the output row for `x`; repeat with `batch_b`; return the largest absolute difference between the two rows.
2. `batch_mean_noise(B, trials=2000, seed=0)`: the standard deviation, over `trials` draws, of the mean of `B` unit-normal values, drawn as one `(trials, B)` array from `np.random.default_rng(seed)`.

The first shows that batch norm makes one example's output depend on its neighbours; the second, how noisy batch statistics are for small batches.

## Hints

1. `np.vstack([x[None, :], others])` puts `x` in row 0.
2. Layer norm's output for `x` cannot depend on the other rows at all.
3. The noise should fall like $1/\sqrt B$.
