# Measuring a rate by a log-linear fit

If $e_k \approx C\rho^k$, then $\log e_k \approx \log C + k\log\rho$: a straight line in $k$ whose slope is $\log\rho$ (Section 5). Fitting it over a window that skips the transient and stops before rounding noise gives the measured rate.

- `fit_rate(errors, start, stop)`: least-squares slope of $\log e_k$ against $k$ for $k$ in `range(start, stop)`, returned as $\rho = e^{\text{slope}}$.
- `iterations_for(rho, factor)`: the steps needed to shrink the error by `factor`, $\lceil\log(\text{factor})/(-\log\rho)\rceil$.
- `half_life(rho)`: the steps that halve the error, $\log 2/(-\log\rho)$.

## Hints

1. `np.polyfit(k, np.log(e), 1)[0]` is the slope.
2. A rate of $0.99$ has a half-life of about 69 steps; $0.9$ of about 6.6.
3. Choose the window by looking: a log plot shows where the line is straight.
