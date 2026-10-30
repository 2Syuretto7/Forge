# Small singular values through A^T A

- `ill_matrix(kappa, seed=0)`: a $40 \times 6$ matrix with singular values from 1 down to $1/\kappa$, evenly spaced in logarithm (orthonormal factors from QR of random matrices).
- `smallest_two_ways(A)`: `(via_svd, via_gram)`: the smallest singular value from `np.linalg.svd(A)` and from the square root of the smallest eigenvalue of $A^\top A$ (clip negatives to 0).
- `normal_vs_qr(A, x_true)`: form $b = Ax_{\text{true}}$, solve least squares with the normal equations and with QR, and return `{"normal": err, "qr": err}`, relative errors against `x_true`.

At $\kappa = 10^{10}$, $A^\top A$ has smallest eigenvalue $10^{-20}$, far below the rounding of its largest entries, about $10^{-16}$: the Gram route reports garbage near $10^{-8}$, while the SVD of $A$ is accurate.

## Hints

1. `U, _ = np.linalg.qr(rng.normal(size=(40, 6)))`, similarly `V` for $6 \times 6$, then `U @ np.diag(s) @ V.T`.
2. `np.linalg.eigvalsh(A.T @ A)[0]`.
3. Relative error: `norm(x - x_true) / norm(x_true)`.
