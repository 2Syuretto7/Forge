# A 50-dimensional posterior

Bayesian linear regression with 50 weights: data $y = Xw + \text{noise}$ with noise standard deviation $\sigma$, and a prior $w \sim N(0, \tau^2I)$. The log posterior, up to a constant, is $-\frac{\lVert y - Xw\rVert^2}{2\sigma^2} - \frac{\lVert w\rVert^2}{2\tau^2}$. This posterior is Gaussian with a known answer, which lets you grade a sampler that does not know it (Section 5).

- `log_posterior(w, X, y, sigma=1.0, tau=1.0)` and `grad_log_posterior(...)` $= X^\top(y - Xw)/\sigma^2 - w/\tau^2$.
- `exact_posterior(X, y, sigma=1.0, tau=1.0)`: `(mean, cov)` with $\Sigma = (X^\top X/\sigma^2 + I/\tau^2)^{-1}$ and mean $\Sigma X^\top y/\sigma^2$.
- `rw_chain(log_p, x0, step, n, rng)`: random-walk Metropolis as in e06, returning `(samples, acceptance)`.
- `tune_rw(log_p, x0, rng, step=0.1, target=0.234, rounds=30, per_round=200)`: run `rounds` short chains, each starting where the last ended, and after each multiply the step by $e^{2(\text{acceptance} - \text{target})}$. Return `(step, x)`, the tuned step and the final state.

The tests run a **gradient check**, then tune, run 20,000 steps, and compare the chain's mean with the exact posterior mean in units of posterior standard deviations. The tuned acceptance is near 0.234, the optimum for random-walk proposals in high dimensions.

## Hints

1. The exact mean is where the gradient vanishes: a good check of both functions.
2. Too many acceptances means the step is too small, so the update raises it; too few lowers it.
3. The tuned step comes out near $2.38/\sqrt d$ times the posterior's scale.
