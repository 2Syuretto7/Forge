# k-fold cross-validation

- `kfold_indices(n, k, seed)`: shuffle `np.arange(n)` with `np.random.default_rng(seed).permutation(n)` and split it into `k` folds of nearly equal size (`np.array_split`). Return a list of `(train_idx, val_idx)` pairs.
- `cv_mse(x, y, degree, k, seed)`: the average over folds of the validation MSE of a polynomial fit of the given degree.

Every index must appear in exactly one validation fold.

## Hints

1. `folds = np.array_split(perm, k)`; for fold `i`, train on the concatenation of the others.
2. Average the fold scores with equal weight.
3. Copy your polynomial fit into this module.
