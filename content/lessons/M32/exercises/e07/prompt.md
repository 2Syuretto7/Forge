# Gibbs sampling

Gibbs sampling updates one coordinate at a time from its conditional distribution given the others. Each update is a Metropolis-Hastings step whose acceptance probability is exactly 1 (Section 6). For a Gaussian with mean $\mu$ and precision $\Lambda = \Sigma^{-1}$, coordinate $i$ given the rest is normal with variance $1/\Lambda_{ii}$ and mean $\mu_i - \frac1{\Lambda_{ii}}\sum_{j \ne i}\Lambda_{ij}(x_j - \mu_j)$.

- `gibbs_bivariate(rho, n, rng)`: $n$ sweeps for the standard bivariate normal with correlation $\rho$, starting at $(0, 0)$; each sweep draws $x \mid y \sim N(\rho y, 1 - \rho^2)$, then $y \mid x$. Returns an array of shape `(n, 2)`.
- `lag1(x)`: the lag-one autocorrelation of a sequence.
- `gibbs_gaussian(mu, cov, n, rng)`: $n$ systematic sweeps through all coordinates of a $d$-dimensional Gaussian, from $x = \mu$. Returns `(n, d)`.

The tests check the samples' correlation, and the fact that the $x$ chain of the bivariate sampler is an AR(1) sequence with lag-one autocorrelation $\rho^2$: at $\rho = 0.99$ it barely moves.

## Hints

1. After one sweep $x_{t+1} = \rho y_t + \text{noise}$ and $y_t = \rho x_t + \text{noise}$, so $x_{t+1} = \rho^2x_t + \text{noise}$.
2. Pre-draw the standard normals; scale by $\sqrt{1 - \rho^2}$.
3. In the general sampler, compute $\Lambda$ once with `np.linalg.inv`.
