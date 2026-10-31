# The Marchenko-Pastur law at scale

Test the law with a goodness-of-fit statistic instead of a picture. The **Kolmogorov-Smirnov distance** between the empirical distribution of the eigenvalues and the Marchenko-Pastur distribution is the largest gap between their cumulative distribution functions (Section 6).

- `mp_cdf(x, gamma)`: the Marchenko-Pastur CDF at the points `x`, by numerical integration of the density on a fine grid (e07's density, rewritten here).
- `ks_distance(eigs, gamma)`: $\max_i\max\left(\left\lvert F(\lambda_{(i)}) - \frac ip\right\rvert, \left\lvert F(\lambda_{(i)}) - \frac{i - 1}p\right\rvert\right)$ for the sorted eigenvalues $\lambda_{(1)} \le \dots \le \lambda_{(p)}$.
- `ks_for_sizes(sizes, gamma, rng)`: the KS distance for each $p$ in `sizes`, with $n = p/\gamma$.

The tests find the distance below 0.03 at $p = 500$ and shrinking as the matrices grow, while a sample covariance whose features have unequal variances fails the test.

## Hints

1. Build the CDF once on a grid with a cumulative trapezoid sum, normalize its last value to 1, and interpolate with `np.interp`.
2. The empirical CDF jumps by $1/p$ at each eigenvalue; compare both sides of each jump.
3. The KS distance of a correct law shrinks with $p$; a wrong law leaves a gap that does not.
