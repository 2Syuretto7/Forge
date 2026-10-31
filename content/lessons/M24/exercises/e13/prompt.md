# Break it: a proposal with lighter tails than the target

Importance sampling needs the proposal to reach everywhere the target does, with tails at least as heavy. Estimate $\mathbb{E}[X^2] = 2$ for the Laplace density $p(x) = \frac12 e^{-\lvert x\rvert}$ with two proposals: the standard normal, whose tails fall like $e^{-x^2/2}$, and the Laplace density with scale 2.

- `laplace_logpdf(x, b=1.0)`: $-\lvert x\rvert/b - \log(2b)$.
- `laplace_sample(b, n, rng)`: inverse-CDF sampling from one call `rng.random(n)`, as in M22.
- `is_run(proposal, n, rng)`: draw `n` samples from `"normal"` (one call `rng.standard_normal(n)`) or `"laplace2"`, and return the estimate of $\mathbb{E}_p[X^2]$, its standard error, and the effective sample size as a fraction of `n`.

The tests repeat each 50 times. With the normal proposal the weights $p/q$ grow like $e^{x^2/2 - \lvert x\rvert}$ and have infinite variance: the estimates usually fall short of 2, the error bars lie, and fewer than 70 percent of the intervals cover the truth. With the heavier proposal more than 85 percent do.

## Hints

1. For $u < \frac12$, $x = b\log(2u)$; otherwise $x = -b\log(2(1 - u))$.
2. Reuse the logic of e07 for the estimate and e07's `ess` divided by $n$.
3. A quarter of $\mathbb{E}[X^2]$ under the Laplace density comes from $\lvert x\rvert > 4$, where the normal proposal almost never looks.
