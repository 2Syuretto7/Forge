# Variance as the dimension grows

Estimate the gradient of $\mathbb{E}\lVert x\rVert^2$ with respect to the first coordinate of the mean, for $x \sim N(\mu, I_d)$, with 10,000 samples (Section 4). At $\mu = 0$ the exact gradient is 0 and the per-sample variances are known in closed form: $(d + 2)(d + 4)$ for the score function, $2d + 8$ for the score function with the baseline $b = \mathbb{E}\lVert x\rVert^2 = d$, and $4$ for reparameterization.

- `score_estimates(d, n, rng, baseline=False)`: $n$ single-sample estimates $(\lVert x\rVert^2 - b)(x_1 - \mu_1)$ at $\mu = 0$.
- `reparam_estimates(d, n, rng)`: $2x_1$.
- `variance_table(ds, n, rng)`: a dict from $d$ to the three sample variances `(score, baseline, reparam)`.
- `theory(d)`: the three exact values.

The tests compare all three with theory for $d$ from 1 to 256: the score function's variance grows like $d^2$, the baseline's like $d$, and reparameterization's not at all.

## Hints

1. Sample an $n \times d$ matrix of standard normals once per $d$.
2. The score function sees $\lVert x\rVert^2$, a sum of $d$ noisy terms, multiplied by $x_1$; only one of the $d$ terms carries signal about $\mu_1$.
3. The EstimatorVariance widget plots the same curves.
