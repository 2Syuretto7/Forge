# Inverse-CDF sampling and the slope of a quantile

Section 5 shows that $F^{-1}(U)$ has CDF $F$. Implement it for three distributions, with their densities.

- `laplace_pdf(x, b)` $= \frac{1}{2b} e^{-|x|/b}$ and `laplace_quantile(u, b)`: $b\log(2u)$ for $u < \frac12$, $-b\log(2(1 - u))$ otherwise.
- `cauchy_pdf(x)` $= \frac{1}{\pi(1 + x^2)}$ and `cauchy_quantile(u)` $= \tan(\pi(u - \frac12))$.
- `pareto_pdf(x, alpha, xm)` $= \alpha x_m^\alpha / x^{\alpha + 1}$ for $x \ge x_m$, and `pareto_quantile(u, alpha, xm)` $= x_m (1 - u)^{-1/\alpha}$.

All functions accept arrays. The tests run a **gradient check**: differentiating $F(F^{-1}(u)) = u$ gives $\frac{d}{du}F^{-1}(u) = 1/f(F^{-1}(u))$, so the quantile's slope by central differences must match one over the density. They also check the samples' CDF and the Pareto mean $\alpha x_m/(\alpha - 1)$.

## Hints

1. `np.where(u < 0.5, ..., ...)` evaluates both branches; wrap the logarithms' arguments in `np.maximum(..., 1e-300)` or use `np.minimum` to keep both finite.
2. The slope of a quantile is large where the density is small: samples spread out where probability is thin.
3. Feed the quantiles evenly spaced $u$ to see the shape without randomness.
