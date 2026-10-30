# How a density transforms

- `transformed_density(p_x, g_inv, g_inv_prime)`: return the function $y \mapsto p_X(g^{-1}(y))\,|(g^{-1})'(y)|$.
- `density_of_square(y)`: the density of $Y = X^2$ for $X$ uniform on $[0, 1]$, for $0 < y \leq 1$.
- `density_of_neglog(y)`: the density of $Y = -\ln X$ for $X$ uniform on $(0, 1]$, for $y \geq 0$.
- `lognormal_density(y)`: the density of $Y = e^Z$ for a standard normal $Z$, for $y > 0$.

The tests run a **gradient check**: the derivative of each distribution function, $P(Y \leq y) = P(X \leq g^{-1}(y))$ computed through $X$, matches your density; and each integrates to 1.

## Hints

1. Return a closure.
2. $g^{-1}(y) = \sqrt y$, $e^{-y}$, $\ln y$ respectively.
3. The standard normal density is $e^{-z^2/2}/\sqrt{2\pi}$.
