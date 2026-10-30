# Ten million samples, streamed

Ten million float64 numbers take 80 MB. Stream them instead: draw a million at a time, summarize each chunk by its count, mean and sum of squared deviations $M_2$, and merge the summaries. For chunks $a$ and $b$ with $\delta = \bar x_b - \bar x_a$ and $n = n_a + n_b$,

$$
\bar x = \bar x_a + \delta\,\frac{n_b}{n}, \qquad M_2 = M_{2,a} + M_{2,b} + \delta^2\,\frac{n_a n_b}{n} .
$$

- `chunk_stats(x)`: the triple `(n, mean, M2)` of an array.
- `merge(a, b)`: the triple of the union of two chunks; an empty chunk is `(0, 0.0, 0.0)`.
- `streaming_moments(draw, n, chunk=10**6)`: call `draw(k)` repeatedly for `k` samples at a time until `n` are drawn; return the mean and the variance $M_2/(n - 1)$.
- `mean_se(var, n)` $= \sqrt{\text{var}/n}$ and `var_se(var, m4, n)` $= \sqrt{(\mu_4 - \text{var}^2)/n}$: the predicted standard errors of the sample mean and sample variance, where $\mu_4 = \mathbb{E}(X - \mu)^4$.

The tests stream $10^7$ draws of Exponential(1) and Uniform(0, 1) and require both moments within 4 standard errors of the truth.

## Hints

1. Check `merge` against `np.var(x, ddof=1)` on a small array split unevenly.
2. Merging with an empty chunk must return the other chunk unchanged; the formulas do that when $n_a = 0$.
3. For Exponential(1), $\mu_4 = 9$; for Uniform(0, 1), $\mu_4 = 1/80$.
