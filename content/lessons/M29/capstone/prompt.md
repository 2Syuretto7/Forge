# Capstone: an optimizer zoo with proved and measured rates

Build the optimizers, measure their rates, and hold them to the theory.

1. `gd`, `heavy_ball` and `nesterov`, each a function `(lam, x0, iters)` running on the diagonal quadratic with curvatures `lam` (minimum 0) with its optimal constants for $\mu = \min\lambda$ and $L = \max\lambda$ (e03, e04), returning the error norms.
2. `proved_rate(method, kappa)`: $\frac{\kappa - 1}{\kappa + 1}$, $\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}$ and $1 - \frac{1}{\sqrt\kappa}$.
3. `measured_rate(errors, start, stop)`: e02's log-linear fit.
4. `sgd_inverse_time(mu, sigma, eta0, k0, iters, chains, rng)`: SGD on $\frac\mu2 x^2$ with gradient noise $\sigma\xi$ and step $\eta_0 k_0/(k + k_0)$, for many chains at once from $x = 1$; return the mean squared error after every step. With $\eta_0\mu > 1$ it decays like $1/k$.
5. `bias_correction(b1, b2, t)`: the pair $(1/(1 - \beta_1^t), 1/(1 - \beta_2^t))$, and `uncorrected_mean(b1, t)`: $\mathbb{E}[m_t]/\mathbb{E}[g]$ for a stationary gradient, $1 - \beta_1^t$.

The tests require, for $\kappa \in \{10, 100, 1000\}$, each method's measured $-\log\rho$ within **15 percent** of the proved one; the SGD error's log-log slope within 15 percent of $-1$; and the bias correction verified by averaging Adam's first moment over many random gradient sequences.
