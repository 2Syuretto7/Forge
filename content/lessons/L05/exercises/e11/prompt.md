# Break it: separable data and runaway weights

Train unregularized logistic regression on data a line separates perfectly, and watch the weight norm.

- `train_norms(X, y, lr, steps, l2, every)`: gradient descent from zero (no bias term, for simplicity). Every `every` steps record $\|w\|$; return the list.
- `train_confidence(X, y, w)`: the smallest and largest probability the model assigns to the correct label on the training set, as `(min, max)`.

Expect the unregularized norm to keep growing like $\log t$, and the L2-regularized norm to level off.

## Hints

1. The gradient is `X.T @ (sigmoid(X @ w) - y) / n + l2 * w`.
2. Use a stable sigmoid such as `0.5 * (1 + tanh(a / 2))`.
3. Probability of the correct label: $\sigma(a)$ when $y = 1$, $1 - \sigma(a)$ when $y = 0$.
