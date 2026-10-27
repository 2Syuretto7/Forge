# Training logistic regression

Train by gradient descent with an optional L2 penalty $\tfrac{\lambda}{2}\|w\|^2$ on the weights (not the bias).

- `fit_logistic(X, y, lr, steps, l2)`: start from zeros; return `(w, b)`.
- `predict_proba(w, b, X)`.
- `accuracy(w, b, X, y)`: threshold at 0.5.

One test checks the mean-matching property from the build movement: with an intercept, the average predicted probability on the training data equals the fraction of positive labels.

## Hints

1. Reuse `sigmoid` and the gradient from exercise 4, adding `l2 * w` to `dw`.
2. A learning rate around 0.5 to 1 works for standardized features.
3. Mean matching needs enough steps to converge; 5,000 are plenty here.
