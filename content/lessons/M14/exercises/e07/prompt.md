# Measuring the condition number

Section 2 bounded the relative error growth when solving $Ax = b$ by $\kappa(A) = \sigma_{\max}/\sigma_{\min}$. Measure it and then show the bound is attained.

- `cond2(A)`: the 2-norm condition number of square `A`, from its singular values (`np.linalg.svd(A, compute_uv=False)`).
- `amplification(A, b, db)`: solve $Ax = b$ and $A(x + \delta x) = b + \delta b$ and return $\dfrac{\|\delta x\| / \|x\|}{\|\delta b\| / \|b\|}$.
- `worst_case_pair(A)`: return unit vectors `(b, db)` for which the amplification equals $\kappa(A)$. Think about which output direction makes $\|x\|$ as small as possible relative to $\|b\|$, and which perturbation direction $A^{-1}$ stretches most.

## Hints

1. With `U, s, Vt = np.linalg.svd(A)`, the solution of $Ax = u_i$ is $x = v_i / \sigma_i$.
2. Choose `b` along $u_1$ (so $\|x\| = \|b\|/\sigma_{\max}$) and `db` along $u_n$ (so $\|\delta x\| = \|\delta b\|/\sigma_{\min}$).
3. Compute $\delta x$ as `solve(A, db)` rather than subtracting two solutions, to avoid cancellation.
