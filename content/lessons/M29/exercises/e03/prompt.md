# Heavy-ball momentum

Polyak's heavy ball adds a fraction of the last step to the next: $x_{k+1} = x_k - \alpha\nabla f(x_k) + \beta(x_k - x_{k-1})$ (Section 2). On a quadratic with curvatures in $[\mu, L]$ the best constants are

$$
\alpha^\star = \frac{4}{(\sqrt L + \sqrt\mu)^2}, \qquad \beta^\star = \left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^2 ,
$$

and the error then shrinks by $\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}$ per step instead of gradient descent's $\frac{\kappa - 1}{\kappa + 1}$.

- `heavy_ball(A, b, x0, alpha, beta, iters)`: error norms $\lVert x_k - x^\star\rVert$ for $k = 0, \dots,$ `iters` on $\frac12 x^\top A x - b^\top x$, starting with $x_{-1} = x_0$.
- `optimal_heavy_ball(L, mu)`: the pair $(\alpha^\star, \beta^\star)$.

The tests measure the rate with e02's fit and compare iteration counts with gradient descent at $\kappa = 100$: about ten times fewer.

## Hints

1. Keep the previous iterate in a variable; the first step is plain gradient descent.
2. The convergence has a factor of $k$ in front of $\rho^k$ (a double eigenvalue), so fit over a window after the transient and before the error reaches rounding level, about $10^{-15}$ of its start.
3. Gradient descent's best step is $2/(L + \mu)$.
