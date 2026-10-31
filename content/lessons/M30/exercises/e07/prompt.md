# Support vectors and complementary slackness

At the SVM optimum, complementary slackness sorts the points (Section 5):

- $\alpha_i = 0$: the point is outside the margin, $y_i w^\top x_i \ge 1$, and does not affect $w$;
- $0 < \alpha_i < C$: the point lies exactly on the margin, $y_i w^\top x_i = 1$;
- $\alpha_i = C$: the point is inside the margin or misclassified, $y_i w^\top x_i \le 1$.

The starter provides `coordinate_ascent` from e06.

- `categories(alpha, C, tol=1e-6)`: an array of `0`, `1` or `2` for the three cases.
- `margin_values(w, X, y)`: $y_i w^\top x_i$.
- `slackness_violations(alpha, w, X, y, C, tol=1e-4)`: the number of points whose category disagrees with their margin value.
- `refit_on_support(X, y, alpha, C, epochs, rng)`: rerun the solver on the points with $\alpha_i > 0$ only and return its $w$; dropping the others leaves the solution unchanged.

## Hints

1. Compare against $1 - \text{tol}$ and $1 + \text{tol}$, never exact equality.
2. The support vectors are typically a small fraction of the data when the classes are well separated.
3. A point with $\alpha_i = 0$ could be moved anywhere outside the margin without changing $w$.
