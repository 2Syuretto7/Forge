# Momentum by eigen-analysis

Along an eigenvector with curvature $\lambda$, heavy ball is a two-term recurrence, $e_{k+1} = (1 + \beta - \alpha\lambda)e_k - \beta e_{k-1}$, or in matrix form

$$
\begin{pmatrix} e_{k+1} \\ e_k \end{pmatrix} = \begin{pmatrix} 1 + \beta - \alpha\lambda & -\beta \\ 1 & 0 \end{pmatrix}\begin{pmatrix} e_k \\ e_{k-1} \end{pmatrix} ,
$$

and the error decays like the **spectral radius** of that matrix, the largest eigenvalue modulus (M13). The method's rate on $[\mu, L]$ is the worst spectral radius over the curvatures in that range (Section 2).

- `momentum_matrix(lam, alpha, beta)` and `spectral_radius(M)`.
- `worst_radius(alpha, beta, mu, L, n=200)`: the largest spectral radius over `n` curvatures spread evenly in $[\mu, L]$.
- `best_beta(alpha, mu, L, betas)`: the momentum in `betas` with the smallest worst radius.

The tests find the optimal momentum numerically and match the formula of e03, and show that every curvature then contracts at the same rate $\sqrt\beta$.

## Hints

1. `np.max(np.abs(np.linalg.eigvals(M)))`.
2. When the eigenvalues of the 2 by 2 matrix are complex, their modulus is $\sqrt\beta$ whatever $\lambda$ is: that is the equalization the optimum achieves.
3. Include both ends, $\mu$ and $L$, in the grid.
