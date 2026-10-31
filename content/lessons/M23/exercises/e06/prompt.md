# Conditioning a Gaussian

Split a Gaussian vector into unobserved coordinates $a$ and observed coordinates $b$. Given $x_b$, the rest is Gaussian with (Section 5)

$$
\mu_{a \mid b} = \mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(x_b - \mu_b), \qquad \Sigma_{a \mid b} = \Sigma_{aa} - \Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba} .
$$

- `condition(mu, Sigma, obs, x_obs)`: `obs` is a list of observed indices; return the conditional mean and covariance of the other coordinates, in increasing index order.
- `regression_slope(mu, Sigma, obs)`: the matrix $\Sigma_{ab}\Sigma_{bb}^{-1}$ by which the conditional mean moves per unit of $x_b$.

The tests run a **gradient check**: the derivative of the conditional mean with respect to the observed values, by differences, must equal `regression_slope`. They also compare with the bivariate formula and with a simulation that keeps only samples whose observed coordinate lands near the given value.

## Hints

1. `rest = [i for i in range(d) if i not in obs]`, then `Sigma[np.ix_(rest, obs)]`.
2. `np.linalg.solve(Sbb, Sba)` instead of an inverse.
3. The conditional covariance does not depend on the observed value, only on which coordinates are observed.
