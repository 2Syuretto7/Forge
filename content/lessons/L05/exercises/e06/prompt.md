# Softmax regression

Implement Section 4 for $K$ classes. `W` is `(d, K)`, `b` is `(K,)`, labels `y` are integers.

- `softmax_loss(W, b, X, y, l2)`: mean cross-entropy plus $\tfrac{\lambda}{2}\|W\|_F^2$, computed stably from logits.
- `softmax_grad(W, b, X, y, l2)`: returns `(dW, db)`.
- `fit_softmax(X, y, K, lr, steps, l2)`: gradient descent from zeros, returning `(W, b)`.
- `predict_proba(W, b, X)`: `(n, K)` probabilities.

## Hints

1. `Z = X @ W + b`; subtract the row max before exponentiating.
2. `dZ = (P - onehot(y)) / n`; `dW = X.T @ dZ + l2 * W`; `db = dZ.sum(axis=0)`.
3. One-hot: `np.eye(K)[y]`.
