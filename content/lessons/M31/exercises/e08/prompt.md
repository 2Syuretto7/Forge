# Rademacher complexity of a linear class

The empirical **Rademacher complexity** of a class measures how well it can fit random signs $\sigma_i = \pm 1$ on the sample: $\hat{\mathcal R} = \mathbb{E}_\sigma\sup_h\frac1n\sum_i\sigma_ih(x_i)$ (Section 3). For linear functions with $\lVert w\rVert \le B$, the supremum has a closed form, $\frac Bn\lVert\sum_i\sigma_ix_i\rVert$, and Jensen's inequality bounds its expectation by $\frac Bn\sqrt{\sum_i\lVert x_i\rVert^2}$.

- `rademacher_linear(X, B, draws, rng)`: the Monte Carlo average of $\frac Bn\lVert\sum_i\sigma_ix_i\rVert$ over `draws` sign vectors.
- `rademacher_bound(X, B)`: the Jensen bound.

The tests check the estimate against the bound, its $1/\sqrt n$ decay, and its independence from the input dimension when the points have unit norm.

## Hints

1. Signs: `rng.choice([-1.0, 1.0], size=(draws, n))`, then `S @ X` gives all the sums at once.
2. The bound is tight up to a constant close to 1 for many points.
3. A class that can fit random signs well can also fit noise: that is what the complexity measures.
