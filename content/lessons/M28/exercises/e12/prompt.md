# Preconditioning: rescale before you descend

Badly scaled features make a badly conditioned problem: if one feature is in metres and another in millimetres, the loss surface is a long thin valley. Rescaling the coordinates changes the condition number, and the simplest rescaling, dividing by the square root of the Hessian's diagonal (**Jacobi preconditioning**), often removes most of it. Standardizing features before regression (L05) is this idea.

- `jacobi(A)`: the matrix $D^{-1/2} A D^{-1/2}$ with $D = \operatorname{diag}(A)$.
- `kappa(A)`: the condition number from the eigenvalues.
- `scaled_least_squares(n, scales, seed)`: the Hessian $\frac1n X^\top X$ of least squares on `n` rows of independent standard normal features, column $j$ multiplied by `scales[j]`.

The tests show feature scales from $10^{-2}$ to $10^2$ producing a condition number near $10^8$, which Jacobi preconditioning brings down to nearly 1, and an example where it cannot help: a quadratic whose difficulty is in its correlations, not its scales.

## Hints

1. `d = 1 / np.sqrt(np.diag(A))`, then `A * np.outer(d, d)`.
2. Scaling column $j$ by $s_j$ multiplies the Hessian's entry $(i, j)$ by $s_i s_j$.
3. Jacobi preconditioning fixes diagonal scaling exactly, and correlations not at all.
