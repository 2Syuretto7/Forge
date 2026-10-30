# Diagonalization

- `diagonalize(A)`: `(V, lam)` from `np.linalg.eig`.
- `power_by_eig(A, k)`: $A^k = V \Lambda^k V^{-1}$, returning the real part when the result is real up to rounding.
- `spectral(S)`: for symmetric `S`, `(Q, lam)` from `np.linalg.eigh`.

The tests check an **invariant** on random symmetric matrices: `Q` is orthogonal and $Q \Lambda Q^\top = S$.

## Hints

1. `V @ np.diag(lam ** k) @ np.linalg.inv(V)`.
2. `np.real_if_close` drops imaginary parts that are only rounding.
3. `np.allclose(Q.T @ Q, np.eye(n))`.
