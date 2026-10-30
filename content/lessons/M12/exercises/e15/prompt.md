# Leverage

- `leverages(A)`: the diagonal of the projection matrix $P = A(A^\top A)^{-1}A^\top$, computed without forming the $m \times m$ matrix: with $A = QR$, $P = QQ^\top$, so $P_{ii}$ is the squared length of row $i$ of $Q$.
- `line_design(x)`: the design matrix with columns $1$ and $x$.
- `influence(x, y, i)`: how much the fitted slope changes when point $i$ is removed (new slope minus old).

The tests check an **invariant**: leverages lie in $[0, 1]$ and sum to the number of columns, for random designs.

## Hints

1. `Q, _ = np.linalg.qr(A)`, then `np.sum(Q * Q, axis=1)`.
2. The trace of $P$ is $n$ (Section 3).
3. `np.delete(x, i)` removes a point.
