# Standard errors from the Jacobian

Near the best fit the model is almost linear in $\theta$, so the linear least-squares formula carries over (Section 4): with $s^2 = \text{SSE}/(n - p)$, the estimated noise variance for $n$ points and $p$ parameters,

$$
\widehat{\operatorname{Cov}}(\hat\theta) = s^2(J^\top J)^{-1}, \qquad \operatorname{se}(\hat\theta_j) = \sqrt{\widehat{\operatorname{Cov}}_{jj}} .
$$

- `model`, `jacobian` and a fitter of your choice (Levenberg-Marquardt from e05 is safest) as `fit(x, y, theta0)`.
- `param_cov(x, y, theta)`.
- `standard_errors(x, y, theta)`.

The tests fit 300 independent noisy datasets and check that the standard error of $\alpha$ from a single fit matches the spread of the 300 fitted values within 20 percent.

## Hints

1. Divide by $n - p$, not $n$: three parameters were fitted to the same data.
2. `np.linalg.inv` is fine for a $3 \times 3$ matrix.
3. The formula assumes independent noise of equal variance; e15 shows what happens when the data are too few for it.
