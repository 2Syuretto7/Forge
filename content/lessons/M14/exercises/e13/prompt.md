# PCA without centring

`make_offset_cloud(seed=0)` in the starter returns 500 points in 10 dimensions: a long mean vector plus spread mostly along one known direction `true_dir` (also returned).

- `first_direction(X, centre)`: the top right singular vector of `X`, after subtracting the column means if `centre` is true.
- `alignment(u, v)`: $|u \cdot v|$ for unit vectors (the sign of a singular vector is arbitrary).
- `explained_first(X, centre)`: the fraction $\sigma_1^2 / \sum \sigma_i^2$ with or without centring.

Without centring, the first direction points at the mean and "explains" almost everything; with centring it finds `true_dir`.

## Hints

1. `np.linalg.svd(X, full_matrices=False)[2][0]`.
2. Normalize the mean before comparing with it.
3. The uncentred fraction is large for the wrong reason: the offset's squared length.
