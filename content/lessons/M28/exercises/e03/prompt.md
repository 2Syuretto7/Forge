# Jensen's inequality

For convex $f$, $f(\mathbb{E}X) \le \mathbb{E}f(X)$ (Section 3): the function of the average lies below the average of the function.

- `jensen_gap(f, samples, weights=None)`: $\mathbb{E}f(X) - f(\mathbb{E}X)$ for the empirical distribution of `samples` (equal weights unless `weights` is given).
- `am_gm(x)`: the pair `(arithmetic mean, geometric mean)` of positive numbers, the geometric mean computed as $\exp(\text{mean of logs})$.
- `log_mean_exp(x)`: $\log\frac1n\sum_i e^{x_i}$, stably; by Jensen it is at least the mean of $x$.

The tests check the sign of the gap for convex and concave functions, the AM-GM inequality, and that the gap of $x^2$ is the variance.

## Hints

1. With weights $w$ summing to 1: `np.sum(w * f(x)) - f(np.sum(w * x))`.
2. $-\log$ is convex; Jensen applied to it gives AM-GM.
3. Subtract the maximum before exponentiating, as in M26.
