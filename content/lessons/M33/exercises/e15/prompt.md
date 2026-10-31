# Break it: squaring the condition number

The normal equations $A^\top Ax = A^\top b$ are the fastest way to write least squares and the least accurate way to solve it. Forming $A^\top A$ squares the condition number, so in double precision a problem with $\kappa(A) = 10^8$ becomes one with $\kappa = 10^{16}$, where every digit can be lost (M26, Section 7). The QR factorization $A = QR$ solves $Rx = Q^\top b$ and keeps the conditioning of $A$.

- `vandermonde(m, n)`: the $m \times n$ matrix with entries $t_i^j$, $j = 0, \dots, n - 1$, at $m$ equally spaced points $t_i$ in $[0, 1]$: a polynomial fit, and badly conditioned.
- `solve_normal(A, b)` and `solve_qr(A, b)`.
- `relative_error(x, x_true)`.

The tests fit a degree-11 polynomial whose exact coefficients are known, so the data fit it perfectly: QR recovers the coefficients to about $10^{-9}$, and the normal equations miss them by more than 1 percent.

## Hints

1. `np.vander(t, n, increasing=True)`.
2. Solve the triangular system with `np.linalg.solve(R, Q.T @ b)`; it is small.
3. The error of a backward-stable method is about $\kappa\varepsilon$; of the normal equations about $\kappa^2\varepsilon$.
