# Single precision on the Hilbert matrix

The Hilbert matrix $H_{ij} = 1/(i + j + 1)$ (indices from zero) is famously ill-conditioned: $\kappa(H_6) \approx 1.5 \times 10^7$. Write your own solver so the arithmetic precision is fully under your control:

- `hilbert(n, dtype)`: the `n x n` Hilbert matrix as an array of `dtype`.
- `gauss_solve(A, b)`: Gaussian elimination with partial pivoting followed by back substitution, **keeping the dtype of `A`** throughout (no `np.linalg`).
- `hilbert_error(n, dtype)`: build $H$ in `dtype`, set $b = H \mathbf{1}$ (computed in `dtype`), solve with `gauss_solve`, and return the relative error $\|x - \mathbf{1}\| / \|\mathbf{1}\|$ as a float.

The tests expect float32 to lose essentially all digits at $n = 6$ while float64 keeps most.

## Hints

1. Pivoting as in M11: at column `k`, swap up the row with the largest entry in that column.
2. Copy inputs first (`A = A.copy()`), and create work arrays with `dtype=A.dtype`.
3. Expect float32 errors near $\kappa \varepsilon$, with $\varepsilon \approx 6 \times 10^{-8}$.
