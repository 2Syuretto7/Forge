# QR factorization and back substitution

Build the QR factorization from Gram-Schmidt and the triangular solver that makes it useful.

- `qr(A)`: for `A` of shape `(m, n)`, $m \ge n$, independent columns, return `Q` `(m, n)` with orthonormal columns and `R` `(n, n)` upper triangular with a **positive** diagonal, such that $A = QR$. Record $R_{jk} = q_j^\top v$ during the modified Gram-Schmidt loop and $R_{kk} = \|v\|$.
- `back_substitute(R, y)`: solve $Rx = y$ for upper-triangular `R` `(n, n)` and `y` `(n,)`, starting from the last row. Do not call `np.linalg.solve`.

With these two, least squares becomes $Rx = Q^\top b$.

## Hints

1. Inside the inner loop, `R[j, k] = Q[:, j] @ v` and then `v -= R[j, k] * Q[:, j]`.
2. Back substitution: `x[i] = (y[i] - R[i, i+1:] @ x[i+1:]) / R[i, i]` for `i` from `n-1` down to `0`.
3. The positive-diagonal convention makes the factorization unique.
