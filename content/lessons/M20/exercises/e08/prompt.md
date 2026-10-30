# Inverse-CDF sampling

If $F$ is a continuous distribution function and $U$ is uniform, $F^{-1}(U)$ has distribution $F$: the change of variables with $g = F^{-1}$ gives density $1 / (F^{-1})'(u) = F'(x)$.

- `sample_exponential(n, rate, seed=0)`: $-\ln(1 - U)/\text{rate}$.
- `sample_cauchy(n, seed=0)`: $\tan(\pi(U - \tfrac12))$.
- `sample_from_table(xs, cdf_values, n, seed=0)`: for a tabulated increasing CDF, invert by linear interpolation (`np.interp(u, cdf_values, xs)`).

The tests compare sample quantiles with exact ones.

## Hints

1. Use `rng.random(n)`.
2. The median of the exponential is $\ln 2/\text{rate}$; the quartiles of the Cauchy are $\pm 1$.
3. The tests tabulate the Beta(2, 2) distribution function $3x^2 - 2x^3$.
