# The Marchenko-Pastur law

Draw $n$ samples of $p$ independent standard normal features and form the sample covariance $S = X^\top X/n$. Its true value is the identity, every eigenvalue 1, yet the sample eigenvalues spread out: as $n, p \to \infty$ with $p/n \to \gamma \le 1$, their histogram approaches the **Marchenko-Pastur** density (Section 6)

$$
f(\lambda) = \frac{\sqrt{(\lambda_+ - \lambda)(\lambda - \lambda_-)}}{2\pi\gamma\lambda}, \qquad \lambda_\pm = (1 \pm \sqrt\gamma)^2 .
$$

- `mp_edges(gamma)` and `mp_density(x, gamma)` (0 outside the edges; `x` may be an array).
- `sample_cov_eigs(n, p, rng)`: the eigenvalues of $S$, ascending (`np.linalg.eigvalsh`).
- `mp_moments(gamma)`: the first two moments $(1, 1 + \gamma)$, which the mean of the eigenvalues and of their squares should match.

The tests compare a histogram of 400 eigenvalues with the density, the extremes with the edges, and the moments with the formula.

## Hints

1. The mean eigenvalue is $\operatorname{tr}S/p$, which is the average squared entry of $X$: exactly 1 in expectation.
2. `np.clip` the product under the square root at 0 to avoid warnings at the edges.
3. With $\gamma = 1/4$ the eigenvalues fill $[0.25, 2.25]$: a ninefold spread from pure noise.
