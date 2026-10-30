# LU with partial pivoting

`lu(A)` returns `(P, L, U)` for a square matrix with $PA = LU$:

- before clearing column $k$, swap up the row (among rows $k$ and below) with the largest absolute entry in column $k$, and record the swap in `P` and in the multipliers already stored in `L`;
- `L` is unit lower triangular and holds the multipliers, each at most 1 in absolute value;
- `U` is upper triangular.

If a whole column below the diagonal is zero, skip it (the matrix is singular, and `U` gets a zero pivot).

The tests check an **invariant** on random matrices: $PA = LU$, the shapes of the factors, and $|L_{ij}| \leq 1$.

## Hints

1. Keep `U` as a working copy, `L` as the identity, and `perm = list(range(n))`.
2. When swapping rows `k` and `p`, swap them in `U`, swap `L[k, :k]` with `L[p, :k]`, and swap the entries of `perm`.
3. `P = np.eye(n)[perm]`.
