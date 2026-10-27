# Ridge regression: loss, gradient and closed form

For a design matrix `X` `(n, p)` and targets `y`, ridge minimizes

$$
J(w) = \tfrac1n\|Xw - y\|^2 + \lambda\|w\|^2 .
$$

- `ridge_loss(w, X, y, lam)` and `ridge_grad(w, X, y, lam)`.
- `ridge_closed_form(X, y, lam)`: set the gradient to zero and solve; note the factor $1/n$ means the closed form uses $n\lambda$.

## Hints

1. $\nabla J = \tfrac2n X^\top(Xw - y) + 2\lambda w$.
2. Zero gradient: $(X^\top X + n\lambda I)w = X^\top y$.
3. Check your gradient numerically before trusting the closed form.
