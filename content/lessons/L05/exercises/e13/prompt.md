# Curved boundaries from a linear model

A linear classifier on engineered features can draw curved boundaries in the original space. Two classes separated by a circle are impossible for logistic regression on $(x_1, x_2)$ and easy on quadratic features.

- `poly2(X)`: map `(n, 2)` inputs to `(n, 6)` features $[1, x_1, x_2, x_1^2, x_1 x_2, x_2^2]$.
- `fit_and_score(F_train, y_train, F_test, y_test, l2)`: train logistic regression (no separate bias: the constant feature is in `F`) by gradient descent with `lr=0.5` for 3000 steps from zero, and return test accuracy.

## Hints

1. `np.column_stack` the six columns.
2. For the linear baseline, the tests pass `np.column_stack([ones, X])`.
3. A small L2 penalty keeps the weights finite if the training data happen to be separable.
