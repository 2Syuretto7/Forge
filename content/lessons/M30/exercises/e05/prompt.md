# The support vector machine, primal

A linear classifier $\operatorname{sign}(w^\top x)$ for labels $y_i \in \{-1, +1\}$ (no bias; add a constant feature if you need one) is a **soft-margin SVM** when it minimizes

$$
P(w) = \tfrac12\lVert w\rVert^2 + C\sum_i\max(0, 1 - y_i w^\top x_i) ,
$$

which trades a wide margin, $2/\lVert w\rVert$, against points inside it (Section 5).

- `primal_objective(w, X, y, C)`.
- `margin_violations(w, X, y)`: the boolean array of points with $y_i w^\top x_i < 1$.
- `subgradient(w, X, y, C)`: $w - C\sum_{\text{violators}} y_i x_i$.
- `subgradient_descent(X, y, C, iters)`: steps $1/(k + 1)$ from $w = 0$; return the best iterate seen.

The tests confirm that the subgradient method decreases the objective and classifies well, and that each point outside the margin contributes nothing to the subgradient.

## Hints

1. `np.maximum(0, 1 - y * (X @ w))`.
2. The hinge loss is not differentiable at the margin; any value between the two sides is a valid subgradient, and the formula picks one.
3. Subgradient methods are slow, about $1/\sqrt k$; keep the best value, since the objective is not monotone.
