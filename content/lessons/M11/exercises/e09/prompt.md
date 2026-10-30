# Independence and a basis

- `independent(vectors, tol=1e-10)`: whether a list of vectors (NumPy arrays of the same length) is linearly independent, by comparing the rank of the matrix with those vectors as columns to their number.
- `pick_basis(vectors, tol=1e-10)`: the indices of a maximal independent subset, chosen greedily in order: keep a vector if it is not a combination of the ones already kept.
- `coordinates(basis, v)`: the weights $c$ with $\sum_i c_i\, \text{basis}_i = v$, for an independent list `basis` and a `v` in its span (use `np.linalg.lstsq`, or your own solver).

The starter provides `rank` from e05.

## Hints

1. `np.column_stack(vectors)`.
2. Keep vector $k$ when adding it raises the rank of the kept set.
3. More vectors than coordinates can never be independent.
