# The variance formula on both sides of the threshold

Check Section 5's exact formulas by simulation, with no signal: $y = \epsilon$, $\sigma = 1$, features standard normal.

- `variance_theory(n, p)`: $p/(n - p - 1)$ for $p < n - 1$, $n/(p - n - 1)$ for $p > n + 1$, and `inf` otherwise.
- `variance_sim(n, p, trials, seed)`: for each trial draw `X` `(n, p)` then `y` `(n,)` from one `np.random.default_rng(seed)`; fit least squares if $p < n$ and the minimum-norm interpolant if $p > n$; return the average of $\|\hat w\|^2$.

## Hints

1. Least squares: `np.linalg.lstsq(X, y, rcond=None)[0]`.
2. Minimum norm: `X.T @ np.linalg.solve(X @ X.T, y)`.
3. Heavy tails near the threshold make simulations noisy; the tests stay a few features away from it.
