# Densities and cumulative distribution functions

Implement the continuous families of Section 4. Every function accepts a number or a NumPy array `x` and returns an array of the same shape.

- `uniform_pdf(x, a, b)` and `uniform_cdf(x, a, b)`.
- `exponential_pdf(x, lam)` and `exponential_cdf(x, lam)`, both 0 for $x < 0$.
- `normal_pdf(x, mu, sigma)` and `normal_cdf(x, mu, sigma)` $= \frac12\big(1 + \operatorname{erf}\frac{x - \mu}{\sigma\sqrt2}\big)$.

The tests run a **gradient check**: the derivative of each CDF, by central differences, must equal the density (Section 1: $F' = f$). They also check that each density integrates to 1.

## Hints

1. `np.clip((x - a) / (b - a), 0, 1)` is the uniform CDF.
2. Write the exponential with `np.maximum(x, 0)` inside the exponent so that negative `x` never overflows, and use `-np.expm1(-lam * x)` for $1 - e^{-\lambda x}$.
3. `math.erf` takes one number: `np.vectorize(math.erf)` applies it to an array.
