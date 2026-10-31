# Nesterov's accelerated gradient

Nesterov evaluates the gradient at a look-ahead point: $y_k = x_k + \beta(x_k - x_{k-1})$, then $x_{k+1} = y_k - \alpha\nabla f(y_k)$. With $\alpha = 1/L$ and $\beta = \frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}$, on a $\mu$-strongly convex $L$-smooth function the error shrinks like $(1 - 1/\sqrt\kappa)^k$, and unlike heavy ball the guarantee holds beyond quadratics (Section 2).

- `nesterov(grad, x0, alpha, beta, iters)`: the list of iterates.
- `ridge_logistic(lam)`: the pair `(f, grad)` for logistic regression plus $\frac\lambda2\lVert w\rVert^2$ on the starter's data `X`, `Y`; it is $\lambda$-strongly convex.

The tests compare Nesterov with gradient descent on the regularized logistic loss, a non-quadratic problem: to reach the same accuracy Nesterov needs several times fewer steps.

## Hints

1. With $\beta = 0$ the method is gradient descent with step $\alpha$.
2. $L \le \lambda_{\max}(X^\top X)/(4n) + \lambda$ and $\mu = \lambda$.
3. Measure accuracy against a long run of either method.
