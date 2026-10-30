# Long vectors win the raw dot product

- `rank_by_dot(q, X)` and `rank_by_cosine(q, X)`: the indices of the rows of `X` from best to worst under each score.
- `length_bias(q, X)`: the Spearman-style check: the correlation (`np.corrcoef`) between the rows' lengths and their raw dot-product scores, minus the correlation between their lengths and their cosine scores. A large positive value means the raw score is mostly measuring length.
- `make_trap(q, scale)`: a 2-row array whose first row points exactly along `q` with length 1 and whose second row is at $60^\circ$ from `q` with length `scale`. For `scale` above 2, the second row wins the raw dot product.

## Hints

1. `np.argsort(-(X @ q))`.
2. A vector at $60^\circ$ in the plane of `q` and any perpendicular vector `p`: $\cos 60^\circ\, \hat q + \sin 60^\circ\, \hat p$.
3. Find a perpendicular vector by projecting the coordinate axis least aligned with `q` and taking the residual.
