# Power laws and scale invariance

A power law $f(x) = Ax^{-\alpha}$ looks the same at every scale: multiplying $x$ by $c$ multiplies $f$ by $c^{-\alpha}$, whatever $x$ was (Section 1). On log-log axes it is a straight line with slope $-\alpha$, because $\log f = \log A - \alpha\log x$.

- `power_law(x, A, alpha)`.
- `loglog_slope(x1, y1, x2, y2)`: the slope between two points on log-log axes.
- `scale_factor(alpha, c)`: $c^{-\alpha}$, the factor by which the law changes when $x$ is multiplied by $c$.
- `is_scale_invariant(f, xs, c, tol=1e-9)`: whether $f(cx)/f(x)$ is the same for every $x$ in `xs`.

The tests check that a power law passes the scale-invariance test and an exponential fails it, and that every tenfold increase of compute cuts a loss term with $\alpha = 0.3$ by the same factor, about half.

## Hints

1. Use `math.log`; the base cancels in a slope.
2. For an exponential $e^{-x}$ the ratio $f(cx)/f(x) = e^{-(c - 1)x}$ depends on $x$.
3. $10^{-0.3} \approx 0.50$.
