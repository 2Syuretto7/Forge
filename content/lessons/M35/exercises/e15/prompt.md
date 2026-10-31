# Break it: five runs

The puzzle's five runs are too few for normal-theory error bars. Take the simplest case, a pure power law with multiplicative noise fitted by least squares in log space, a straight line with 2 parameters. Its prediction interval at a new point $u_0 = \log x_0$ has half-width $q\cdot s\sqrt{1 + \frac1n + \frac{(u_0 - \bar u)^2}{\sum_i(u_i - \bar u)^2}}$ (Section 5). With many runs, $q = 1.96$ gives 95 percent coverage; with $n = 5$ the noise level $s$ is itself estimated from 3 degrees of freedom, and the right multiplier is Student's $t$ quantile, $q = 3.182$.

- `line_fit(u, v)`: intercept, slope and $s$ (residual standard deviation with $n - 2$ in the denominator).
- `prediction_half_width(u, s, u0, q)`.
- `coverage(n, q, u0, trials, rng, sigma=0.05)`: simulate `trials` datasets of `n` runs at evenly spaced $u$ in $[0, \ln 100]$, fit, and return the fraction of trials in which a fresh observation at `u0` falls within the interval.

The tests extrapolate to $x_0 = 10^4$, a hundred times beyond the last run: with 5 runs, $q = 1.96$ covers well under 90 percent of the time and $q = 3.182$ about 95 percent; with 50 runs both are close to 95 percent.

## Hints

1. Write the fit with sums: slope $= \sum(u_i - \bar u)(v_i - \bar v)/\sum(u_i - \bar u)^2$.
2. The new observation has its own noise, hence the 1 under the square root.
3. Student's quantile for $\nu$ degrees of freedom is 12.71 for $\nu = 1$, 4.30 for 2, 3.18 for 3, and approaches 1.96 as $\nu$ grows.
