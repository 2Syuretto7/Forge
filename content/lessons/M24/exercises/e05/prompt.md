# The central limit theorem, checked by simulation

Measure how close standardized means are to a standard normal.

- `normal_cdf(z)`: $\Phi(z) = \tfrac{1}{2}\big(1 + \operatorname{erf}(z/\sqrt{2})\big)$, elementwise on arrays (use `math.erf` with `np.vectorize`, or a loop).
- `standardized_means(samples, mu, sigma)`: `samples` has shape `(trials, n)`; return the `trials` values $(\bar x - \mu)/(\sigma/\sqrt{n})$.
- `ks_distance(z)`: the Kolmogorov-Smirnov distance $\max_t \lvert\hat F(t) - \Phi(t)\rvert$ between the empirical CDF of `z` and $\Phi$ (M22). Evaluate at the sorted points, checking both $i/m$ and $(i-1)/m$.

The tests check that means of 30 uniform draws are close to normal, while single draws from a skewed distribution are not.

## Hints

1. Sort `z`; with $m$ points the empirical CDF jumps from $(i-1)/m$ to $i/m$ at the $i$-th point.
2. `np.max(np.maximum(np.arange(1, m+1)/m - F, F - np.arange(m)/m))` where `F = normal_cdf(sorted z)`.
3. The uniform distribution on $[0,1]$ has $\mu = 1/2$ and $\sigma = 1/\sqrt{12}$.
