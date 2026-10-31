# Bootstrap intervals for a fit

The Jacobian formula is a linear approximation. The **residual bootstrap** makes none (Section 4): keep the fitted curve, resample its residuals with replacement, add them back to make a new dataset, refit, and repeat. The spread of the refitted parameters estimates their uncertainty, and their percentiles give intervals (M25).

- `model`, `jacobian`, `fit` as in e06.
- `residual_bootstrap(x, y, theta_hat, B, rng)`: an array of shape `(B, 3)` of refits, each started from `theta_hat`.
- `percentile_interval(samples, level=0.95)`: the lower and upper percentiles of each column, as two arrays.

The tests compare the bootstrap standard deviation of $\alpha$ with the Jacobian standard error, and check that the interval contains the true value.

## Hints

1. `rng.choice(residuals, size=n, replace=True)`.
2. Start each refit at `theta_hat`: it is close, so Levenberg-Marquardt converges in a few steps.
3. `np.quantile(samples, [0.025, 0.975], axis=0)`.
