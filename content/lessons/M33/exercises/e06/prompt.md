# Preconditioning

CG's speed depends on the condition number, so change the problem: solve with $M^{-1}A$ for a matrix $M \approx A$ that is cheap to invert (Section 4). The **Jacobi** preconditioner $M = \mathrm{diag}(A)$ costs one division per entry and undoes bad scaling of the variables. Preconditioned CG keeps $z = M^{-1}r$ alongside the residual:

$$
\alpha_k = \frac{r_k^\top z_k}{p_k^\top Ap_k},\quad z_{k+1} = M^{-1}r_{k+1},\quad p_{k+1} = z_{k+1} + \frac{r_{k+1}^\top z_{k+1}}{r_k^\top z_k}\,p_k, \quad p_0 = z_0 .
$$

- `pcg(A, b, minv, tol=1e-8, max_iter=5000)`: with `minv` the vector of diagonal entries of $M^{-1}$; returns `(x, iterations)`. With `minv` all ones it is plain CG.
- `badly_scaled(n, rng, spread=1e4)`: $DA_0D$ with $A_0 = GG^\top/n + I$ for a Gaussian $n \times n$ matrix $G$, and $D$ diagonal with entries from `np.geomspace(1/sqrt(spread), sqrt(spread), n)`.
- `jacobi_condition(A)`: the condition number of $D^{-1/2}AD^{-1/2}$ with $D = \mathrm{diag}(A)$, the matrix Jacobi-preconditioned CG effectively sees.

The tests find plain CG hitting its limit on a system with condition number near $10^8$, and Jacobi-preconditioned CG finishing in under 100 iterations.

## Hints

1. Scaling the variables by $D$ multiplies the condition number by up to the square of $D$'s spread; Jacobi divides that scaling back out.
2. `np.linalg.cond` gives the 2-norm condition number.
3. Good preconditioners exploit structure: incomplete factorizations, multigrid, or, for the normal equations of a regression, the scale of each feature.
