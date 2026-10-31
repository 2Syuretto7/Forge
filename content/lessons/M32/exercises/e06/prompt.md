# Metropolis-Hastings

The random-walk Metropolis sampler proposes $y = x + s\,z$ with $z$ standard normal and accepts with probability $\min(1, \pi(y)/\pi(x))$; on a rejection the chain repeats $x$ (Section 5). With an asymmetric proposal $q$ the Hastings correction multiplies the ratio by $q(x)/q(y)$. Work with log densities: the normalizing constant cancels, and nothing overflows.

- `rw_metropolis(log_p, x0, step, n, rng)`: `(samples, acceptance)` with `samples` of shape `(n, d)`.
- `independence_mh(log_p, sample_q, log_q, x0, n, rng, correct=True)`: proposals `y = sample_q(rng)` drawn independently of $x$; the log acceptance ratio is $\log\pi(y) - \log\pi(x) + \log q(x) - \log q(y)$, without the last two terms when `correct` is false. Returns `(samples, acceptance)` with samples a 1-D array.

The tests sample a correlated two-dimensional Gaussian, then a Gamma(3, 1) target with exponential proposals of mean 3. Without the Hastings correction the chain still converges, but to the wrong distribution, one proportional to $\pi(x)q(x)$, whose mean is $9/4$ instead of 3.

## Hints

1. Accept when `log(u) < log_p(y) - log_p(x)` for a uniform `u`; keep `log_p(x)` from the previous step rather than recomputing it.
2. Pre-draw the normal and uniform numbers in arrays.
3. A density of $-\infty$ (outside the support) is never accepted, because `log(u)` is finite.
