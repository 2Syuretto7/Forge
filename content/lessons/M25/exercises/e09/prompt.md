# Two coins, settled

Coin A lands heads 3 times in 4 and coin B 6 times in 10. Which is more likely to have the higher bias? With uniform priors, coin A (3 heads in 4) has posterior $\text{Beta}(4, 2)$ and coin B (6 in 10) has $\text{Beta}(7, 5)$. Compute $P(\theta_A > \theta_B)$ two ways.

- `beta_logpdf(t, a, b)`: the log density on an array of points in $(0, 1)$, using `math.lgamma` for the normalizer $\log B(a, b) = \log\Gamma(a) + \log\Gamma(b) - \log\Gamma(a + b)$.
- `prob_a_better_grid(ka, na, kb, nb, m)`: numerical integration of $\int_0^1 p_A(t)\, F_B(t)\, dt$ on `m` grid points (midpoints of $[0, 1]$ split into `m` cells), with $F_B$ the cumulative sum of $p_B$ times the cell width.
- `prob_a_better_mc(ka, na, kb, nb, draws, seed)`: draw from both posteriors with one `np.random.default_rng(seed)` (A first, then B) and return the fraction of draws where A's value is larger.

## Hints

1. Midpoints: `t = (np.arange(m) + 0.5) / m`, cell width `1/m`.
2. For a slightly better integral, use the CDF at the cell midpoint: `np.cumsum(pB) * h - 0.5 * pB * h`.
3. The answer is about 0.65.
