# Least squares is maximum likelihood

Model $y_i = w^\top x_i + \varepsilon_i$ with independent noise $\varepsilon_i \sim N(0, \sigma^2)$. The average negative log-likelihood, with $s = \log\sigma$, is

$$
J(w, s) = \tfrac12\log 2\pi + s + \frac{1}{2n}\lVert y - Xw\rVert^2 e^{-2s} .
$$

For any $s$, minimizing over $w$ minimizes the residual sum of squares: the MLE of $w$ is M12's least-squares solution, and the MLE of $\sigma^2$ is the mean squared residual (Section 4).

- `nll(w, s, X, y)` and `grad_w(w, s, X, y)` $= -\frac1n X^\top (y - Xw)\,e^{-2s}$.
- `fit(X, y)`: the MLE `(w, sigma2)`, with `np.linalg.lstsq` for $w$.

The tests run a **gradient check** of `grad_w`, compare with the normal equations, and confirm that perturbing either parameter raises the loss.

## Hints

1. `np.linalg.lstsq(X, y, rcond=None)[0]`.
2. The gradient with respect to $s$ is $1 - \frac1n\lVert y - Xw\rVert^2 e^{-2s}$; it vanishes at $e^{2s} = \text{RSS}/n$.
3. The MLE of $\sigma^2$ divides by $n$, not $n - d$: biased low, like the variance estimator of Section 1.
