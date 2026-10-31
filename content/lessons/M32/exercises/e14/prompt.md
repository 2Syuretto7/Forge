# Break it: steps too small, steps too large

Random-walk Metropolis works for every step size in theory and for few in practice. Tiny steps are almost always accepted and crawl; huge steps are almost always rejected and stand still. Both produce long runs of nearly identical samples, and an effective sample size close to nothing (Section 7).

- `rw_standard_normal(step, d, n, rng)`: random-walk Metropolis on the standard normal in $d$ dimensions from $x = 0$; return `(samples, acceptance)`.
- `ess(x)`: as in e08.
- `ess_for_step(step, d, n, rng)`: `(acceptance, ess of the first coordinate)`.
- `best_step(steps, d, n, rng)`: the step in `steps` with the largest `ess_for_step`.
- `mode_fraction(sep, step, n, rng)`: run random-walk Metropolis on the provided two-peaked target from $x = -\text{sep}/2$ and return the fraction of samples with $x > 0$. The target puts half its mass there.

The tests find the effective sample size collapsing at both extremes, the best step near $2.38/\sqrt d$, and a chain that never finds the second peak when the peaks are 12 standard deviations apart.

## Hints

1. Use `-0.5 * x @ x` as the log density; the normalizing constant cancels.
2. Pre-draw the random numbers for speed.
3. No step size fixes well-separated peaks: a step large enough to jump between them is rejected almost everywhere else.
