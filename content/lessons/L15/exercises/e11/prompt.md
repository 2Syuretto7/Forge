# Break it: fitting too narrow a range

You have compute-optimal runs between $10^{18}$ and $10^{21}$ FLOPs and want the loss at $10^{24}$. The true frontier is $L^*(C) = E + K C^{-\gamma}$, which curves in log-log coordinates as it approaches $E$.

1. `fit_pure(C, L)`: the pure power law $L = k C^{-g}$, by a log-log line.
2. `fit_floor(C, L, grid=400)`: $L = E + k C^{-g}$: for each $E$ in `np.linspace(0, min(L) * (1 - 1e-6), grid + 1)`, fit $\log(L - E)$ by a line and keep the $E$ with the smallest squared error. Return $(E, k, g)$.
3. `extrapolation_errors(C, L, target_C, target_L)`: the relative errors (prediction / truth − 1) of both fits at `target_C`.

## Hints

1. `np.polyfit(x, y, 1, full=True)` also returns the sum of squared residuals.
2. A straight line cannot bend toward a floor, so the pure fit keeps falling at the same log-log slope.
3. With no floor the pure fit predicts too low a loss: it is optimistic.
