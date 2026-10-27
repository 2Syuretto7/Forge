# The Rayleigh quotient and its gradient

For symmetric `S` and nonzero `x`, the Rayleigh quotient is $\rho(x) = \dfrac{x^\top S x}{x^\top x}$. Section 5 showed that its gradient is

$$
\nabla \rho(x) = \frac{2}{x^\top x}\big(Sx - \rho(x)\, x\big),
$$

which vanishes exactly at eigenvectors.

- `rayleigh(S, x)` returns a float.
- `rayleigh_grad(S, x)` returns shape `(n,)`.
- `ascend(S, x0, lr, steps)`: gradient ascent on $\rho$, renormalizing $x$ to unit length after each step. Return the final unit vector.

## Hints

1. Use the quotient rule: numerator $x^\top S x$ has gradient $2Sx$; denominator $x^\top x$ has gradient $2x$.
2. Because $\rho(cx) = \rho(x)$, renormalizing does not change the objective.
3. With `lr` around $1/\lambda_{\max}$, a few hundred steps reach the top eigenvector.
