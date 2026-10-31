# Water-filling across 100,000 channels

Allocate a power budget $P$ across channels with noise levels $n_i$ to maximize $\sum_i\log(1 + x_i/n_i)$ subject to $\sum_i x_i = P$ and $x_i \ge 0$. The KKT conditions give $x_i = \max(0, \nu - n_i)$ for a single water level $\nu$: pour power until the water reaches the same height everywhere it is poured (Section 2).

- `allocation(noise, nu)`: $\max(0, \nu - n_i)$.
- `water_level(noise, P)`: the $\nu$ with $\sum_i\max(0, \nu - n_i) = P$, by bisection between $\min n$ and $\min n + P$.
- `kkt_check(noise, x, nu)`: the largest violation of the KKT conditions with multiplier $\mu_i = 1/\nu - 1/(n_i + x_i) \ge 0$ on each $x_i \ge 0$: stationarity holds by construction, so check $\mu_i \ge 0$ and $\mu_i x_i = 0$, and the budget.

The tests use $10^5$ channels from the starter's `make_noise()` and require the budget met to $10^{-9}$ and the KKT residual below $10^{-9}$.

## Hints

1. The total $\sum\max(0, \nu - n_i)$ increases with $\nu$: bisection works.
2. Channels with $n_i \ge \nu$ get nothing; their multiplier is positive.
3. The objective's derivative in $x_i$ is $1/(n_i + x_i)$; stationarity reads $1/(n_i + x_i) = 1/\nu - \mu_i$.
