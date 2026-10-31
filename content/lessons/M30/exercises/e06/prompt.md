# The SVM dual by coordinate ascent

The SVM's dual is a box-constrained quadratic program (Section 5):

$$
\max_{0 \le \alpha \le C}\ D(\alpha) = \sum_i\alpha_i - \tfrac12\Big\lVert\sum_i\alpha_i y_i x_i\Big\rVert^2, \qquad w = \sum_i\alpha_i y_i x_i .
$$

One coordinate at a time it is a one-dimensional quadratic with a closed-form maximizer: with $G_i = y_i w^\top x_i - 1$ (minus the partial derivative of $D$), set $\alpha_i \leftarrow \operatorname{clip}(\alpha_i - G_i/\lVert x_i\rVert^2, 0, C)$ and update $w$ by the change.

- `dual_objective(alpha, X, y)`.
- `dual_grad(alpha, X, y)`: $\nabla D = 1 - y \odot X w$.
- `coordinate_ascent(X, y, C, epochs, rng)`: sweep the coordinates in a fresh random order each epoch; return `(alpha, w)`.

The tests run a **gradient check** of `dual_grad`, then require the duality gap $P(w) - D(\alpha)$ below $10^{-6}$ of the primal value after 400 epochs on 200 points.

## Hints

1. Keep $w$ up to date: `w += (new - old) * y[i] * X[i]`.
2. Precompute the squared norms $\lVert x_i\rVert^2$.
3. Weak duality says $D(\alpha) \le P(w)$ for every feasible $\alpha$ and every $w$; the gap is the honest stopping rule.
