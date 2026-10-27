# PCA from the SVD

Implement principal component analysis as in Section 8. Input `X` has shape `(n, d)`, one point per row. Return a dict with:

- `"mean"`: shape `(d,)`.
- `"components"`: shape `(k, d)`, the top `k` right singular vectors of the centered data as rows, each flipped so its largest-magnitude entry is positive.
- `"explained_variance"`: shape `(k,)`, $\sigma_i^2 / (n - 1)$.
- `"explained_variance_ratio"`: shape `(k,)`, $\sigma_i^2 / \sum_j \sigma_j^2$ over **all** singular values.
- `"scores"`: shape `(n, k)`, the centered data expressed in the component basis.

Use `np.linalg.svd(Xc, full_matrices=False)`.

## Hints

1. `Xc = X - X.mean(axis=0)`.
2. The components are the first `k` rows of `Vt`.
3. Compute scores after fixing signs, as `Xc @ components.T`, so they stay consistent.
