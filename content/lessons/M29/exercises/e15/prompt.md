# Break it: too much momentum

Momentum is not "more is better". Along curvature $\lambda$, heavy ball is stable only when $0 < \alpha\lambda < 2(1 + \beta)$, and once the 2 by 2 iteration matrix has complex eigenvalues it contracts at exactly $\sqrt\beta$ per step, whatever $\alpha$ is (e05). So $\beta = 0.99$ caps the rate at $0.995$: slower than gradient descent on an easy problem.

- `heavy_ball_errors(lam, alpha, beta, iters)`: on the one-dimensional $f(x) = \frac\lambda2 x^2$ from $x_0 = x_{-1} = 1$, the list of $\lvert x_k\rvert$.
- `stable(lam, alpha, beta)`: whether $0 < \alpha\lambda < 2(1 + \beta)$ and $0 \le \beta < 1$.

The tests compare $\beta = 0.99$ with $\beta = 0$ on a well-conditioned problem and cross the stability boundary.

## Hints

1. Two variables, `x` and `prev`, as in e03.
2. Oscillation with a slowly shrinking envelope is the signature of too much momentum.
3. At $\alpha\lambda$ just above $2(1 + \beta)$ the iterates flip sign and grow.
