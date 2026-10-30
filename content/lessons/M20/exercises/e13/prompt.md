# The forgotten determinant

$X$ is a standard normal and $Y = 2X + 1$.

- `wrong_density(y)`: $p_X((y - 1)/2)$, without the Jacobian factor.
- `right_density(y)`: with it.
- `total(density, lo=-30, hi=30, n=60_000)`: the integral of a density by the midpoint rule.

The wrong one integrates to 2. Then a two-dimensional case: for the linear map $y = Ax$ of a standard normal pair,

- `linear_density(y, A)`: $p_X(A^{-1}y) / |\det A|$, with $p_X$ the standard bivariate normal density.

## Hints

1. $p_X(x) = e^{-x^2/2}/\sqrt{2\pi}$.
2. The factor for $Y = 2X + 1$ is $\frac12$.
3. `np.linalg.solve(A, y)` for $A^{-1}y$.
