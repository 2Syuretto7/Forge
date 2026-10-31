# The Hessian test

A twice-differentiable function is convex exactly when its Hessian is positive semidefinite everywhere (Section 2): all eigenvalues at least 0, M13's test for a quadratic form.

- `hessian_fd(f, x, h=1e-4)`: the Hessian by central differences, $H_{ij} \approx \frac{f(x + he_i + he_j) - f(x + he_i - he_j) - f(x - he_i + he_j) + f(x - he_i - he_j)}{4h^2}$, symmetrized.
- `min_eigenvalue(H)`: the smallest eigenvalue of a symmetric matrix.
- `convex_on_samples(f, points, h=1e-4, tol=1e-6)`: whether the finite-difference Hessian has smallest eigenvalue above `-tol` at every point.

The tests run a **gradient check** of `hessian_fd` against exact Hessians (of a quadratic, and of log-sum-exp, whose Hessian is $\operatorname{diag}(p) - pp^\top$), and classify functions by their Hessians.

## Hints

1. Build the four shifted points with unit vectors `e_i = np.eye(d)[i]`.
2. Symmetrize with `(H + H.T) / 2`.
3. A function like $x^4 - x^2$ is convex in some places and not in others: the samples decide.
