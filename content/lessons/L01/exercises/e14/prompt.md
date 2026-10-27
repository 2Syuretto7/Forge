# Break it: float32, Hilbert matrices and the normal equations

Two experiments make Section 7 concrete.

**Experiment 1.** The Hilbert matrix $H_{ij} = 1/(i + j + 1)$ (zero-based indices) is famously ill-conditioned. Write your own solver so the arithmetic precision is fully under your control:

- `hilbert(n, dtype)`: the `n x n` Hilbert matrix as an array of `dtype`.
- `gauss_solve(A, b)`: Gaussian elimination with partial pivoting followed by back substitution, **keeping the dtype of `A`** throughout (no `np.linalg`).
- `hilbert_error(n, dtype)`: build $H$ in `dtype`, set $b = H \mathbf{1}$ (computed in `dtype`), solve with `gauss_solve`, and return the relative error $\|x - \mathbf{1}\| / \|\mathbf{1}\|$ as a float.

**Experiment 2.** `normal_vs_qr(A, x_true)`: form $b = A x_{\text{true}}$ in float64, solve the least-squares problem with the normal equations and with QR (both via `np.linalg`), and return `{"normal": err, "qr": err}` with relative errors against `x_true`.

The tests expect float32 to lose essentially all digits at $n = 6$ while float64 keeps most, and QR to beat the normal equations by orders of magnitude on a matrix with $\kappa = 10^6$.

## Hints

1. Pivoting: at column `k`, swap row `k` with the row below it whose entry in column `k` has the largest magnitude.
2. Copy inputs first (`A = A.copy()`), and create work arrays with `dtype=A.dtype`.
3. Expect float32 errors near $\kappa \varepsilon$: $\kappa(H_6) \approx 1.5 \times 10^7$ and $\varepsilon \approx 6 \times 10^{-8}$.
