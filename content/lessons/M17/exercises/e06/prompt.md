# Normalizing densities

An unnormalized density $g \geq 0$ becomes a probability density after dividing by its total area $Z = \int g$.

- `normalizer(g, a, b, n=2000)`: $Z$ by Simpson's rule on $[a, b]$.
- `make_pdf(g, a, b)`: the function $g(x)/Z$.
- `make_cdf(g, a, b, n=2000)`: the function $x \mapsto \int_a^x g / Z$ (Simpson's rule on $[a, x]$ with `n` strips).
- `beta_normalizer(alpha, beta)`: the exact $B(\alpha, \beta) = \Gamma(\alpha)\Gamma(\beta)/\Gamma(\alpha + \beta)$ with `math.gamma`, the area under $x^{\alpha - 1}(1 - x)^{\beta - 1}$.

The tests include a **gradient check**: the derivative of the cumulative distribution, by central differences, is the density.

## Hints

1. Use your Simpson rule from e02, or write it again for scalar functions.
2. The Gaussian $e^{-x^2/2}$ on $[-10, 10]$ has $Z = \sqrt{2\pi}$ to many digits.
3. For $\alpha = 2, \beta = 2$, $B = 1/6$, so the density is $6x(1 - x)$, the puzzle's.
