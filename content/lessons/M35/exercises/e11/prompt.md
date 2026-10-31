# How sure is the frontier?

The compute-optimal $N$ at a budget far beyond the data is an extrapolation, and its uncertainty grows with the distance (Section 5). Measure it with the residual bootstrap of e07, applied to the two-dimensional fit.

- `fit_surface` and `optimal_N` are provided.
- `bootstrap_optimal_N(N, D, L, Cs, B, rng)`: fit once, then refit `B` residual-bootstrap datasets; return an array of shape `(B, len(Cs))` of $\ln N_{\text{opt}}(C)$ for each refit and budget.
- `log_interval_width(samples, level=0.9)`: for each budget, the width of the percentile interval of $\ln N_{\text{opt}}$, a multiplicative uncertainty.

The tests fit 200 runs with compute between $10^{18}$ and $10^{20}$ and find the 90 percent interval at $10^{24}$ more than twice as wide, in log terms, as at $10^{19}$, while still containing the true optimum.

## Hints

1. A width of $w$ in $\ln N$ is a factor of $e^w$ between the ends of the interval.
2. Forty bootstrap refits are enough to see the trend; more give smoother intervals.
3. Errors in the exponents multiply $\ln C$, so the interval for $\ln N_{\text{opt}}$ widens roughly linearly in $\ln C$ beyond the data.
