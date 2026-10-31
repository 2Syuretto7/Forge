# A score from data: kernels and score matching

Without the target's formula, estimate the score from 300 training samples (Section 8). The simplest estimator replaces the data distribution by a kernel density estimate with bandwidth $h$: each training point becomes a small Gaussian. Its noised version is again a mixture, with centres $e^{-t}c_i$ and variance $h^2e^{-2t} + 1 - e^{-2t}$, so its score is exact and cheap. Choose $h$ by denoising score matching on held-out samples: the bandwidth whose score best predicts $-\varepsilon/\sigma$ is the one that generalizes.

- `kde_score(X, t, centres, h)`: the score of the noised kernel density estimate at points `X` of shape `(n, 2)`.
- `dsm_loss(score, x0, rng, T=5.0, n_t=8)`: the average over `n_t` times, geometrically spaced from 0.01 to $T$, of $\mathbb{E}\lVert\sigma s(x_t, t) + \varepsilon\rVert^2$ on the samples `x0` (the weighting by $\sigma^2$ puts all times on the same scale).
- `choose_bandwidth(train, valid, hs, rng)`: the $h$ in `hs` with the smallest held-out loss.

The tests find that $h = 0$, which makes the estimate the empirical distribution itself, scores worse on held-out data than a bandwidth near 0.1 to 0.2.

## Hints

1. With $h = 0$ the formula still works: the components are points that the noise has blurred.
2. Use the same random numbers for every bandwidth (pass a fresh generator with the same seed), so the comparison is not noise.
3. A training-set loss would always prefer $h = 0$: it is the exact minimizer of the empirical objective, which is memorization.
