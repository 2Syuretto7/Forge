# The Rayleigh quotient and its gradient

For symmetric `S` and nonzero `x`, $\rho(x) = \frac{x^\top S x}{x^\top x}$ (M13). By the quotient rule,

$$
\nabla \rho(x) = \frac{2}{x^\top x}\big(Sx - \rho(x)\,x\big),
$$

which vanishes exactly at eigenvectors.

- `rayleigh(S, x)` and `rayleigh_grad(S, x)`.
- `ascend(S, x0, lr, steps)`: gradient ascent on $\rho$, renormalizing $x$ to unit length after each step; return the final unit vector.

The tests run a **gradient check** and show the ascent reaching the top eigenvector.

## Hints

1. The numerator's gradient is $2Sx$ and the denominator's $2x$.
2. $\rho(cx) = \rho(x)$, so renormalizing does not change the objective.
3. With `lr` around $1/\lambda_{\max}$, a few thousand steps suffice.
