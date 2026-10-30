# QR and back substitution

- `qr(A)`: for `A` of shape `(m, n)`, $m \geq n$, independent columns, return `Q` `(m, n)` with orthonormal columns and `R` `(n, n)` upper triangular with a **positive** diagonal and $A = QR$. Record $R_{jk} = q_j \cdot v$ inside the modified Gram-Schmidt loop and $R_{kk} = \|v\|$.
- `back_substitute(R, y)`: solve $Rx = y$ for upper triangular `R`, from the last row up, without `np.linalg.solve`.
- `lstsq_qr(A, b)`: least squares by $R\hat x = Q^\top b$ using your two functions.

## Hints

1. In the inner loop: `R[j, k] = Q[:, j] @ v`, then `v -= R[j, k] * Q[:, j]`.
2. `x[i] = (y[i] - R[i, i+1:] @ x[i+1:]) / R[i, i]`.
3. The positive diagonal makes the factorization unique, so it matches NumPy's up to signs.
