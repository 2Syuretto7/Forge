# Confidence and credible intervals, judged by coverage

Three 95 percent intervals for a proportion from $k$ successes in $n$ trials:

- **Wald**: $\hat p \pm z\sqrt{\hat p(1 - \hat p)/n}$, the textbook formula.
- **Wilson**: invert the test instead of plugging in $\hat p$: center $\frac{\hat p + z^2/(2n)}{1 + z^2/n}$ and halfwidth $\frac{z}{1 + z^2/n}\sqrt{\frac{\hat p(1 - \hat p)}{n} + \frac{z^2}{4n^2}}$.
- **Credible**: the central 95 percent of the Beta($k + 1$, $n - k + 1$) posterior under a uniform prior (Section 8). The starter provides `beta_quantiles(a, b, qs)`.

Implement `wald(k, n, z=1.96)`, `wilson(k, n, z=1.96)` and `credible(k, n)`, each returning `(low, high)`, and `exact_coverage(interval, p, n)`: the probability, summed exactly over the binomial distribution of $k$, that `interval(k, n)` contains $p$.

The tests find the Wald interval covering a rare event ($p = 0.05$, $n = 20$) only about 64 percent of the time, because 36 percent of samples have $k = 0$ and a zero-width interval, while the other two stay above 90 percent.

## Hints

1. `math.comb(n, k) * p**k * (1 - p) ** (n - k)` is the probability of each $k$.
2. Coverage is a property of a procedure over repeated samples; a credible interval answers a different question, but you can still ask how often it covers.
3. With $p = 0.5$ and $n = 100$ all three are nearly the same interval.
