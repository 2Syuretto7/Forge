# Gradient descent on a smooth convex function

For an $L$-smooth function, a step of $1/L$ decreases the value by at least $\frac{1}{2L}\lVert\nabla f\rVert^2$ (the **descent lemma**, Section 1), and on a convex function the gap to the optimum after $k$ steps is at most $\frac{L\lVert x_0 - x^\star\rVert^2}{2k}$.

Take ridge-free logistic regression, $f(w) = \frac1n\sum_i[\operatorname{softplus}(x_i^\top w) - y_i x_i^\top w]$, whose smoothness is at most $\lambda_{\max}(X^\top X)/(4n)$ (M28).

- `loss(w, X, y)` and `grad(w, X, y)`.
- `gd(X, y, w0, step, iters)`: the list of iterates $w_0, \dots, w_{\text{iters}}$.
- `descent_lemma_holds(X, y, w0, iters)`: run with step $1/L$ for that bound $L$ and check $f(w_{k+1}) \le f(w_k) - \frac{1}{2L}\lVert\nabla f(w_k)\rVert^2$ at every step.

The tests run a **gradient check** of `grad`, the descent lemma, and the $1/k$ bound against a long run's best value.

## Hints

1. Stable softplus and sigmoid from M26.
2. $L$ = `np.linalg.eigvalsh(X.T @ X)[-1] / (4 * n)`.
3. Allow a rounding tolerance of $10^{-12}$ in the inequality.
