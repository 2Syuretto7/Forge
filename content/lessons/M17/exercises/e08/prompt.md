# Probabilities, means and medians as integrals

For a density `pdf` on $[a, b]$ (use Simpson's rule with 2,000 strips, provided as `simpson`):

- `prob_between(pdf, lo, hi)`: $\int_{lo}^{hi} p$.
- `mean(pdf, a, b)`: $\int_a^b x\,p(x)\,dx$.
- `variance(pdf, a, b)`: $\int_a^b (x - \mu)^2 p(x)\,dx$.
- `quantile(pdf, a, b, q)`: the $x$ with $\int_a^x p = q$, by bisection on $[a, b]$ to $10^{-10}$.

For the puzzle's density $6x(1 - x)$: probability $0.112$ on $[0.2, 0.3]$, mean $1/2$, variance $1/20$, median $1/2$.

## Hints

1. Each is one call to `simpson` with the right integrand.
2. The variance needs the mean first.
3. The cumulative probability increases with $x$, so bisection applies.
