# Control variates

If $g(X)$ has a known mean and moves with $f(X)$, subtract its fluctuation: $f(X) + c\,(g(X) - \mathbb{E}g)$ has the same mean as $f(X)$ for every $c$, and the smallest variance at $c = -\operatorname{Cov}(f, g)/\operatorname{Var}(g)$, where the variance shrinks by the factor $1 - \rho^2$.

- `control_variate(fx, gx, g_mean)`: from paired samples, estimate $c$, form the adjusted values, and return `(estimate, standard_error, c)`.
- `plain(fx)`: the ordinary estimate and standard error, for comparison.

The tests estimate $\mathbb{E}e^U = e - 1$ for $U$ uniform on $[0, 1]$ with $g(U) = U$, whose correlation with $e^U$ is $0.99$: the error bar shrinks about eightfold, worth sixty times the samples.

## Hints

1. `np.cov(fx, gx)` returns the 2 by 2 sample covariance matrix.
2. Estimating $c$ from the same samples adds a tiny bias, negligible for thousands of samples.
3. The variance falls by $1 - \rho^2$, so the standard error by $\sqrt{1 - \rho^2}$.
