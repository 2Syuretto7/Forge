# Splitting a vector into two perpendicular parts

- `complement_basis(A)`: an orthonormal basis of the orthogonal complement of the column space of `A` (shape `(m, n)`, independent columns), as an `(m, m - n)` array. Use `np.linalg.qr(A, mode="complete")`: its first $n$ columns span the column space, and the remaining $m - n$ columns are orthonormal and perpendicular to them.
- `split(b, A)`: return `(p, r)` with `p` in the column space, `r` in the complement and `p + r == b`.

The tests check an **invariant**: for random shapes, the dimensions add to $m$, the complement is perpendicular to every column, and the split is unique (projecting `r` onto the column space gives 0).

## Hints

1. `Q, _ = np.linalg.qr(A, mode="complete")`, then `Q[:, n:]`.
2. `p` is the projection; `r = b - p`.
3. With an orthonormal basis $Q_2$ of the complement, `r` is also $Q_2 Q_2^\top b$.
