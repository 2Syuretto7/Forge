# Capstone: a Monte Carlo engine with honest error bars

Build an engine that reports every estimate with a 95 percent interval, and test the intervals the only way that counts: repeat the experiment 100 times and count how often they contain the truth.

1. `interval(values, level=0.95)`: the sample mean and the CLT interval, as `(estimate, low, high)`, with the starter's `z_for(level)` (1.96 at 95 percent) and the sample standard deviation.
2. `integrate(f, a, b, n, rng)`: the integral of `f` over $[a, b]$ from `n` uniform points, drawn with one call `rng.random(n)`.
3. `expect(f, draw, n, rng)`: $\mathbb{E}f(X)$ from one call `draw(rng, n)`.
4. `tail_prob(a, n, rng)`: $P(Z > a)$ for a standard normal by importance sampling from $N(a, 1)$, drawn with one call `a + rng.standard_normal(n)`.

Items 2 to 4 return `(estimate, low, high)`. The tests run each 100 times with $n = 2{,}000$ (seeds 400 to 499) on $\int_0^1 \frac{4}{1 + x^2}dx = \pi$, on $\mathbb{E}\max(Z, 0) = 1/\sqrt{2\pi}$, and on $P(Z > 4) \approx 3.17 \times 10^{-5}$. Each must cover the truth in **at least 93 of 100 runs**, and quadrupling $n$ must halve the average width.

The count of covering runs is itself random: for a perfect 95 percent interval it is Binomial(100, 0.95), about $95 \pm 2$, and falls below 93 about one time in eight. The fixed seeds make the test repeatable; try other seed blocks to see the count move.
